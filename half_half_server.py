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
        self.client_fifo = FIFO(1)
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        data_size = payload['size']
        t = 0 
        xt = 0
        self.client_fifo.write((0,0))
        

        
        
        #server_cb = CircBuff(size=501)
        

        #fig_cb, ax_cb = plt.subplots()
        
        
        
        while True:
            (t,xt) = generate_next_sample(current_sample=(t,xt),tau=0.01,sigma=1)
            
            if t<10:
                
                #if np.abs(xt - last_x) >= epsilon:
                    print('added {} at t={}s'.format(xt,t))
                    self.client_fifo.write((t, xt), current_time=t)
                    #last_x = xt
                    #this is collecting data and sending data collected every 0.5 seconds from server side
                    cb_data =self.client_fifo.read()  
                    if len(cb_data) >= data_size/2:
                        payload = {'data':cb_data,'time':t}
                        self.publish_payload(payload,"plotting")
                        self.client_fifo.clear()

                    
                    #if np.abs(t % 1) >= 0.5:
                    #    cb1 = [  y for y in self.client_fifo.read()[:] if  np.abs(y[0] % 1) <=0.5 ]
                    #    cb2 = [ y for y in self.client_fifo.read()[:] if  np.abs(y[0] % 1) >0.5 ]
                    #    print(cb1)
                    #    print(cb2)
                    #    payload = {'data':cb1,'time':t}
                    #    self.publish_payload(payload,"plotting")
                    #    cb1.clear()
                    #    payload = {'data':cb2,'time':t}
                    #    self.publish_payload(payload,"plotting")
                    #    cb2.clear()
                    #    self.client_fifo.clear()


                         
                # this acts like a trigger, so the buffer would fill until t value reaches 0.5 or in a sense buffer collects half a second value and then sends the data
                        #may be not form a loop that is wht it is running 4 times each time
                       
                       # if t in self.client_fifo.read()[:][0] <= 0.5:
                        #        cb1.append(self.client_fifo.read()[tt][:])
                         #       payload = {'data':cb1,'time':t}
                          #      self.publish_payload(payload,"plotting")
                           #     cb1.clear()
                            #if np.abs(self.client_fifo.read()[tt][0] % 1) > 0.5:
                             #   cb1.append(self.client_fifo.read()[tt][:])
                             #   payload = {'data':cb1,'time':t}
                             #   self.publish_payload(payload,"plotting")
                             #   cb1.clear()
                        #self.client_fifo.clear()




                
                    
            else:
                break        
            
            
                
            
            #t += self.dt
            #x += G.rvs()
        
            #if np.abs(x - last_x) >= epsilon:
            #    self.client_fifo.write((t, x), current_time=t)
            #    last_x = x
            #    print('added {} at t={}s'.format(x, t))

            #if np.abs(t % 1) <= self.dt:
                
            #    payload = {'data':self.client_fifo.read(),'time':t}
            #    self.publish_payload(payload,"plotting")
            #    #server_cb.write(cb)
            #    #server_cb.read()
            #    self.client_fifo.clear()
        
        #buffer_server = CircBuff(10)

        #buffer_server.read()
        #buffer_server.write()

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

        
        
        #buffer = []
        
        #buffer = np.zeros(payload['data_size']) 

        #for i in range(len(buffer)):
        #    buffer[i] = random.randint(0,10)

        #data_list = list(buffer)

        #payload = {'data':data_list}
        
       # self.publish_payload(payload,"plotting")
        #print("Data sent")
        #print(payload["data"])


def buff_server():
    BuffServer()


if __name__ == '__main__':
    buff_server()





