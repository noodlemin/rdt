# Minsung Kim s1857642

import sys
import socket
import struct

# data packet length
packet_length = 1027
# save arguments
if len(sys.argv) == 3:
    port = int(sys.argv[1])
    filename = sys.argv[2]
else:    
    sys.exit('Invalid arguments')

# create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to the port
socket.bind(('localhost', port))
# write bytes in filename 
with open(filename, 'wb') as f:
    try:
        # receive data
        packet, addr = socket.recvfrom(packet_length)
        # print('{} is connected'.format(addr))
        # convert sequence number in byte to int
        seq_num = int.from_bytes(packet[:2], byteorder='big')        
        # print('sequence no {} - data length {}'.format(seq_num, len(packet[3:])))
        # end-of-file flag
        eof = packet[2]        
        while 1:          
            # write the received data in filename                  
            f.write(packet[3:])            
            # if eof is up, close the file and the socket
            if eof == 1:
                f.close()
                socket.close() 
                break          
            # receive data
            packet, addr = socket.recvfrom(packet_length)
            # convert sequence number in byte to int
            seq_num = int.from_bytes(packet[:2], byteorder='big')            
            # print('sequence no {} - data length {}'.format(seq_num, len(packet[3:])))
            # end-of-file flag
            eof = packet[2]   
    except Exception as ex:
        print(ex)



