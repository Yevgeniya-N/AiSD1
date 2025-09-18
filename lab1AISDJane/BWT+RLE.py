def BWT(data):
    n = len(data)
    table = sorted(data[i:] + data[:i] for i in range(n))
    last_column = bytearray(row[-1] for row in table)
    suffix_index = table.index(data)
    return last_column, suffix_index

def iBWT(bwt_bytes, suffix_index):
    n = len(bwt_bytes)
    count = [0] * 256  
    
    for byte in bwt_bytes:
        count[byte] += 1

    for i in range(1, 256):
        count[i] += count[i - 1]
    next_index = [0] * n
    for i in range(n - 1, -1, -1):
        byte = bwt_bytes[i]
        count[byte] -= 1
        next_index[count[byte]] = i
    original = bytearray(n)
    current_index = suffix_index
    for i in range(n):
        original[i] = bwt_bytes[current_index]
        current_index = next_index[current_index]

    return original


def rle_compress(input):
    compressed = bytearray()
    n = len(input)
    i = 0

    while i < n:
        count = 1
        while i + 1 < n and input[i] == input[i + 1]:
            count += 1
            i += 1
        if count > 1:
            while count > 0:
                if count > 127:
                    compressed.append(127)  
                    compressed.append(input[i])  
                    count -= 127
                else:
                    compressed.append(count)  
                    compressed.append(input[i])  
                    count = 0  
        else:
            start = i
            while i + 1 < n and input[i] != input[i + 1]:
                i += 1
            
            count1 = i - start + 1  
            
            while count1 > 0:
                if count1 > 127:
                    compressed.append(0x80 | 127)  
                    compressed.extend(input[start:start + 127])  
                    start += 127
                    count1 -= 127
                else:
                    compressed.append(0x80 | count1)  
                    compressed.extend(input[start:start + count1])  
                    count1 = 0  
        
        i += 1  

    return compressed

def rle_decompress(compressed):
    decompressed = bytearray()
    n = len(compressed)
    i = 0

    while i < n:
        if compressed[i] & 0x80:  
            count = compressed[i] & 0x7F  
            i += 1
            
            for _ in range(count):
                if i < n:
                    decompressed.append(compressed[i])
                    i += 1
                else:
                    print("Данные находятся за пределами сжатых данных")
                    break
        else:  
            count = compressed[i]  
            i += 1
            if i < n:
                value = compressed[i]  
                decompressed.extend([value] * count)  
                i += 1
            else:
                print("Данные находятся за пределами сжатых данных")
                break

    return decompressed

def process_file_in_blocks(input_file, output_file, block_size):
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while True:
            block = infile.read(block_size)
            if not block:
                break  
            bwt_bytes, suffix_index = BWT(block)
            compressed = rle_compress(bwt_bytes)
            outfile.write(compressed)
            outfile.write(suffix_index.to_bytes(4, 'little'))  


def compress_file_BWT_RLE(input_file, output_file, block_size=5000):
    with open(input_file, 'rb') as f:
        with open(output_file, 'ab') as out_f:
            while True:
                block = f.read(block_size)
                if not block:
                    break
                changed_S, S_indx = BWT(block)
                compressed = rle_compress(changed_S)
                block_length = len(compressed) + 8  
                out_f.write(block_length.to_bytes(4, byteorder='big'))
                out_f.write(S_indx.to_bytes(4, byteorder='big'))
                out_f.write(compressed)

def decompress_file_RLE_BWT(input_file, output_file):
    with open(input_file, 'rb') as f:
        with open(output_file, 'wb') as out_f:
            while True:
                block_length_bytes = f.read(4)
                if not block_length_bytes:
                    break
                block_length = int.from_bytes(block_length_bytes, byteorder='big')
                S_indx = int.from_bytes(f.read(4), byteorder='big')  
                compressed_data = f.read(block_length - 8)  
                rle_data = compressed_data
                bwt_data = rle_decompress(rle_data)
                original_data = iBWT(bwt_data, S_indx)
                out_f.write(original_data)
                

compress_file_BWT_RLE('enwik7.txt', 'enwik7_compressed_BWT_RLE.bin')
#decompress_file_RLE_BWT('BW_compressed_BWT_RLE.txt', 'BW_decompressed_BWT_RLE.txt')



