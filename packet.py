# DATA_DIVIDE_LENGTH = 32768
DATA_DIVIDE_LENGTH = 32768
DATA_LENGTH = DATA_DIVIDE_LENGTH
PACKET_SIZE = (32 * 1024) + 56


class Packet:
    def __init__(self, list_bytes = None):
        if list_bytes != None:
            self.type = list_bytes[0] >> 4
            self.id = list_bytes[0] & 0xF
            self.sequence = (list_bytes[1] << 8) + list_bytes[2]
            self.length = (list_bytes[3] << 8) + list_bytes[4]
            self.checksum = (list_bytes[5] << 8) + list_bytes[6]
            self.data = list_bytes[7:]
    
    def print_packet_info(self):
        print('type : ')
        print(self.type)
        print('id : ')
        print(self.id)
        print('sequence : ')
        print(self.sequence)
        print('length : ')
        print(self.length)
        print('checksum : ')
        print(self.checksum)
        # print(self.data)
        print()
    
    def combine_rows(self):
        output = []
        row_data = data_divider(self.data,1)
        print()
        output.append(convert_int_to_binary((self.type << 4) + self.id, 1))
        output.append(convert_int_to_binary(self.sequence, 2))
        output.append(convert_int_to_binary(self.length, 2))
        output.append(convert_int_to_binary(self.checksum,2))

        for row in row_data:
            output.append(row)

        return b''.join(output)
        

def MakePackets(int_id, file):
    binary_file = convert_file_to_binary(file)
    remainder = len(binary_file) % DATA_DIVIDE_LENGTH

    data = data_divider(binary_file, DATA_DIVIDE_LENGTH)
    types = get_packet_types(len(data))
    id = get_packet_id(len(data), int_id)
    sequence = get_packet_sequence(len(data))
    length = get_packet_length(len(data), remainder)

    checksum = []
    list_for_csum = []

    for x in range(0,len(data)):
        list_for_csum.append(combine_rows_for_csum(types[x], id[x], sequence[x], length[x], data[x]))
    for lbyte in list_for_csum:
        checksum.append(get_packet_checksum(lbyte))

    packets = []
    for x in range (0,len(data)):
        packets.append(MakePacket(types[x], id[x], sequence[x], length[x], checksum[x], data[x]))
    
    return packets

def MakePacket(type, id, sequence, length, csum, data):
    p = Packet()
    p.type = type
    p.id = id
    p.sequence = sequence
    p.length = length
    p.checksum = csum
    p.data = data
    return p

def combine_rows_for_csum(type, id, sequence, length, data):
    row_data = data_divider(data,1)

    temp = convert_int_to_binary((type << 4) + id, 1)
    temp +=(convert_int_to_binary(sequence, 2))
    temp +=(convert_int_to_binary(length, 2))
    for row in row_data:
        temp += row

    return temp

def convert_file_to_binary(fileName):
    f = open(fileName, 'rb')
    file_content = f.read()
    f.close()
    return file_content

def convert_int_to_binary(x, width):
    return x.to_bytes(width, byteorder='big')

def convert_binary_to_int(bin):
    return int.from_bytes(bin, byteorder='big')

def data_divider(data, width):
    data = [data[i:i + width] for i in range(0, len(data), width)]
    return data

def get_packet_types(len):
    types = []
    for x in range(0, len):
        if (x == len-1): 
            types.append(0x2) #type FIN
        else:
            types.append(0x0) #type DATA
    return types

def get_packet_id(len, int_id):
    list_id = []
    for x in range(0, len):
        list_id.append(int_id)
    return list_id

def get_packet_sequence(len):
    seq = []
    for x in range(0, len):
        seq.append(x+1)
    return seq

def get_packet_length(len, remainder):
    length = []
    for x in range(0, len):
        if (x == len-1):
            length.append(remainder)
        else:
            length.append(DATA_DIVIDE_LENGTH)
    return length

def get_packet_checksum(list_bytes):
    checksum = []
    
    temp = 0
    # print(list_bytes)
    packet_wo_checksum = data_divider(list_bytes, 2)
    # print(packet_wo_checksum)
    # print(packet_wo_checksum)
    for row in packet_wo_checksum:
        # print(x)
        # print("row")
        # print(bin(convert_binary_to_int(row)))
        # if (i < 15):
        #     # print(temp)
        # i += 1
        temp ^= convert_binary_to_int(row)
        
        # print(bin(temp))
    # print()

    checksum = temp
    # checksum.append(temp)
    # print(checksum)

    # print(convert_int_to_binary(checksum[0], 16))
    return checksum

# def add_zero_padding(list_of_bytes):
#     idx = len(list_of_bytes)-1
#     remainder = list_of_bytes[idx] % 2
#     print(remainder)
#     if (remainder != 0):
#         temp = list_of_bytes.pop(idx)
#         print(temp)
#         zeros = convert_int_to_binary(0, remainder)
#         list_of_bytes.append(temp + )

# p = MakePackets(4,"test.txt")
# for a in p :
#     a.print_packet_info()
#     print(a.combine_rows())
#     b = Packet(a.combine_rows())
#     b.print_packet_info()
