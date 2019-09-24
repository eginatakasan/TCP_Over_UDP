import socket

HOST ='127.0.0.1'
PORT = 6134 

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto("halo".encode(),0,(HOST,PORT))

