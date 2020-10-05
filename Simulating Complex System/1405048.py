import heapq
import random
import queue as Q
import numpy as np

TYPE  = 1
customer_id = 0

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
        self.queue = Q.PriorityQueue()
        # self.server_status = 0.0
        self.server_status = []
        self.server_status.append(-1.0)
        self.num_in_queue = 0
        self.num_in_queue_max = -1
        self.last_event_time = 0.0
        self.total_delay = 0.0
        self.total_delay_max = -1.0
        self.server_status_max = -1
        self.area_in_queue = 0.0
        self.area_server_status = 0.0

        # Statistics
        self.server_busy_avg = 0.0
        self.avgTotalDelay = 0.0
        self.avgQlength = 0.0
        self.served = 0


    def setServerStatus(self, k):
        for i in range(1, k + 1):
            self.server_status.append(0.0)

    def update(self, sim, event):
        if event.eventType == "START":
            return
        time_since_last_event = sim.now() - self.last_event_time
        self.last_event_time = sim.now()
        if self.num_in_queue > self.num_in_queue_max:
            self.num_in_queue_max = self.num_in_queue
        self.area_in_queue += self.num_in_queue * time_since_last_event
        _count = 0
        for i in range(1,sim.params.k + 1):
            _count+= self.server_status[i]
        if _count > self.server_status_max:
            self.server_status_max = _count
        self.area_server_status += _count * time_since_last_event # now sure about this stat

    def finish(self, sim):
        self.avgQlength = self.area_in_queue / 480.0
        self.avgTotalDelay = self.total_delay / self.served
        self.server_busy_avg = self.area_server_status / sim.now()

    def printResults(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, omega = variable, k = %d' % (sim.params.lambd, sim.params.k))
        print('MMk Total customer satisfied: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Maximum queue length: %lf' % (self.num_in_queue_max))
        print('MMk Average customer delay in total: %lf' % (self.avgTotalDelay))
        print('MMk Maximum customer delay in total: %lf' % (self.total_delay_max))
        print('MMk Time-average server busy: %lf' % (self.server_busy_avg))
        print('MMk Maximum number server busy: %lf' % (self.server_status_max))

    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)


class Customer:
    def __init__(self, priority,arrival_time):
        global customer_id
        customer_id+=1
        self.id = customer_id
        self.priority = priority # either number of customers in Q or number of unsatisfactory services
        self.arrival_time = arrival_time
        self.a = 2
        self.b = 2.8
        self.p = 0.2
        self.i = 0 # unsatisfactory services
    def __lt__(self, other):
        if TYPE == 1:
            return self.priority < other.priority
        else:
            return self.priority > other.priority


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType

    def generateRandomObservation(self, rate):
        mean = 1 / rate
        uniform_random = random.random()
        return -(mean * (np.log(uniform_random)))


class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        arrival_time = self.generateRandomObservation(sim.params.lambd)
        self.sim.scheduleEvent(ArrivalEvent(arrival_time, sim))


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
        sim.scheduleEvent(ArrivalEvent(next_arrival_time, sim))
        server = -1
        for i in range(1, sim.params.k + 1):
            if sim.states.server_status[i] == 0.0:
                server = i
                break

        if server == -1:  # that is all the servers are busy
            sim.states.num_in_queue += 1
            if(TYPE == 1):
                new_customer = Customer(sim.states.num_in_queue,sim.now())
            else:
                new_customer = Customer(0, sim.now())
            sim.states.queue.put(new_customer)
            # print('AE: num_in_Q',sim.states.num_in_queue)
            # if len(sim.states.queue) > 1:
            #     if sim.states.num_in_queue >= len(sim.states.queue):
            #         sim.states.queue.append(sim.now())
            #     else:
            #         sim.states.queue[sim.states.num_in_queue] = sim.now()
            # else:
            #     sim.states.queue.append(sim.now())
            #     # sim.states.queue[sim.states.num_in_queue] = sim.now()
        else:
            sim.states.server_status[server] = 1.0
            new_customer = Customer(0, sim.now()) # for service time delay
            service_mean = random.uniform(new_customer.a,new_customer.b)
            next_departure_time = sim.now() + self.generateRandomObservation(1.0/service_mean) # between a and b
            # print("AE : Next departure : "+repr(next_departure_time))
            sim.scheduleEvent(DepartureEvent(next_departure_time, sim, server,new_customer))


class DepartureEvent(Event):
    def __init__(self, eventTime, sim, server,customer):
        self.eventTime = eventTime
        self.eventType = 'D'
        self.sim = sim
        self.server = server
        self.customer = customer

    def process(self, sim):
        customer_satisfaction_prob = random.random()
        if sim.states.num_in_queue == 0:
            if customer_satisfaction_prob > self.customer.p : # customer satisfied
                sim.states.server_status[self.server] = 0.0
                delay = sim.now() - self.customer.arrival_time
                if delay > sim.states.total_delay_max:
                    sim.states.total_delay_max = delay
                sim.states.total_delay += delay # including Q delay and service time
                sim.states.served += 1
            else: # unsatisfied
                self.customer.i += 1
                # print('Unsatisfied',self.customer.id,self.server, self.customer.p,self.customer.i)
                service_mean = random.uniform(self.customer.a/(self.customer.i+1), self.customer.b/(self.customer.i+1))
                self.customer.p /= (self.customer.i+1)
                next_departure_time = sim.now() + self.generateRandomObservation(1.0 / service_mean)  # between a and b
                sim.scheduleEvent(DepartureEvent(next_departure_time, sim, self.server, self.customer))

        else:
            if customer_satisfaction_prob > self.customer.p: # customer satisfied
                delay = sim.now() - self.customer.arrival_time
                if delay > sim.states.total_delay_max:
                    sim.states.total_delay_max = delay
                sim.states.total_delay += delay  # including Q delay and service time
                sim.states.served += 1
            else:
                self.customer.i += 1
                # print('Unsatisfied', self.customer.id,self.server,self.customer.p,self.customer.i)
                sim.states.num_in_queue += 1 # as will be returned to the Q
                if TYPE == 1:
                    self.customer.priority = sim.states.num_in_queue
                else:
                    self.customer.priority = self.customer.i
                sim.states.queue.put(self.customer) # returned to the Q

            sim.states.num_in_queue -= 1
            new_customer = sim.states.queue.get() # another from the Q
            service_mean = random.uniform(new_customer.a / (new_customer.i + 1),
                                          new_customer.b / (new_customer.i + 1))
            new_customer.p /= (new_customer.i + 1)
            next_departure_time = sim.now() + self.generateRandomObservation(1.0 / service_mean)  # between a and b
            sim.scheduleEvent(DepartureEvent(next_departure_time, sim, self.server, new_customer))


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

            if event.eventType == 'EXIT':
                break

            self.simclock = event.eventTime
            if self.simclock > 480 :
                self.simclock = 480
                break
            if self.states != None:
                self.states.update(self, event)

            print(event.eventTime, 'Event', event)

            event.process(self)

        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)

    def getResults(self):
        return self.states.getResults(self)


def solveProblem():
    seed = 101
    sim = Simulator(seed)
    sim.configure(Params(1.0/5, 8.0 / 60, 5), States())
    sim.run()
    sim.printResults()


def main():
    solveProblem()
    # experiment2()
    # experiment3()


if __name__ == "__main__":
    main()

