import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 6231     # Port to listen on (non-privileged ports are > 1023)


def ask_port():
    port = int(input("Masukkan port "))
    return port

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    PORT = ask_port()
    s.bind((HOST, PORT))

    while True:
        data, addr = s.recvfrom(1024)
        print ("Message: ", data)