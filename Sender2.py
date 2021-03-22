# Minsung Kim s1857642

import sys
import socket
import time
# import math


# header length in byte
header_length = 3
# data length in byte
data_length = 1024
# data packet length
packet_length = header_length + data_length
# save arguments
if len(sys.argv) == 5:
    remote_host = sys.argv[1]
    port = int(sys.argv[2])
    file_name = sys.argv[3]
    retry_timeout = sys.argv[4]
else:    
    sys.exit('Invalid arguments')

# timeout in ms
rt_timeout = int(retry_timeout) * 0.001
# create socket
socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# set socket timeout
socket2.settimeout(rt_timeout)
# count the amount of the data transferred
data_transferred = 0
# retrasmission number
retry_num = 0
# ack length
ack_length = 2

# create packets
def create_packet(data, seq_num):
    # end-of-file flag
    eof = 0
    # create the packet_length-long bytearray 
    packet = bytearray(packet_length)               
    # if there are less than data_length data, eof is up
    if len(data) < data_length:                  
        eof = 1
    # sequence number converted to bytes 
    # and saved in the first 2 bytes of the packet
    packet[0:2] = seq_num.to_bytes(2, byteorder='big')      
    # save eof flag in the 3rd byte of the packet
    # don't need to convert int to byte if it is byte-long
    packet[2] = eof  
    # data saved in the rest of the packet
    packet[3:] = data                
    return packet

# total_f = 0

with open(file_name, 'rb') as f:
    try:            
        # create the packet_length-long bytearray 
        # packet = bytearray(packet_length)  
        # sequence number
        seq_num = 0
        # end-of-file flag 
        data = f.read(data_length)
        total_time = 0    
        while data:
            packet = create_packet(data, seq_num)               
            socket2.sendto(packet, (remote_host, port))                     
            start = time.time()
            ack_check = False
            while not ack_check:
                try:                    
                    ack, addr = socket2.recvfrom(ack_length)
                    end = time.time()
                    total = end - start
                    ack_num = int.from_bytes(ack[:2], byteorder='big')
                    if ack_num == seq_num:
                        total_time += total
                        # total_f += total
                        ack_check = True
                except socket.timeout:                                       
                    socket2.sendto(packet, (remote_host, port))
                    retry_num += 1    
            data_transferred += len(data)           
            data = f.read(data_length)      
            seq_num += 1  
        # close file                                   
        f.close()
        # close socket
        socket2.close()
    except Exception as ex:
        print(ex)    

# print("Transfer finished %s, file length %d" %(file_name, data_transferred))
print(retry_num, round((data_transferred/1000)/total_time, 2))
# print(total_time)
