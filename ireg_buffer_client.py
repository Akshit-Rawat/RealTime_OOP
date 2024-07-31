import sys
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random
from buffers_1 import FIFO
from scipy.stats import expon, norm

import matplotlib.pyplot as plt
from time import sleep
plt.ion()
class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient',loop_time=0.001)
        
        
        # data creation 
        self.set_subscriber_topic('plotting')
        
        self.server_fifo = FIFO(5)
        self.loop_time = 0.001
        self.fig_fifo, self.ax_fifo = plt.subplots()
        self.publish_payload({'data_size':self.loop_time},'initiation')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        
        if payload["time"] <9:
            self.server_fifo.write(payload["data"],current_time=payload["time"])
            
        

            t_, x_ = zip(*self.server_fifo.read())
            self.ax_fifo.clear()
            self.ax_fifo.stem(t_, x_)
            self.ax_fifo.set_xlim([payload["time"]-2,payload["time"]])
            self.ax_fifo.set_ylim([-10, 10])
            self.fig_fifo.canvas.draw()  # update figure
            self.fig_fifo.canvas.flush_events()
            sleep(.5)
        else:
            print("Plotting complete")
            input("Press Enter to exit")
            self.clean_up()
            sys.exit(0) 
        
        
        
        
        
        
        #plt.ion()
        #x = payload['data']
        #plt.plot(x)
        #print("plotting complete")
        #input('Press enter to exit.')
        #self.clean_up()
        #sys.exit(0)


def buff_client():
    BuffClient()


if __name__ == '__main__':
    buff_client()