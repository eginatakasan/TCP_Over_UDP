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
    return int.from_bytes(bin, byteorder='big')

def data_divider(data, width):
    data = [data[i:i + width] for i in range(0, len(data), width)]
    return data

# def fix_size(x, width):
    

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
        seq.append(x)
    return seq

def get_packet_length(len, remainder):
    length = []
    for x in range(0, len):
        if (x == len-1):
            length.append(remainder)
        else:
            length.append(DATA_DIVIDE_LENGTH)
    return length

def get_packet_checksum(type, id, sequence, length, data):
    checksum = 0
    list_bytes = []

    for x in range(0,len(data)):
        first_row = (type[x] << 4) + id[x]
        row_sequence = sequence
        row_length = length
        row_data = data_divider(data[x],1)

        temp = (convert_int_to_binary((type[x] << 4) + id[x], 8))
        temp +=(convert_int_to_binary(sequence[x], 16))
        temp +=(convert_int_to_binary(length[x], 16))
        for row in row_data:
            temp += row
        list_bytes.append(temp)

        data_divider(list_bytes, 8)

    #     checksum ^= first_row
    #     for row in row_sequence:
    #         checksum ^= row
    #     for row in row_length:
    #         checksum ^= row
    #     for row in row_data:
    #         checksum ^= convert_binary_to_int(row)
    # print(checksum)

    # return checksum


MakePacket(4,"a.jpg")
