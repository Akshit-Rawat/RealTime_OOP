import sys
from banyan_base import BanyanBase
import numpy as np
import random

from buffers_1 import FIFO
from scipy.stats import expon, norm, invgauss
from math import sqrt




class BuffServer(BanyanBase):
    
    
    def __init__(self):

        super().__init__(process_name = 'BuffServer',receive_loop_idle_addition=self.datageneration_loop,loop_time = 0.1)
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
            if not cb_data:  # this is done because, as soon as the request is sent the buffer is read empty therefore it caused an error in the client side as it sends an empty list, which is for a cicular buffer not valid
                return         # does not return anything but it executes and lets the function progress to next phase
            else:
                payload = {'data':cb_data,'time':self.t} #
                self.publish_payload(payload,"plotting")
                self.server_fifo.clear()
                self.topicc.clear()
        
           
            
            
                
        elif topic == 'interrupt':
            self.topic_ = False
            print("client interrupt")
            self.server_fifo.clear()

        
             
       # if i keep writing function outside and then according to topic it registers the data     
            
                
      #or writing can be inside and whenever the topic gets triggered the sample generator works
      # and iterates and as the self function should update anyywhere
    
    #works quite well for 0.5 loop
    
    
    def datageneration_loop(self):

        
            if self.topic_:
                (self.t,self.xt) = generate_next_sample(current_sample=(self.t,self.xt),tau=0.1,sigma=0.5)
                #self.new_sample =(self.t,self.xt)
                #print('added {} at t={}s'.format(self.xt,self.t))
                self.server_fifo.write((self.t,self.xt), current_time=self.t)
                
                #self.new_sample=None 
            #explanation for above: as the loop time was same(0.5), the buffer was getting
            #adequate time to reset or clear out the old data, therefore the tuple value was able to update
            #however as the loop time was decreased, the tuple object was not updating, therefore the buffer was being overwritten by the same value again and again
            #hence reseting the sample by putting none solved the overwrriting issue.
            else:
                return 
                
                
                    
                        
#every 0.5 second the reading and clearing of data occurs and sending too
               
                    
        
                
           

            

def generate_next_sample(current_sample = None, tau=.01,sigma=1):
    if current_sample is None:
        return 0, 0
    else:
        T = invgauss(mu=tau)
        dt = T.rvs()
        X = norm(loc=0, scale=sigma)
        t, xt = current_sample
        t += dt
        xt += X.rvs() * sqrt(dt)
        return t, xt  

        
     

def buff_server():
    BuffServer()


if __name__ == '__main__':
    buff_server()



#i think there might be but let say there is no need of 


#the thing which worked was using the datageneration loop in the receive loop idle addition but the reverse shall work



