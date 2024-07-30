import sys
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random
from buffers_1 import CircBuff
from scipy.stats import expon, norm

import matplotlib.pyplot as plt
from time import sleep


class BuffServer(BanyanBase):
    
    
    def __init__(self,dt = .01,sigma =1):

        super().__init__(process_name = 'BuffServer',receive_loop_idle_addition=None,loop_time = 0.1)
        
        self.dt = dt
        self.sigma = sigma
        self.set_subscriber_topic('initiation')
        self.client_cb = CircBuff(size=101)
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        G = norm(loc=0, scale=self.sigma*np.sqrt(self.dt))

        
        
        #server_cb = CircBuff(size=501)
        t = 0 
        x = 0
        self.client_cb.write((0, 0))

        #fig_cb, ax_cb = plt.subplots()

        while t <= 100:
            t += self.dt
            x += G.rvs()
            self.client_cb.write((t, x))
            cb = self.client_cb.read()

            if np.abs(t % 1) <= self.dt:
                
                payload = {'data':cb}
                self.publish_payload(payload,"plotting")
                #server_cb.write(cb)
                #server_cb.read()
                self.client_cb.clear()
        
        #buffer_server = CircBuff(10)

        #buffer_server.read()
        #buffer_server.write()



        
        
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





