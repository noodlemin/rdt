# Minsung Kim s1857642

import sys
import socket
import time
import threading
import math
import os

# header length in byte
header_length = 3
# data length in byte
data_length = 1024
# data packet length
packet_length = header_length + data_length
# save arguments
if len(sys.argv) == 6:
    remote_host = sys.argv[1]
    port = int(sys.argv[2])
    file_name = sys.argv[3]
    retry_timeout = int(sys.argv[4])
    window_size = int(sys.argv[5])
    if window_size < 0:
        sys.exit('Invalid window size')    
else:    
    sys.exit('Invalid arguments')


# timeout in ms
rt_timeout = retry_timeout * 0.001
# create socket
socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_addr = (remote_host, port)
# next sequence number
nextseqnum = 0
# ack length
ack_length = 2
# lock
lock = threading.Lock()
# packets
packets = []
# total trasfer time
total_time = 0

# create packets
def create_packet(data, seq_num):
    global packet_length
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

# oper the file and save packets
# f = open(file_name, 'rb')
# oper the file and save packets
with open(file_name, 'rb') as f:
    seq_num = 0
    data = f.read(data_length) 
    try:
        while data:
            packets.append(create_packet(data, seq_num))
            seq_num += 1
            data = f.read(data_length)
        f.close()
    except Exception as ex:
        print(ex)
# timer flag for timeout 
start_timer = 0
# start time for timeout
s_time = 0
start = 0
base =  0
packet_num = math.ceil(os.path.getsize(file_name)/data_length)

recved_ack = []
# receiver 
def recver(sock):
    global nextseqnum
    global base
    global start_timer
    global s_time
    global start
    global recved_ack

    # runs until
    while base < packet_num:
        # run
        time.sleep(0.0001)                 
        # receive the ack packet from Receiver
        packet, _ = sock.recvfrom(ack_length)
        # number of ack
        ack = int.from_bytes(packet[:2], byteorder='big')
        # lock the thread when we need to change variables    
        lock.acquire()
        recved_ack.append(ack)
        # for throughput
        if ack == 0:
            start = time.time()
        # print throughput at the end of ack packet
        if ack == packet_num -1:
            end = time.time()
            total_time = end - start            
            file_size = os.path.getsize(file_name)/1000
            print(round(file_size/total_time, 2))    
        # move base
        base = ack + 1        
        # nothing to send yet
        if base == nextseqnum:            
            start_timer = 0  
        # timer flag on           
        else:
            s_time = time.time()                
            start_timer = 1
        # release the thread after change the variables
        lock.release() 
    
# rt = 0
def sender(sock):
    global nextseqnum    
    global start_timer
    global s_time
    global packets
    # run until
    while base < packet_num:
        # print(nextseqnum)
        # run 
        time.sleep(0.00001)
        # send packets until reaches to the window size
        if nextseqnum < base + window_size:
            # don't send if nextseqnum is over than the packet size            
            if nextseqnum < len(packets):    
                sock.sendto(packets[nextseqnum], recv_addr)
            # to change variables               
            lock.acquire()
            # sent packets, start timer
            if base == nextseqnum:
                s_time = time.time()
                start_timer = 1
            # move right-end of window
            nextseqnum += 1
            lock.release()
            
        time.sleep(0.0001)        
        # timeout happening
        if (time.time() - s_time > rt_timeout) and start_timer:    
            lock.acquire()
            # start timer
            s_time = time.time()
            start_timer = 1    
            lock.release()
            # send         
            for i in range(window_size):
                if (base + i - 1 < packet_num) and (base+i-1 not in recved_ack):
                    temp = packets[base+i-1]
                    sock.sendto(temp, recv_addr)

    # close the socket
    sock.close()
        
# make threads and start        
sender_thread = threading.Thread(target=sender, args=(socket4,))
recver_thread = threading.Thread(target=recver, args=(socket4,))
sender_thread.start()
recver_thread.start()
