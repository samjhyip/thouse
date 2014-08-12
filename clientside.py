import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.99', 8000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


def send_emptymessage():

    try:
    
        # Send data
        message = 'Exiting'
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        data = sock.recv(4096)
        print >>sys.stderr, 'received "%s"' % data

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
        
        
list_of_output_pins = []
        
def get_GPIOoutput():

    try:
    
        # Send data
        message = 'xx_gpioout_request'
        #print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        gpiooutputsinuse = sock.recv(4096)
        #print >>sys.stderr, 'received "%s"' %gpiooutputsinuse
        
        #split up all the pins into a list
        #global list_of_output_pins
        list_of_output_pins = gpiooutputsinuse.split()
        

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
        #return list_of_output_pins
        
def ringdoorbell_request():
    try:
    
        # Send data
        message = 'xx_ringdoorbell'
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()    

#get_GPIOoutput()
#ringdoorbell_request()
