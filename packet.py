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

    get_packet_checksum(types, id, sequence, length, data)

def convert_file_to_binary(fileName):
    f = open(fileName, 'rb')
    file_content = f.read()
    f.close()
    return file_content

def convert_int_to_binary(x, width):
    input = x
    return bytes((map((int), [x for x in '{:0{size}b}'.format(input,size=width)])))

def convert_binary_to_int(bin):
    return int.from_bytes(bin)

def data_divider(data, width):
    data = [data[i:i + width] for i in range(0, len(data), width)]
    return data


def get_packet_types(len):
    types = []
    for x in range(0, len):
        if (x == len-1): 
            types.append(convert_int_to_binary(0x2, 4)) #type FIN
        else:
            types.append(convert_int_to_binary(0x0, 4)) #type DATA
    return types

def get_packet_id(len, int_id):
    id = convert_int_to_binary(int_id,4)
    list_id = []
    for x in range(0, len):
        list_id.append(id)
    return list_id

def get_packet_sequence(len):
    seq = []
    for x in range(0, len):
        seq.append(convert_int_to_binary(x, 16))
    return seq

def get_packet_length(len, remainder):
    length = []
    for x in range(0, len):
        if (x == len-1):
            length.append(convert_int_to_binary(remainder, 16))
        else:
            length.append(convert_int_to_binary(DATA_DIVIDE_LENGTH, 16))
    return length

def get_packet_checksum(type, id, sequence, length, data):
    checksum = 0
    row_zero_adder = bin([0,0,0,0,0,0,0,0])

    for x in range(0,len(data)):
        first_row = (type[x] + data[x])
        row_sequence = data_divider(sequence[x],1)
        row_length = data_divider(length[x],1)
        row_data = (data_divider(data[x],1))

        checksum ^= first_row
        for row in row_sequence:
            checksum ^= row
        for row in row_length:
            checksum ^= row
        for row in row_data:
            checksum ^= row

    return checksum


MakePacket(4,"a.jpg")
