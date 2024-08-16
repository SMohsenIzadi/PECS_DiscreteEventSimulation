import math
from enum import Enum
from lcg import LCGRand

class Simulator:
    
    def __init__(self, initial_inv_level, holding_cost, shortage_cost, setup_cost, minlag, maxlag, incremental_cost, num_months, mean_interdemand, prob_distrib_demand):
        
        # Random Number Generator
        
        self.__RNG = LCGRand()

        # Initialize the state variables. 

        self.__initial_inv_level = initial_inv_level

        # Initialize the event list.  Since no order is outstanding, the order-
        # arrival event is eliminated from consideration. 

        self.__mean_interdemand = mean_interdemand
        self.__num_months = num_months
        self.__num_events = 4
        self.__setup_cost = setup_cost
        self.__incremental_cost = incremental_cost
        self.__minlag = minlag
        self.__maxlag = maxlag
        self.__holding_cost = holding_cost
        self.__shortage_cost = shortage_cost
        self.__amount = 0 # do nothing here (Just for clarity of code)

        self.__time_next_event = [None] * 5
        self.__prob_distrib_demand = prob_distrib_demand
    
    
    def load_policy(self, smalls, bigs):
        self.__sim_time = 0.0
        self.__inv_level = self.__initial_inv_level
        self.__time_last_event = 0.0
        
        self.__total_ordering_cost = 0.0
        self.__area_holding        = 0.0
        self.__area_shortage       = 0.0
        
        self.__time_next_event[1] = 1.0e+30
        self.__time_next_event[2] = self.__sim_time + self.expon(self.__mean_interdemand)
        self.__time_next_event[3] = self.__num_months
        self.__time_next_event[4] = 0.0
        
        self.__smalls = smalls
        self.__bigs = bigs
    
    
    def timing(self):
        min_time_next_event = 1.0e+29
        self.__next_event_type = 0
        
        for x in range(1, self.__num_events+1):
            if(self.__time_next_event[x] < min_time_next_event):
                min_time_next_event = self.__time_next_event[x]
                self.__next_event_type = x
                
        if(self.__next_event_type == 0):
            print(f"\nEvent list empty at time {self.__sim_time} \n")
            
        self.__sim_time = min_time_next_event
    
    
    def order_arrival(self):
        self.__inv_level = (self.__inv_level + self.__amount)
        self.__time_next_event[1] = 1.0e+30
    
    
    def demand(self):
        self.__inv_level = self.__inv_level - self.random_integer()
        self.__time_next_event[2] = self.__sim_time + self.expon(self.__mean_interdemand)
    
    
    def evaluate(self):
        if (self.__inv_level < self.__smalls):
            self.__amount = (self.__bigs - self.__inv_level)
            self.__total_ordering_cost = self.__total_ordering_cost + ( self.__setup_cost + (self.__incremental_cost * self.__amount) )
            
            self.__time_next_event[1] = self.__sim_time + self.uniform(self.__minlag, self.__maxlag)
            
        self.__time_next_event[4] = self.__sim_time + 1.0
    
    
    def report(self):
        avg_ordering_cost = self.__total_ordering_cost / self.__num_months
        avg_holding_cost  = self.__holding_cost * self.__area_holding / self.__num_months
        avg_shortage_cost = self.__shortage_cost * self.__area_shortage / self.__num_months
        avg_total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost
        
        print(f"({str(self.__smalls).rjust(3)},{str(self.__bigs).rjust(3)})\t{round(avg_total_cost, 2)}\t\t{round(avg_ordering_cost, 2)}\t\t{round(avg_holding_cost, 2)}\t\t{round(avg_shortage_cost, 2)}")
    
    
    def update_time_avg_stats(self):
        time_since_last_event = self.__sim_time - self.__time_last_event
        self.__time_last_event = self.__sim_time
        
        if (self.__inv_level < 0):
            self.__area_shortage -= (self.__inv_level * time_since_last_event)
        elif (self.__inv_level > 0):
            self.__area_holding  += (self.__inv_level * time_since_last_event)
    
    
    def run(self):
        
        while True:
            self.timing()
            
            self.update_time_avg_stats()
            
            if(self.__next_event_type == 1):
                self.order_arrival()
            elif(self.__next_event_type == 2):
                self.demand()
            elif(self.__next_event_type == 4):
                self.evaluate()
            elif(self.__next_event_type == 3):
                self.report()
                return
            
    
    
    def expon(self, mean):
        return -mean * math.log(self.__RNG.GetRand(1))
    
    
    # Random integer generation
    # prob_distrib in an array
    def random_integer(self):
        u = self.__RNG.GetRand(1)
        
        i = 1
        while(u >= self.__prob_distrib_demand[i]):
            i=i+1
            
        return i
    
    
    def uniform(self, a, b):
        return a + self.__RNG.GetRand(1) * (b - a)
    
    
    
        