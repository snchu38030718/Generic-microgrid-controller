import socket
import array

class Ethernet:
    
    BUF_SIZE = 128
    HOST_IP = ''
    PORT = 45000
    
    
    def __init__(self):
        # Set up socket and bind socket to port and local host IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST_IP, self.PORT))
        
        # Receive first message from microgrid to acquire message identification
        print('Waiting for connection from microgrid...')
        data, self.address = self.s.recvfrom(self.BUF_SIZE)
        print('Connected!')
        self.message_header = data[0:6]
        
        # Close socket to prevent accumulation of data
        self.s.close()
        
    def status(self):
        # Set up socket and bind socket to port and local host IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST_IP, self.PORT))
        
        # Receive latest microgrid data
        data, self.address = self.s.recvfrom(self.BUF_SIZE)
        
        # Rearrange data from bytes into an array
        data_doubles = array.array('d', data)
        
        # Close socket to prevent accumulation of data
        self.s.close()
        return data_doubles[1:]
    
    
    def send(self, commands):  # Why we need commands here? Command is the data from status.
        # Set up socket and bind socket to port and local host IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.HOST_IP, self.PORT))
        
        # Rearrange data from array and include message identification
        #n = len(commands)
        
        message_length = array.array('d', commands) # h represent unsinged short
        message=array.array('d', self.message_header)
        message_to_send = message.append(message_length)
        
        # Send data
        self.s.sendto(bytes(message_to_send), self.address)
        
        # Close socket to prevent accumulation of data
        self.s.close()
