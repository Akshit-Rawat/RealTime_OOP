import sys
from python_banyan.banyan_base import BanyanBase

class EchoServer(BanyanBase):
    def __init__(self,):
        super(EchoServer,self).__init__(process_name='EchoServer')

        
        self.set_subscriber_topic("echo")
        
        try:
            self.receive_loop()
            
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit()


    def incoming_message_processing(self, topic, payload):
        
        
        
        
        if payload["clientID"]>=0:
            self.publish_payload(payload,"reply")
            print("Client ID :",payload["clientID"])
            print("Message number :",payload["message_number"])
        
        

            
        
        
        
def echo_sever():
    EchoServer()
   
   



if __name__ == '__main__':
    echo_sever()               
