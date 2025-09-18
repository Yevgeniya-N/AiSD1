def BWT(data_block):
    n = len(data_block)
    table = sorted(data_block[i:] + data_block[:i] for i in range(n))
    last_column = bytearray(row[-1] for row in table)
    suffix_index = table.index(data_block)
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

def compressBWT_in_blocks(input_data, block_size):
    compressed_data = bytearray()
    indices = []
    
    for i in range(0, len(input_data), block_size):
        data_block = input_data[i:i + block_size]
        bwt_result, suffix_index = BWT(data_block)
        compressed_data.extend(bwt_result)
        indices.append(suffix_index)

    return compressed_data, indices

def decompressBWT_in_blocks(compressed_data, indices, block_size):
    original_data = bytearray()
    
    start = 0
    for suffix_index in indices:
        end = start + block_size
        bwt_block = compressed_data[start:end]
        original_block = iBWT(bwt_block, suffix_index)
        original_data.extend(original_block)
        start += block_size

    return original_data


