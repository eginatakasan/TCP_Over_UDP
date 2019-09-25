DATA_DIVIDE_LENGTH = 1024 * 32
DATA_LENGTH = DATA_DIVIDE_LENGTH

def MakePacket(id, file):
    packet = []

    data = convertBinary(file)
    types = get_packet_types(len(data))
    
    sequence = []


def convertBinary(fileName):
    f = open(fileName, 'rb')
    file_content = f.read()
    f.close()
    return file_content

def data_divider(data):
    data = [data[i:i + DATA_DIVIDE_LENGTH] for i in range(0, len(data), DATA_DIVIDE_LENGTH)]
    data.append("END")
    return data

def get_packet_types(len):
    types = []
    for x in range(0, len):
        if (x == len-1): 
            types.append(bin(0x2)) #type FIN
        else:
            types.append(bin(0x0)) #type DATA
    return types

def get_packet_sequence(len):
    seq = []
    for x in range(0, len):
        seq.append(x)
    return seq
