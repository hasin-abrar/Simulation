import heapq
import random
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
        
        # Statistics
        self.util = 0.0         
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0

    def update(self, sim, event):
        None
    
    def finish(self, sim):
        None
        
    def printResults(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, omega = %lf, k = %d' % (sim.params.lambd, sim.params.omega, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))
     
    def getResults(self, sim):
        return (self. avgQlength, self.avgQdelay, self.util)
   
class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None
        
    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')
    
    def __repr__(self):
        return self.eventType

class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim
        
    def process(self, sim):
        None
                
class ExitEvent(Event):    
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim
    
    def process(self, sim):
        None

                                
class ArrivalEvent(Event):        
    def process(self, sim):
        None
        
class DepartureEvent(Event):            
    def process(self, sim):
        None                                       

class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0   
        self.seed = seed
        self.params = None
        self.states = None
        
    def initialize(self):
        self.simclock = 0        
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
            
            if self.states != None:
                self.states.update(self, event)
                
            print (event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)
     
        self.states.finish(self)   
    
    def printResults(self):
        self.states.printResults(self)
        
    def getResults(self):
        return self.states.getResults(self)
        

def experiment1():
	seed = 101    
	sim = Simulator(seed)
	sim.configure(Params(5.0/60, 8.0/60, 1), States())
	sim.run()
	sim.printResults()

def experiment2():
    seed = 110
    omega = 1000.0 / 60
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []
    
    for ro in ratios:
        sim = Simulator(seed)
        sim.configure(Params(omega * ro, omega, 1), States())    
        sim.run()
        
        length, delay, utl = sim.getResults()
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)
        
    plt.figure(1)
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
	None
				            
def main():
	experiment1()
	experiment2()
	experiment3()        

          
if __name__ == "__main__":
    main()
                  