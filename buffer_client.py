import sys
from banyan_base import BanyanBase

import matplotlib.pyplot as plt
import time
import numpy as np



class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient',receive_loop_idle_addition=self.loop,loop_time=0.1)
        
        
        # data creation 
        self.set_subscriber_topic('plotting')
        self.x = 10
        self.clientplot = []
        self.data_size = 20
        self.publish_payload({'data_size':self.data_size},'initiation')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        
        print("this is second")
        plt.ion()
        self.x = payload["data"]
        
        
        plt.plot(self.x)
        
       
        time.sleep(3)
        print("plotting complete")
        
        input('Press enter to exit.')
        self.clean_up()
        sys.exit(0)
    def loop(self):
        
        time.sleep(2)
        print("got in loop first")
        self.set_subscriber_topic('plotting')
        self.publish_payload({'data_size':self.data_size},'initiation')
        print("subscription set again")
        
         
        
          


def buff_client():
    BuffClient()


if __name__ == '__main__':
    buff_client()