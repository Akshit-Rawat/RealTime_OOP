import sys
from python_banyan.banyan_base import BanyanBase
import numpy as np
import random
from buffers_1 import CircBuff

class BuffServer(BanyanBase):
    def __init__(self):

        super().__init__(process_name = 'BuffServer',receive_loop_idle_addition=1,loop_time = 0.1)
        
        
        self.set_subscriber_topic('initiation')
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()

    def incoming_message_processing(self, topic, payload):
        buffer_server = CircBuff(10)

        buffer_server.read()
        buffer_server.write()



        
        
        buffer = []
        
        buffer = np.zeros(payload['data_size']) 

        for i in range(len(buffer)):
            buffer[i] = random.randint(0,10)

        data_list = list(buffer)

        payload = {'data':data_list}
        
        self.publish_payload(payload,"plotting")
        print("Data sent")
        print(payload["data"])


def buff_server():
    BuffServer()


if __name__ == '__main__':
    buff_server()





