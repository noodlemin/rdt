import sys
import socket
import time
import signal
from functools import wraps
import errno
import os

packet_length = 1027

# create packets
def create_packets(file_name, data_length):
    with open(file_name, 'rb') as f:
        try:
            packets = []
            packet = bytearray(packet_length)  
            # sequence number
            seq_num = 0
            # end-of-file flag
            eof = 0     
            data = f.read(data_length)

            while(data):              
                # print(seq_num)  
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
                packets.append(packet[:])
                # print(packets[0][2])
                seq_num += 1
                data = f.read(data_length)
            f.close()                
            # print(packets[0][2])    
            return packets
        except Exception as ex:
            print(ex)         

a = create_packets('test.jpg', packet_length)

# b = int.from_bytes(a[10][:2], byteorder='big')


print(len(a))
print(a[875][2])

l = [12,3,4]
print(1 not in l)