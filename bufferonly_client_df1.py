import sys
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random
from buffers_1 import CircBuff
from scipy.stats import expon, norm

import matplotlib.pyplot as plt
from time import sleep
plt.ion()
class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient',loop_time=0.001)
        
        
        # data creation 
        self.set_subscriber_topic('plotting')
        
        self.server_cb = CircBuff(size=501)
        self.loop_time = 0.001
        self.fig_cb, self.ax_cb = plt.subplots()
        self.publish_payload({'data_size':self.loop_time},'initiation')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        
        if payload["time"] <=100:
            self.server_cb.write(payload["data"])
            self.server_cb.read()
        

            t_, x_ = zip(*self.server_cb.read())
            self.ax_cb.clear()
            self.ax_cb.scatter(t_, x_,s = 1)
            self.ax_cb.set_xlim([payload["time"]-5,payload["time"]])
            self.ax_cb.set_ylim([-10, 10])
            self.fig_cb.canvas.draw()  # update figure
            self.fig_cb.canvas.flush_events()
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