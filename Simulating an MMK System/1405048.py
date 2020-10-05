import heapq
import random
import sys
import numpy as np
import matplotlib.pyplot as plt


# Parameters
class Params:
    def __init__(self, lambd, omega, k):
        self.lambd = lambd
        self.omega = omega
        self.k = k


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []
        self.queue.append(-1.0)
        # self.server_status = 0.0
        self.server_status = []
        self.server_status.append(-1.0)
        self.num_in_queue = 0
        self.last_event_time = 0.0
        self.total_delay = 0.0
        self.area_in_queue = 0.0
        self.area_server_status = 0.0

        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0  # area_num_in_Q
        self.served = 0  # no of customers delayed

    def setServerStatus(self, k):
        for i in range(1, k + 1):
            self.server_status.append(0.0)

    def update(self, sim, event):
        if event.eventType == "START":
            return
        time_since_last_event = sim.now() - self.last_event_time
        self.last_event_time = sim.now()
        self.area_in_queue += self.num_in_queue * time_since_last_event
        _count = 0
        for i in range(1,sim.params.k + 1):
            _count+= self.server_status[i]
        if _count > 0:
            _count = 1
        self.area_server_status += _count * time_since_last_event
        # print(sim.now())
        # print('area_Q',self.area_in_queue)
        # print('area_status',self.area_server_status)

    def finish(self, sim):
        print('Finished', sim.now(), self.total_delay)
        self.avgQlength = self.area_in_queue / sim.now()
        self.avgQdelay = self.total_delay / self.served
        self.util = self.area_server_status / sim.now()

    def printResults(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, omega = %lf, k = %d' % (sim.params.lambd, sim.params.omega, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))

    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def generateRandomObservation(self, rate):
        mean = 1 / rate
        uniform_random = random.random()
        return -(mean * (np.log(uniform_random)))

    def __repr__(self):
        return self.eventType


class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        arrival_time = self.generateRandomObservation(sim.params.lambd)
        departure_time = sys.float_info.max
        self.sim.scheduleEvent(ArrivalEvent(arrival_time, sim))
        # self.sim.scheduleEvent(DepartureEvent(departure_time, sim))


class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        None


class ArrivalEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'A'
        self.sim = sim

    def process(self, sim):
        next_arrival_time = sim.now() + self.generateRandomObservation(sim.params.lambd)
        # print('AE : Next arrival : '+ repr(next_arrival_time))
        sim.scheduleEvent(ArrivalEvent(next_arrival_time, sim))
        server = -1
        for i in range(1, sim.params.k + 1):
            if sim.states.server_status[i] == 0.0:
                server = i
                break

        if server == -1: # that is all the servers are busy
            sim.states.num_in_queue += 1
            # print('AE: num_in_Q',sim.states.num_in_queue)
            if len(sim.states.queue) > 1:
                if sim.states.num_in_queue >= len(sim.states.queue):
                    sim.states.queue.append(sim.now())
                else:
                    sim.states.queue[sim.states.num_in_queue] = sim.now()
            else:
                sim.states.queue.append(sim.now())
                # sim.states.queue[sim.states.num_in_queue] = sim.now()
        else:
            sim.states.served += 1
            sim.states.server_status[server] = 1.0
            next_departure_time = sim.now() + self.generateRandomObservation(sim.params.omega)
            # print("AE : Next departure : "+repr(next_departure_time))
            sim.scheduleEvent(DepartureEvent(next_departure_time, sim,server))


class DepartureEvent(Event):
    def __init__(self, eventTime, sim, server):
        self.eventTime = eventTime
        self.eventType = 'D'
        self.sim = sim
        self.server = server

    def process(self, sim):
        if sim.states.num_in_queue == 0:
            sim.states.server_status[self.server] = 0.0
            departure_time = sys.float_info.max
            # self.sim.scheduleEvent(DepartureEvent(departure_time, sim))
        else:
            sim.states.num_in_queue -= 1
            delay = sim.now() - sim.states.queue[1]
            # print('Delay:',sim.states.queue[1], sim.states.num_in_queue)
            sim.states.total_delay += delay
            sim.states.served += 1
            next_departure_time = sim.now() + self.generateRandomObservation(sim.params.omega)
            sim.scheduleEvent(DepartureEvent(next_departure_time, sim,self.server))
            for i in range(1, sim.states.num_in_queue + 1):
                sim.states.queue[i] = sim.states.queue[i + 1]


class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        self.simclock = 0
        self.states.setServerStatus(self.params.k)
        self.scheduleEvent(StartEvent(0, self))

    def configure(self, params, states):
        self.params = params
        self.states = states

    def now(self):
        return self.simclock

    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))

    def run(self):
        random.seed(self.seed)
        self.initialize()
        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)

            if self.states != None:
                self.states.update(self, event)

            # print(event.eventTime, 'Event', event, self.states.served,len(self.eventQ))
            self.simclock = event.eventTime
            event.process(self)
            if self.states.served == 100000:
                break;

        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)

    def getResults(self):
        return self.states.getResults(self)


def experiment1():
    seed = 101
    sim = Simulator(seed)
    sim.configure(Params(5.0 / 60, 8.0 / 60, 1), States())
    sim.run()
    sim.printResults()
    print('Analytical Solution: ')
    avg_delay = sim.params.lambd / (sim.params.omega * (sim.params.omega - sim.params.lambd))
    avg_queue_length = (sim.params.lambd * sim.params.lambd) / (
    sim.params.omega * (sim.params.omega - sim.params.lambd))
    utility = sim.params.lambd / sim.params.omega
    print('Average delay in queue: ' + repr(avg_delay))
    print('Average length of queue: ' + repr(avg_queue_length))
    print('Utility: ' + repr(utility))


def experiment2(serverCount):
    seed = 110
    omega = 1000.0 / 60
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    for ro in ratios:
        sim = Simulator(seed)
        sim.configure(Params(omega * ro, omega, serverCount), States())
        sim.run()

        length, delay, utl = sim.getResults()
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)

    plt.figure(serverCount)
    plt.subplot(311)
    plt.plot(ratios, avglength)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(ratios, avgdelay)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(ratios, util)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Util')

    plt.show()


def experiment3():
    # Similar to experiment2 but for different values of k; 1, 2, 3, 4
    # Generate the same plots
    for k in range(1, 5):
        experiment2(k)



def main():
    experiment1()
    experiment2(1)
    experiment3()


if __name__ == "__main__":
    main()
