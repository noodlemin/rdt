# Minsung Kim s1857642

import sys
import socket
# import struct
# import time


# data packet length in byte
packet_length = 1027
# ack packet length in byte
ack_length = 2
# save arguments
if len(sys.argv) == 3:
    port = int(sys.argv[1])
    filename = sys.argv[2]
else:    
    sys.exit('Invalid arguments')

# create socket
socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket2.settimeout()
# bind the socket to the port
socket2.bind(('localhost', port))
# ack number
ack_num = 0
# sequence numbers of recieved packets

# create the packet_length-long bytearray 
# ack = bytearray(ack_length)
# write bytes in filename 
seq_nums = []
# i = 0
# while i < 5:
with open(filename, 'wb') as f:
    while 1:             
        try:
            # receive data
            packet, addr = socket2.recvfrom(packet_length)
            # print('{} is connected'.format(addr))
            # send ack
            socket2.sendto(packet[:2], addr)
            # convert sequence number in byte to int
            seq_num = int.from_bytes(packet[:2], byteorder='big')
            # end-of-file flag
            eof = packet[2]        
            # i = 0                        
            # seq_nums.append(seq_num)
            # write the received data in filename                                 
            if (seq_num not in seq_nums):
                seq_nums.append(seq_num)
                print('sequence no {} - data length {}'.format(seq_num, len(packet[3:]))) 
                f.write(packet[3:])
            if eof == 1:
                # print(i)
                f.close()
                socket2.close() 
                # i += 1
                break                                         
        except Exception as ex:
            print(ex)
                          
            # eof = packet[2]  
        # if eof is up, close the file and the socket
        
    
    # print(seq_nums)                  
        # # receive data
        # packet, addr = socket.recvfrom(packet_length)            
        # # convert sequence number in byte to int
        # seq_num = int.from_bytes(packet[:2], byteorder='big')          
        # receive data
        # packet, addr = socket2.recvfrom(packet_length)            
        # convert sequence number in byte to int
        # seq_num = int.from_bytes(packet[:2], byteorder='big')
        # # print(seq_num in seq_nums)            
        # socket2.sendto(packet[:2], addr)                    
        # print('sequence no {} - data length {}'.format(seq_num, len(packet[3:])))
        # end-of-file flag
        # eof = packet[2]                            
        
       


