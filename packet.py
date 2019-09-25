DATA_DIVIDE_LENGTH = 32768
DATA_LENGTH = DATA_DIVIDE_LENGTH

def MakePacket(int_id, file):
    packet = []

    binary_file = convert_file_to_binary(file)
    remainder = len(binary_file) % DATA_DIVIDE_LENGTH

    data = data_divider(binary_file, DATA_DIVIDE_LENGTH)
    types = get_packet_types(len(data))
    id = get_packet_id(len(data), int_id)
    sequence = get_packet_sequence(len(data))
    length = get_packet_length(len(data), remainder)

    list_for_csum = combine_rows_for_csum(types, id, sequence, length, data)
    checksum = get_packet_checksum(len(data), list_for_csum)

    packet = combine_rows(types, id, sequence, length, checksum, data)
    return packet


def combine_rows_for_csum(types, id, sequence, length, data):
    list_bytes = []

    for x in range(0,len(data)):
        row_data = data_divider(data[x],1)

        temp = convert_int_to_binary((types[x] << 4) + id[x], 1)
        temp +=(convert_int_to_binary(sequence[x], 2))
        temp +=(convert_int_to_binary(length[x], 2))
        for row in row_data:
            temp += row
        list_bytes.append(temp)

    return list_bytes

def combine_rows(types, id, sequence, length, csum, data):
    list_bytes = []

    for x in range(0,len(data)):
        row_data = data_divider(data[x],1)

        temp = convert_int_to_binary((types[x] << 4) + id[x], 1)
        temp +=(convert_int_to_binary(sequence[x], 2))
        temp +=(convert_int_to_binary(length[x], 2))
        temp +=(convert_int_to_binary(csum,2))
        for row in row_data:
            temp += row
        list_bytes.append(temp)

    return list_bytes


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

def get_packet_checksum(len, list_bytes):
    checksum = 0
    for x in range (len):
        packet_wo_checksum = data_divider(list_bytes[x], 2)
        print(packet_wo_checksum)
        for row in packet_wo_checksum:
            checksum ^= convert_binary_to_int(row)

    return checksum


print(MakePacket(4,"test.txt"))
