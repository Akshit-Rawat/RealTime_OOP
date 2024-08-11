import sys
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random
#from buffers_1 import FIFO
from buffers_1 import CircBuff
from scipy.stats import expon, norm

import matplotlib.pyplot as plt
from time import sleep
plt.ion()
class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient',loop_time=0.1,receive_loop_idle_addition=None)
        
        
        # data creation 
        self.set_subscriber_topic('plotting')
        
        # the circular buffer has a limit of 30 as it corresponds to storing 30 datapoints.
        #although the server would only send 10 datapoints for every second, it is safer to take a bigger buffer
        
        #plus the canvas draw() would show all the 30 datapoints and to show new datapoints everytime, the flush events is used, so that the screen can be updated 
         #the new model sends empty buffer, thats why it would not read anything and would throw error
        self.buff_size = 20
        self.client_fifo = CircBuff(self.buff_size)
        
        self.fig_fifo, self.ax_fifo = plt.subplots()
        self.publish_payload({'size':self.buff_size/2},'initiation')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        data = []
        if payload["time"] <9:
            self.client_fifo.write(payload["data"])
            
            data.append(payload["data"])
            print('update plot at t={}s'.format(payload["time"]))
            t_, x_ = zip(*self.client_fifo.read())
            self.ax_fifo.clear()
            print(data)

            self.ax_fifo.stem(t_, x_)
            #self.ax_fifo.set_xlim([payload["time"]-2,payload["time"]])
            self.ax_fifo.set_ylim([-10, 10])
            self.fig_fifo.canvas.draw()  # update figure
            self.fig_fifo.canvas.flush_events()
            sleep(0.5)
        elif payload["time"] >9: 
            print("Plotting complete")
            input("Press Enter to exit")
            
            self.clean_up()
            sys.exit(0) 
        
        
        
    #def callloop(self):
    #    self.publish_payload({'data_size':self.loop_time},'initiation')    
        
    


def buff_client():
    BuffClient()


if __name__ == '__main__':
    buff_client()