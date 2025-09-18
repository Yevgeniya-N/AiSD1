import math
from collections import Counter

def mtf_encode(block):
    output = []
    seen = []
    for byte in block:
        if byte in seen:
            output.append(seen.index(byte))
            seen.remove(byte)
        else:
            output.append(len(seen))
            seen.append(byte)
    return bytes(output)  

def BWT(block):
    n = len(block)
    table = [block[i:] + block[:i] for i in range(n)]
    table.sort()
    last_column = [row[-1] for row in table]
    suffix_index = table.index(block)  
    return bytes(last_column), suffix_index  

def calculate_entropy(data):
    if not data:
        return 0.0
    frequency = Counter(data)
    total = len(data)
    entropy = -sum((count / total) * math.log2(count / total) for count in frequency.values())
    return entropy

def test_block_sizes(input_file, block_sizes, max_blocks=10):
    results = {}
    
    for block_size in block_sizes:
        total_entropy = 0
        total_blocks = 0
        
        with open(input_file, 'rb') as f:
            while total_blocks < max_blocks:
                block = f.read(block_size)
                if not block:
                    break
                changed_S, S_indx = BWT(block)
                mtf_encoded = mtf_encode(changed_S)
                entropy = calculate_entropy(mtf_encoded)
                total_entropy += entropy
                total_blocks += 1
            average_entropy = total_entropy / total_blocks if total_blocks > 0 else 0
            results[block_size] = average_entropy
            print(f"Размер блока: {block_size} байт, Средняя энтропия: {average_entropy:.4f}")
    
    return results

if __name__ == "__main__":
    input_file = "D:\\Desktop\\lab1AISD\\enwik7.txt" 
    block_sizes = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]  
    results = test_block_sizes(input_file, block_sizes)