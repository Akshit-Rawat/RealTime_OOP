import sys
from python_banyan.banyan_base import BanyanBase

import matplotlib.pyplot as plt



class BuffClient(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffClient')
        
        
        # data creation 
        self.set_subscriber_topic('plotting')
        
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
        print("plotting complete")
        input('Press enter to exit.')
        self.clean_up()
        sys.exit(0)


def buff_client():
    BuffClient()


if __name__ == '__main__':
    buff_client()