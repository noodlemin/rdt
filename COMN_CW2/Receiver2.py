# Minsung Kim s1857642

import sys
import socket
# import struct
# import time


# data packet length in byte
packet_length = 1027
# save arguments
if len(sys.argv) == 3:
    port = int(sys.argv[1])
    filename = sys.argv[2]
else:    
    sys.exit('Invalid arguments')

# create socket
socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to the port
socket2.bind(('localhost', port))
# sequence numbers of recieved packets
seq_nums = []
ack = 0

# write the file with the recieved packets
with open(filename, 'wb') as f:
    while 1:             
        try:
            # receive data
            packet, addr = socket2.recvfrom(packet_length)
            # send the ack packet
            socket2.sendto(packet[:2], addr)
            # convert sequence number in byte to int
            seq_num = int.from_bytes(packet[:2], byteorder='big')
            # end-of-file flag
            eof = packet[2]
            # write the received data in filename if seq_num is not in the list                               
            if (seq_num not in seq_nums) and ack == seq_num:                           
                seq_nums.append(seq_num)
                # print('sequence no {} - data length {}'.format(seq_num, len(packet[3:]))) 
                f.write(packet[3:])
                ack += 1
            # close the file and the socket when the eof is up
            if eof == 1:                
                f.close()
                socket2.close()                 
                break                              
        except Exception as ex:
            print(ex)
        
