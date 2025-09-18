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
                    compressed.append(127 & 0x7F)  
                    compressed.append(input[i])  
                    count -= 127
                else:
                    compressed.append(count & 0x7F)  
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
            count = compressed[i]  
            i += 1
            if i < n:
                value = compressed[i]  
                decompressed.extend([value] * count)  
                i += 1
    return decompressed

def compress_file_RLE(input_file, output_file):
    with open(input_file, 'rb') as f:
        file = f.read() 
    compressed = rle_compress(file)
    with open(output_file, 'wb') as f:
        f.write(compressed)

def decompress_file_RLE(input_file, output_file):
    with open(input_file, 'rb') as f:
        compressed = f.read()
    decompressed = rle_decompress(compressed)
    with open(output_file, 'wb') as f:
        f.write(decompressed)
        
compress_file_RLE('binary.exe', 'binary_RLEcompressed.exe')
decompress_file_RLE('binary_RLEcompressed.exe', 'binary_RLEdecompressed.exe') 

