import socket
import threading
from packet import *
import os

# HOST ='127.0.0.1'
# PORT = 6134 
TIMED_OUT = 2
int_id =2
package =[]
progressBar = 0
BUFFER = 4096
def sender (host,port,file_name):

    port_int = int(port)
    file_size = os.path.getsize(file_name) 
    package = MakePackets(2,file_name)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for a in package:
            try:
                print('Sending package ...')
                a.print_packet_info()
                # print(a.data)
                s.sendto(a.combine_rows(),0,(host,port_int))
                # if (s.sendto(p,0,(host,port_int))):

                s.settimeout(TIMED_OUT)

                print('Waiting..')
                # data,addr = s.recvfrom(BUFFER)
                print('Sending next package... ')
            except s.timeout :
                print("Sorry... failed to send file")
        


if __name__ == '__main__':
    host = input("Address : ")
    port = input("Port : ")
    n_file = int(input("Jumlah file yang ingin dikirim: "))
    print('Tekan 1 untuk inputan file berupa nama file')
    print('Tekan 2 untuk inputan file berupa path file')

    files=[]
    threads=[]

    if (n_file<=5):
        #threading utk banyak files
        for i in range(n_file):
            jenis = int(input("Nomor"))
            if (jenis ==1):              
                file_name = input("Nama file: ")
                files.append(file_name)
            if (jenis ==2):
                path_file = input('Path file : ')
                file_name = os.path.basename(path_file)
                files.append(file_name)

        for f in files:
            thread = threading.Thread(target=sender, args=(host,port,f))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
    else:
        print("Jumlah file harus kurang dari 5")