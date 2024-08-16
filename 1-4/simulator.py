import math
from enum import Enum
from lcg import LCGRand

class ServerStatus(Enum):
    IDLE = 0
    BUSY = 1

class EndCondition(Enum):
    FixCustomer = 0
    FixLength = 1

class Simulator:
    
    def __init__(self, q_limit, mean_interarrival, mean_service, end_condition, end_condition_type):
        # Simulator Clock
        self.__sim_time = 0.0
        
        # Random number generator
        self.__RNG = LCGRand()
        
        # State variables
        self.__server_status = ServerStatus.IDLE
        self.__num_in_q = 0
        self.__time_last_event = 0.0
        
        # Initialize the statistical counters.
        self.__num_custs_delayed  = 0
        self.__total_of_delays    = 0.0
        self.__area_num_in_q      = 0.0
        self.__area_server_status = 0.0
        
        self.__mean_interarrival = mean_interarrival
        self.__mean_service = mean_service
        self.__q_limit = q_limit
        
        self.__end_condition_type = end_condition_type
        if(end_condition_type == EndCondition.FixCustomer):
            self.__time_next_event = [None] * 3
            self.__num_delays_required = end_condition
            self.__num_events = 2
        elif(end_condition_type == EndCondition.FixLength):
            self.__time_next_event = [None] * 4
            self.__time_next_event[3] = end_condition
            self.__num_events = 3
            
            
        self.__time_arrival = [None] * (q_limit + 1)
        
        self.__time_next_event[1] = self.__sim_time + self.expon(mean_interarrival)
        self.__time_next_event[2] = 1.0e+30
        
       
    
    def timing(self):
        min_time_next_event = 1.0e+29
        self.__next_event_type = 0
        
        for x in range(1, self.__num_events+1):
            if(self.__time_next_event[x] < min_time_next_event):
                min_time_next_event = self.__time_next_event[x]
                self.__next_event_type = x
                
        if(self.__next_event_type == 0):
            print(f"\nEvent list empty at time {self.__sim_time} \n")
            exit(1)
            
        self.__sim_time = min_time_next_event
            
       
    def arrive(self):
        self.__time_next_event[1] = self.__sim_time + self.expon(self.__mean_interarrival)
        
        if(self.__server_status == ServerStatus.BUSY):
            self.__num_in_q = self.__num_in_q + 1
            
            if(self.__num_in_q > self.__q_limit):
                print(f"\nOverflow of the array time_arrival at time {self.__sim_time} \n")
                exit(2)
                
            self.__time_arrival[self.__num_in_q] = self.__sim_time
        
        else:
            delay = 0.0
            self.__total_of_delays += delay
            
            self.__num_custs_delayed = self.__num_custs_delayed + 1
            self.__server_status = ServerStatus.BUSY
            
            self.__time_next_event[2] = self.__sim_time + self.expon(self.__mean_service)
            

    def depart(self):
        if(self.__num_in_q == 0):
            self.__server_status = ServerStatus.IDLE
            self.__time_next_event[2] = 1.0e+30
        else:
            self.__num_in_q = self.__num_in_q - 1
            
            delay = self.__sim_time - self.__time_arrival[1]
            self.__total_of_delays = self.__total_of_delays + delay
            
            self.__num_custs_delayed = self.__num_custs_delayed + 1
            self.__time_next_event[2] = self.__sim_time + self.expon(self.__mean_service)
            
            for x in range(1, self.__num_in_q + 1):
                self.__time_arrival[x] = self.__time_arrival[x + 1]
                
            
    def report(self):
        print(f"\n\nAverage delay in queue {round(self.__total_of_delays / self.__num_custs_delayed, 3)} minutes")
        print(f"Average number in queue {round(self.__area_num_in_q / self.__sim_time, 3)}")
        print(f"Server utilization {round(self.__area_server_status / self.__sim_time, 3)}")
        
        if(self.__end_condition_type == EndCondition.FixCustomer):
            print(f"Time simulation ended {round(self.__sim_time, 3)} minutes")
        elif(self.__end_condition_type == EndCondition.FixLength):
            print(f"Number of delays completed {self.__num_custs_delayed}")
        
    
    def update_time_avg_stats(self):
        time_since_last_event = self.__sim_time - self.__time_last_event
        self.__time_last_event = self.__sim_time
        
        self.__area_num_in_q = (self.__area_num_in_q + ( self.__num_in_q * time_since_last_event))
        
        self.__area_server_status = ( self.__area_server_status + ( self.__server_status.value * time_since_last_event ) )
    
    
    def run(self):
        
        if(self.__end_condition_type == EndCondition.FixCustomer):
            while(self.__num_custs_delayed < self.__num_delays_required):
                # Determine the next event
                self.timing()
            
                # Update time-average statistical accumulators
                self.update_time_avg_stats()
            
                # Invoke the appropriate event function
                if(self.__next_event_type == 1): 
                    self.arrive()
                elif(self.__next_event_type == 2):
                    self.depart()
                
            self.report()
            exit(0)
        elif(self.__end_condition_type == EndCondition.FixLength):
            while True:
                # Determine the next event
                self.timing()
                
                # Update time-average statistical accumulators
                self.update_time_avg_stats()
                
                # Invoke the appropriate event function
                if(self.__next_event_type == 1): 
                    self.arrive()
                elif(self.__next_event_type == 2):
                    self.depart()
                elif(self.__next_event_type == 3):
                    self.report()
                    exit(0)
            
       
    def get_next_event_type(self):
        return self.__next_event_type
       
    
    # def get_num_custs_delayed(self):
    #     return self.__num_custs_delayed
    
        
    def expon(self, mean):
        return -mean * math.log(self.__RNG.GetRand(1))
        
     
