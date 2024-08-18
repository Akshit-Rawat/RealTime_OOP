import sys
import keyboard
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random
#from buffers_1 import FIFO
from buffers_1 import CircBuff
from scipy.stats import expon, norm

import matplotlib.pyplot as plt

plt.ion()
class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient',loop_time=0.5,receive_loop_idle_addition=self.callloop)
        
        
        self.set_subscriber_topic('plotting')
        
        # the circular buffer has a limit of 20 as it corresponds to storing 20 datapoints.
        # as the time constant selected is 0.1, the data generated for a time window of 1 second
        #would be 10. the selection of number of data points to be generated is so to reflect the 
        # amount of data to plotted by the client. To match the refresh time, the data size sent would be half the size of requested data, this would make
        # data sending faster and chances of loss of data or overwritting minimizes.
        #buffer size also reflects the time window which will be shown, that is of 2 seconds.
        
        #plus the canvas draw() would show all the 20 datapoints and to show new datapoints everytime, the flush events is used, so that the screen can be updated 
        
        self.buff_size = 20
        
        self.client_circ = CircBuff(size = 20)
        #self.client_fifo_o = FIFO(self.buff_size/10)
        
        self.fig_circ, self.ax_circ = plt.subplots()
        #self.publish_payload({'size':self.buff_size/2},'request')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        
        
        if topic == 'plotting':
            

             

            #if len(payload["data"])<= self.client_circ.size/2:
            self.client_circ.write(payload["data"])
                
            print('update plot at t={}s'.format(payload["time"]))  
            t_, x_ = zip(*self.client_circ.read())
            print(self.client_circ.read())
            self.ax_circ.clear()
                

            self.ax_circ.stem(t_, x_)
            self.ax_circ.set_xlim([payload["time"]-2,payload["time"]]) #this would show the update according to the buffer read point position, which would be last index, therefore the plot update would be every 0.5 seconds
            self.ax_circ.set_ylim([-10, 10])
            self.fig_circ.canvas.draw()  # update figure
            self.fig_circ.canvas.flush_events()

            if payload["time"]>=10:
                print("Plotting complete")
                self.publish_payload({'size': self.buff_size / 2}, 'interrupt')
                input("Press Enter to exit")
            
                self.clean_up()
                sys.exit(0)    

                

        
        if keyboard.is_pressed('l'):
            print("Interrupt key pressed. Sending interrupt...")
            self.publish_payload({'size': self.buff_size / 2}, 'interrupt')
            self.clean_up()
            sys.exit(0)
            
            
        
        
        
    def callloop(self):
        self.publish_payload({'size':self.buff_size/2},'request')    
        
    


def buff_client():
    BuffClient()


if __name__ == '__main__':
    buff_client()


    