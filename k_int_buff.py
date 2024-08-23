import sys
import keyboard
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random

from buffers_1 import CircBuff
from scipy.stats import expon, norm

import matplotlib.pyplot as plt

plt.ion()
class BuffClient(BanyanBase):
    def __init__(self,refresh_time=0.5):

        super().__init__(process_name = 'BuffClient',loop_time=refresh_time,receive_loop_idle_addition=self.callloop) # refresh time is set to 0.5 s
        
        
        self.set_subscriber_topic('plotting')
        
        # the circular buffer has a limit of 20 as it corresponds to storing 20 datapoints.
        # as the time constant (sample period) selected is 0.1, the data generated for a time window of 1 second
        #would be 10. the selection of number of data points to be generated is so to reflect the 
        # amount of data to plotted by the client. To match the refresh time. the data size would be equal to 5 data points for sampel period of 0.1 seconds to avoid overflow 
        #buffer size also reflects the time window which will be shown, that is of 2 seconds.
        self.refresh_time= refresh_time # thisis the referesh time
        #plus the canvas draw() would show all the 20 datapoints and to show new datapoints everytime, the flush events is used, so that the screen can be updated 
        
          
        
        self.client_circ = CircBuff(size = 20) 
        
        
        self.fig_circ, self.ax_circ = plt.subplots() # this is for ploting the data stream
        
        
        try:
            self.receive_loop() # when initiated, the it will look for published payload and the nsend it to message processing function for further work
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        
        
        if topic == 'plotting':  # as soon as the topic plotting is received, the payload sent gets written on the circular buffer
            

             

            
            self.client_circ.write(payload["data"]) # this way the circular buffer stores the samples which  is in the form of tuple list
                
            print('update plot at t={}s'.format(payload["time"]))  #receives the last timestamp of every tuple list
            t_, x_ = zip(*self.client_circ.read()) # this unzips the list and creates two tuples, when representing timestamps and other x values
            print(self.client_circ.read())
            self.ax_circ.clear()  # clear operation performed to clear x axis of plotting window  so that it can be updated
                

            self.ax_circ.stem(t_, x_) # stem plot
            self.ax_circ.set_xlim([payload["time"]-2,payload["time"]]) #payloaf["time"] represents the last time stamps, therefore the updated seen would be of every 0.5 seconds on the screen, it would happen simulatanously with plots are drawn
            self.ax_circ.set_ylim([-10, 10]) # just y limit set to 10 as sometimes x values remain low. but for a short routine, the x values would not go much high
            self.fig_circ.canvas.draw()  # update figure
            self.fig_circ.canvas.flush_events() # it makes the matplotlib plot the pending events and update the whole 

            if payload["time"]>=10: # the data streaming limit is set till time stamp reaches 10
                print("Plotting complete")
                self.publish_payload({'loop_time': self.refresh_time}, 'interrupt') # this  carries out the interrupt event and triggers termination of data gneration loop
                input("Press Enter to exit")
            
                self.clean_up()
                sys.exit(0)    

                

        
        if keyboard.is_pressed('l'): # another way of terminating data generation, but it will stop it desired time stamp once the if statement with condition of timestamp >=10 is commented or deleted 
            print("Interrupt sent")
            self.publish_payload({'loop_time': self.refresh_time}, 'interrupt')
            input("Press Enter to exit")
            self.clean_up()
            sys.exit(0)
            
            
        
        
        
    def callloop(self):
        self.publish_payload({'size':self.refresh_time},'request')    # this evokes the request event which triggers the reading of new samples and sending of message payload
        
    


def buff_client(): #initiates the buffclient class 
    BuffClient()


if __name__ == '__main__':
    buff_client()


    