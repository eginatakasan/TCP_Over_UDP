import socket
import threading
import packet

PACKET_SIZE = (32 * 1024) + 56

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 6231     # Port to listen on (non-privileged ports are > 1023)


file_id = dict()
def ask_port():
    port = int(input("Masukkan port: "))
    return port

def receive():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        PORT = ask_port()
        s.bind((HOST, PORT))

        while True: 
            data, addr = s.recvfrom(PACKET_SIZE)
            
            p = packet.Packet(data)
            
            csums_list = packet.combine_rows_for_csum(p.type, p.id, p.sequence, p.length, p.data)

            if (packet.get_packet_checksum(csums_list)==p.checksum):
                if (p.id in file_id):
                    # file_id[p.id].write(p.data)
                    print('a')
                else:
                    file_name = 'output' + str(p.id) + '.txt'
                    file_id[p.id] = open(file_name,'wb')
                
                file_id[p.id].write(p.data)
                file_id[p.id].flush()

                if (p.type==2):
                    file_name = 'output' + str(p.id) + '.txt'

                    printFileByteContent(file_name)
                    print("finish")

                    del file_id[p.id]
            
                p.type+=1
                p_to_send = packet.MakePacket(p.type,0,0,0,0, {}) 
                s.sendto(p_to_send.combine_rows(), addr)

def printFileByteContent(fileName):
    f = open(fileName, 'rb')
    f.seek(0)
    print(f.read())
    f.close()
    # return file_content

if __name__=='__main__':
    threads = []
    thread = threading.Thread(target=receive, args=())
    thread.start()
    threads.append(thread)

    for t in threads:
        t.join()