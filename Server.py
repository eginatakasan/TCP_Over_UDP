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

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    PORT = ask_port()
    s.bind((HOST, PORT))

    while True: 
        data, addr = s.recvfrom(PACKET_SIZE)
        
        p = packet.Packet(data)
        p.print_packet_info()
        
        csums_list = packet.combine_rows_for_csum(p.type, p.id, p.sequence, p.length, p.data)

        if (packet.get_packet_checksum(csums_list)==p.checksum):
            if (p.id in file_id):
                file_id[p.id].write(p.data)
            else:
                file_id[p.id] = open(p.id,'wb')

            if (p.type==2):
                print(file_id[p.id])
                print("finish")

                del file_id[p.id]
        
            p.type+=1
            p_to_send = packet.MakePacket(p.type, p.id, p.sequence, p.length, p.checksum, p.data) 
            s.sendto(p_to_send.combine_rows(), addr)