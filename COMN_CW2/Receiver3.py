# Minsung Kim s1857642

import sys
import socket
# import struct
import time


# data packet length in byte
packet_length = 1027
# save arguments
if len(sys.argv) == 3:
    port = int(sys.argv[1])
    filename = sys.argv[2]
else:    
    sys.exit('Invalid arguments')


# create socket
socket3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket3.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# bind the socket to the port
socket3.bind(('localhost', port))
# sequence numbers of recieved packets
seq_nums = []
ack = 0

# write the file with the recieved packets
with open(filename, 'wb') as f:
    while 1:             
        try:
            time.sleep(0.0001)
            # receive data. otherwise close 
            try:
                packet, addr = socket3.recvfrom(packet_length)
            except:
                f.close()
                socket3.close()
                break                                         
            # convert sequence number in byte to int
            seq_num = int.from_bytes(packet[:2], byteorder='big')         
            # send the ack packet
            socket3.sendto(ack.to_bytes(2, byteorder='big'), addr)                  
            # end-of-file flag
            eof = packet[2]
            # write the received data in filename if seq_num is not in the list and ack number is same as seq_num                                          
            if (seq_num not in seq_nums) and (ack == seq_num):   
                ack += 1     
                seq_nums.append(seq_num)        
                # print('sequence no {} - data length {}'.format(ack, len(packet[3:]))) 
                f.write(packet[3:])                
                # close the file and the socket when the eof is up
                if eof == 1:
                    # socket3.sendto((ack).to_bytes(2, byteorder='big'), addr)                
                    f.close()
                    socket3.close()                 
                    break                              
        except Exception as ex:
            print(ex)
        
