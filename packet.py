DATA_DIVIDE_LENGTH = 32768
DATA_LENGTH = DATA_DIVIDE_LENGTH

def MakePacket(int_id, file):
    packet = []

    binary_file = convertBinary(file)
    remainder = len(binary_file) % DATA_DIVIDE_LENGTH
    data = data_divider(binary_file)

    types = get_packet_types(len(data))
    id = get_packet_id(len(data), int_id)
    
    sequence = get_packet_sequence(len(data))
    length = get_packet_length(len(data), remainder)

    print("types:")
    print (types)
    print("id:")
    print(id)
    print("sequence:")
    print (sequence)
    print("length:")
    print (length)
    print("data index-4:")
    print(data[4])

def convertBinary(fileName):
    f = open(fileName, 'rb')
    file_content = f.read()
    f.close()
    return file_content

def data_divider(data):
    data = [data[i:i + DATA_DIVIDE_LENGTH] for i in range(0, len(data), DATA_DIVIDE_LENGTH)]
    return data

def convert_int_to_binary(x, width):
    input = x
    return bytes((map((int), [x for x in '{:0{size}b}'.format(input,size=width)])))

def print_iterator(it):
    output = []
    for x in it:
        print(x)

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
    print()

MakePacket(4,"a.jpg")