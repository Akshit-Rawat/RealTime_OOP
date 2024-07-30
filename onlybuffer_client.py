import sys
from python_banyan.banyan_base import BanyanBase

import matplotlib.pyplot as plt
from buffers_1 import CircBuff



class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient',receive_loop_idle_addition=None)
        
        
        # data creation 
        self.set_subscriber_topic('plotting')
        self.buffclient = CircBuff(10)
        self.clientplot = []
        self.data_size = 10
        self.publish_payload({'data_size':self.data_size},'initiation')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        
        plt.ion()
        x = payload['data']
        plt.plot(x)
        
    
        
        
        #input('Press enter to exit.')
        #self.clean_up()
        #sys.exit(0) 
    
    
def buff_client():
    BuffClient()


if __name__ == '__main__':
    buff_client()