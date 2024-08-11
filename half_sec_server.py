import sys
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random

from buffers_1 import FIFO
from scipy.stats import expon, norm, invgauss
from math import sqrt

import matplotlib.pyplot as plt
from time import sleep


class BuffServer(BanyanBase):
    
    
    def __init__(self,dt=0.5):

        super().__init__(process_name = 'BuffServer',receive_loop_idle_addition=None,loop_time = 0.1)
        
        self.dt =dt
        self.set_subscriber_topic('initiation')
        self.server_fifo = FIFO(1)
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        data_size = payload['size']
        t = 0 
        xt = 0
        self.server_fifo.write((0,0))
        

        
        while True:
            (t,xt) = generate_next_sample(current_sample=(t,xt),tau=0.1,sigma=1)
            
            if t<10:
                
                
                    print('added {} at t={}s'.format(xt,t))
                    self.server_fifo.write((t, xt), current_time=t)
                    
                    #this is collecting data and sending data collected every 0.5 seconds from server side
                    cb_data =self.server_fifo.read()  
                    if len(cb_data) >= data_size/2:
                        payload = {'data':cb_data,'time':t}
                        self.publish_payload(payload,"plotting")
                        self.server_fifo.clear()

               
                    
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





