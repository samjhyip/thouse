import socket
import sys
from variables import *

import index as index
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Gets native IP automatically
def get_local_ip():
    hostname = socket.gethostname()
    address = socket.gethostbyname("%s.local" % hostname)
    addr = address
    return str(addr)


    
# Bind the socket to the port
server_address = (get_local_ip(), 8000)


class ListeningServer(object):

    def start_listening(self):
        print >>sys.stderr, 't.H.O.U.S.E is also listening for external commands on %s port %s' % server_address
        sock.bind(server_address)
    
        self.server_still_listening = True
    
    
    
        # Listen for 1 incoming connections
        sock.listen(1)


        while self.server_still_listening:
        
            if self.server_still_listening is True:

                try:
                    # Wait for a connection
                    print >>sys.stderr, 'waiting for a connection'
                    self.connection, self.client_address = sock.accept()
        
                except socket.timeout:
                    if not server_still_listening:
                        raise sock.error
                
        
                print >>sys.stderr, 'connection from', self.client_address

                
                
                # Receive the data in small chunks and retransmit it
                while True:
                    data_received = self.connection.recv(4096)
           
                    print >>sys.stderr, 'Received "%s"' %(data_received)
            
            
            
            
                    #if there is data, DATA==True
                    if data_received:
                        #print >>sys.stderr, 'sending data back to the client'
                        #connection.sendall(data)
                
                
                        if data_received == 'xx_gpioout_request':
                            stringofoutputpins = ''
                            for eachgpioput in pins_to_use:
                                stringofoutputpins = stringofoutputpins + ' ' + str(eachgpioput)
                            #to remove the space in front
                            stringofoutputpins = stringofoutputpins[1:]
                            self.connection.sendall(stringofoutputpins)
                            
                        if data_received == 'xx_ringdoorbell':
                            index.switch_on_off('doorBell')
                            time.sleep(2) #wait for 2 seconds
                            index.switch_on_off('doorBell')
                
                        if 'xx_toggleswitch' in data_received:
                            split_data = data_received.split()
                            pinno_received = split_data[1]
                            index.switch_on_off(str(index.list_name_from_pin(int(pinno_received))))
                
                
                
                    else:
                        print >>sys.stderr, 'no more data from', self.client_address
                        break
                        #wait for connection again
            
            else:
            
                #Clean up the connection
                self.connection.close()
                print "Listening Server is stopping"
                break
            
        

          
    def stop_listening(self):
        self.server_still_listening = False
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((get_local_ip(), 8000))
        self.connection.close()
        
        

