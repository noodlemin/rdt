# Minsung Kim s1857642

import sys
import socket
import struct

# header length in byte
header_length = 3
# data size in byte
data_length = 1024
# packet size
packet_length = header_length + data_length
# save arguments
if len(sys.argv) == 4:
    remote_host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
else:    
    sys.exit('Invalid arguments')

# create UDP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket.connect((remote_host, port))
# socket.sendto("hello".encode(), (remote_host, port))

# count the amount of the data
data_transferred = 0
# sequence number
seq_num = 0
# end-of-file flag
eof = 0     

# create the packet_length-long bytearray 
packet = bytearray(packet_length)
# read the file with binary format
with open(filename, 'rb') as f:
    try:
        # read data_length bytes 
        data = f.read(data_length)           
        while data: # until there are data                 
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
            # send the packet to the reciever
            socket.sendto(packet, (remote_host, port))
            # save the length of the data sent
            data_transferred += len(data)
            # read data_length bytes
            data = f.read(data_length)
            # count the sequence number
            seq_num += 1
    except Exception as ex:
        print(ex)

print("Transfer finished %s, file length %d" %(filename, data_transferred))
# close the socket
socket.close()


# struct method with format
# print(type(eof))
# socket.close()
# header
# fmt = '>2I 1I'
# packer = struct.Struct(fmt)
# packet[2] = 128
# print(packet)
# print((eof.to_bytes(1, byteorder='big')))
# packet = packer.pack(*values)       