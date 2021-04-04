# Minsung Kim s1857642

import sys
import socket
# import struct
import time


# data packet length in byte
packet_length = 1027
# save arguments
if len(sys.argv) == 4:
    port = int(sys.argv[1])
    filename = sys.argv[2]
    window_size = int(sys.argv[3])
    if window_size < 0:
        sys.exit('Invalid arguments')    
else:    
    sys.exit('Invalid arguments')


# create socket
socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket3.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# bind the socket to the port
socket4.bind(('localhost', port))
# sequence numbers of recieved packets
seq_nums = []

# eof = 0
base = 0
nextseqnum = window_size
packets = []
# write the file with the recieved packets
with open(filename, 'wb') as f:
    flag = True
    while flag:             
        try:
            # print(len(packets))
            # print(base)
            time.sleep(0.0001)
            window = list(range(base, nextseqnum))
            while window:
                # print(base)
                packet, addr = socket4.recvfrom(packet_length) 
                data = packet[3:]
                # convert sequence number in byte to int
                seq_num = int.from_bytes(packet[:2], byteorder='big')  
                # eof flag
                eof = packet[2] 
                if seq_num in window:
                    window.remove(seq_num)
                    packets.append([seq_num, data])
                    socket4.sendto(seq_num.to_bytes(2, byteorder='big'), addr) 
                if base == seq_num:
                    packets.sort()
                    size = len(packets)
                    for i in packets:
                        f.write(i[1])
                    base += size
                    nextseqnum += size
                    packets = []
                    break
                if seq_num > base - window_size and seq_num < base - 1:
                   socket4.sendto(seq_num.to_bytes(2, byteorder='big'), addr)
                # if eof == 1:
                    
        except Exception as ex:
            print(ex)   
        