import sys
from banyan_base import BanyanBase
import numpy as np
import random

from buffers_1 import FIFO
from scipy.stats import expon, norm, invgauss
from math import sqrt




class BuffServer(BanyanBase):
    
    
    def __init__(self):

        super().__init__(process_name = 'BuffServer',receive_loop_idle_addition=self.datageneration_loop,loop_time = 0.1) # super function is used for inheritence from the base class which is the banyan_base
        #loop time set to 0.1 so that data generation happens every 0.1 second
        #two topics have been created below so that according to topic data streaming can either be stopped or start 
        self.set_subscriber_topic('request') #initiates the data streaming
        self.set_subscriber_topic('interrupt') # disrupts the datastreaming
        self.server_fifo = FIFO(1) # the size of the buffer is to set to temporal window of 1, maximum samples it can hold would be equivalent to 10 as the time constant is set to 0.1
        self.t = 0   # initialisation of both time stamps and sample value
        self.xt = 0
        #self.new_sample=0
        self.topic_=False # a boolean logic implemented to start and stop the data generation loop 
        self.topicc=[] # to check how many samples would be sent per topic call
        
        
        try:   
            self.receive_loop()  #receive loop for accepting the topic from client
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        

        
        
        if topic=='request':        # when topic is request, the self.topic_ is set to True which initiates the if condition in the data generation looop
            self.topic_ = True
            self.topicc.append(topic)  # topic request accepted and saved in the topic collection list
            print(self.topicc)
            
        
         
            cb_data = self.server_fifo.read() # collected samples from the buffer is read and made ready to be submitted as payload
            
            
            print(cb_data)
            if not cb_data:  # this is done because, as soon as the request is sent, the buffer is read empty therefore, it caused an error in the client side as it sends an empty list, which is for a cicular buffer not valid
                return         # does not return anything but it executes and lets the function progress to next phase
            else:
                payload = {'data':cb_data,'time':self.t} # collected samples are now packed in to payload. "data" has both sample time stamp and sample amplitude, with it is "time" key, which will hold time stamps as well
                self.publish_payload(payload,"plotting") # payload is published using plotting topic as the subsriber topic of client.
                self.server_fifo.clear() # fifo buffer and topic collector list are cleared so that new samples can be added and avoid overflow/overwriting of data 
                self.topicc.clear() 
        
           
            
            
                
        elif topic == 'interrupt': # when topic interrupt is accepted, then the self topic boolean turns to false, which changes the state of the idle loop and stops it from further generating more data
            self.topic_ = False
            print("client interrupt")
            self.server_fifo.clear()
            input("Press Enter to exit")
            
            self.clean_up()
            sys.exit(0)

        
             
       
    
    def datageneration_loop(self): # thisis the receive addition idle loop, and it serves the function of data generation

        
            if self.topic_: # when the state changes to true, whcih happens when topic reques is received by the server. the data generation loop gets initiated 
                (self.t,self.xt) = self.generate_next_sample(current_sample=(self.t,self.xt),tau=0.01,sigma=1) # the generate next sample function generates new samples each time the idle loop runs.
                
                self.server_fifo.write((self.t,self.xt), current_time=self.t) # the fifo buffer writes the generated samples.
                print(self.topic_)
                
            else: # this condition is met when the server receives the topic 'interrupt'. It breaks the if condition, subsequently breaking the gneration of new samples due to loop
                return  print(self.topic_)
                
          # once the topic 'request' gets received, the data as much as collected over the period of 0.5s in buffer, get sent off to the client. Request acts like a trigger to send of the collected data.      
                    
 
    def generate_next_sample(self,current_sample = None, tau=.01,sigma=1): # this is the sample generator method/function
        if current_sample is None:
            return 0, 0        # when no inital values assigned
        else:
            T = invgauss(mu=tau)  # tau is the mean of inversgauss
            dt = T.rvs() #  this function picks the random value from the distribution
            X = norm(loc=0, scale=sigma)
            t, xt = current_sample # this way the sample gnerator gets updated with each loop
            t += dt   #these update the t and xt values
            xt += X.rvs() * sqrt(dt)  
            return t, xt            
                    
        
                
           

            



        
     

def buff_server():
    BuffServer()


if __name__ == '__main__':
    buff_server()





