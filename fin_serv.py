import sys
from banyan_base import BanyanBase
import numpy as np
import random

from buffers_1 import FIFO
from scipy.stats import expon, norm, invgauss
from math import sqrt




class BuffServer(BanyanBase):
    
    
    def __init__(self):

        super().__init__(process_name = 'BuffServer',receive_loop_idle_addition=None,loop_time = 0.01)
        
        
        self.set_subscriber_topic('request')
        self.set_subscriber_topic('interrupt')
        self.set_subscriber_topic('send_data')
        self.server_fifo = FIFO(1)
        self.t = 0 
        self.xt = 0
        self.new_sample=0
        self.topic_=False
        self.topicc=[]
        self.loop_time = 0
        
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        self.loop_time=payload["loop_time"]

        self.topicc.append(topic)
        print(self.topicc)
        
        if topic=='request':
            self.topic_ = True
            self.data_gen()

            self.publish_payload({'loop_time':0.5},"data_ready")
            
            
            
        
        if topic=='send_data':
            cb_data = self.server_fifo.read()
            
            
            print(cb_data)
            if not cb_data:
                return
            else:
                payload = {'data':cb_data,'time':self.t}
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
    
    
    #def datageneration_loop(self):

        
    #        if self.topic_:
    #            (self.t,self.xt) = generate_next_sample(current_sample=(self.t,self.xt),tau=0.1,sigma=0.5)
    #            self.new_sample =(self.t,self.xt)
    #            #print('added {} at t={}s'.format(self.xt,self.t))
                
                
                #self.new_sample=None 
            #explanation for above: as the loop time was same(0.5), the buffer was getting
            #adequate time to reset or clear out the old data, therefore the tuple value was able to update
            #however as the loop time was decreased, the tuple object was not updating, therefore the buffer was being overwritten by the same value again and again
            #hence reseting the sample by putting none solved the overwrriting issue.
    #        else:
    #            return 
                
                
                    
                        
#every 0.5 second the reading and clearing of data occurs and sending too
               
    def data_gen(self):

        while True:  
            (self.t,self.xt) = generate_next_sample(current_sample=(self.t,self.xt),tau=0.1,sigma=0.5)
            if len(self.server_fifo.read())<=self.loop_time*10:
                self.server_fifo.write((self.t,self.xt), current_time=self.t)
                print(self.server_fifo.read())
            else:
                break    


            

            
                
           

            

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



