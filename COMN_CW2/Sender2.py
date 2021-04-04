# Minsung Kim s1857642

import sys
import socket
import time
import os

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

with open(file_name, 'rb') as f:
    try:            
        # sequence number
        seq_num = 0
        # read data_length bytes from the file         
        data = f.read(data_length)  
        # while there are leftover bytes
        while data:
            # create the packet
            packet = create_packet(data, seq_num)              
            # send the data packet
            socket2.sendto(packet, (remote_host, port))
            # check whether received the ack packet
            ack_check = False
            # stop-and-wait
            while not ack_check:
                try:       
                    # receive the ack packet             
                    ack, addr = socket2.recvfrom(ack_length)
                    # sequence number of the ack packet
                    ack_num = int.from_bytes(ack[:2], byteorder='big')
                    # start measuring the transfer time
                    if ack_num == 0:
                        start = time.time() 
                    # if two sequence numbers are matched
                    if ack_num == seq_num:
                        # ack received
                        ack_check = True
                # if timeout happens, send the packet again and add 1 to retry_num        
                except socket.timeout:                                       
                    socket2.sendto(packet, (remote_host, port))
                    retry_num += 1    
            # total bytes successfully transfered        
            data_transferred += len(data)
            # read the next bytes
            data = f.read(data_length)      
            # next sequence
            seq_num += 1
        # close file                                   
        f.close()
        # close socket
        socket2.close()
    except Exception as ex:
        print(ex) 
        
# stop measuring the transfer time           
end = time.time()
total_time = end - start

# print the retry number and the throughput
print(retry_num, round((os.path.getsize(file_name)/1000)/total_time, 2))
