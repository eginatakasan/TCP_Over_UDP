DATA_DIVIDE_LENGTH = 1024 * 32
DATA_LENGTH = DATA_DIVIDE_LENGTH

def convertBinary(fileName):
    f = open(fileName, 'rb');
    file_content = f.read()
    print(len(data_divider(file_content)))
    f.close()

def data_divider(data):
    data = [data[i:i + DATA_DIVIDE_LENGTH] for i in range(0, len(data), DATA_DIVIDE_LENGTH)]
    data.append("END")
    return data

def packet_type():
    if 

print(convertBinary("a.jpg"))