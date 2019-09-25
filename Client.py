import socket
import threading

HOST ='127.0.0.1'
PORT = 6134 

def send():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto("halo".encode(),0,(HOST,PORT))

if __name__ == '__main__':
    n_file = int(input("Jumlah file yang ingin dikirim: "))
    print('Tekan 1 untuk inputan file berupa nama file')
    print('Tekan 2 untuk inputan file berupa path file')

    files=[]
    threads=[]

    if (n<=5):
        #threading utk banyak files
        for i in range n_file:
            jenis = int(input("Nomor"))
            if (jenis ==1):              
                nama_file = input("Nama file: ")
                files.append(file_name)
            if (jenis ==2):
                path_file = input('Path file : ')
                file_name = os.path.basename(path_file)
                files.append(file_name)
        
        for f in range files:
            thread = threading.Thread(target=sender, args=())
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
    else:
        print("Jumlah file harus kurang dari 5")