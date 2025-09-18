import numpy as np
from collections import Counter, deque
import heapq
import os

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

def MTF(data):
    alphabet = [_ for _ in range(256)]
    new_d = []
    for byte in data:
        index = alphabet.index(byte)
        new_d.append(index)
        alphabet = [alphabet[index]] + alphabet[:index] + alphabet[index + 1:]
    return bytes(new_d)


def MTF_decode(c_data):
    alphabet = [_ for _ in range(256)]
    original = []
    for i in c_data:
        byte = alphabet[i]
        original.append(byte)
        alphabet = [alphabet[i]] + alphabet[:i] + alphabet[i + 1:]
    return bytes(original) 

class TreeNode():
    def __init__(self, char=None, freq=None, left_child=None, right_child=None, parent_node=None):
        self.char = char
        self.freq = freq
        self.left_child = left_child
        self.right_child = right_child


def build_huffman_tree(input_data):
    frequency_map = {}
    for character in input_data:
        if character in frequency_map:
            frequency_map[character] += 1
        else:
            frequency_map[character] = 1
    node_list = [TreeNode(char, freq) for char, freq in frequency_map.items()]
    
    while len(node_list) > 1:
        node_list.sort(key=lambda node: node.freq)
        first_node = node_list.pop(0)
        second_node = node_list.pop(0)
        parent_node = TreeNode(None, first_node.freq + second_node.freq, first_node, second_node)
        node_list.append(parent_node)
    
    root_node = node_list[0]
    huffman_codes = generate_huffman_codes(root_node)
    encoded_string = create_encoded_string(input_data, huffman_codes)
    
    padding_size = 8 - len(encoded_string) % 8
    encoded_string += padding_size * "0"
    
    byte_array = b""
    for i in range(0, len(encoded_string), 8):
        segment = encoded_string[i:i + 8]
        byte_value = binary_string_to_integer(segment)
        byte_array += byte_value.to_bytes(1, "big")

    metadata_bytes = b""
    for char in frequency_map:
        metadata_bytes += char.to_bytes(1, "big")
        metadata_bytes += frequency_map[char].to_bytes(3, "big")
        
    final_output = len(frequency_map).to_bytes(2, "big") + metadata_bytes + byte_array + (8 - padding_size).to_bytes(1, "big")
    return final_output


def generate_huffman_codes(node):
    code_dict = {}

    def traverse_tree(current_node, current_code=""):
        if current_node is not None:
            if current_node.char is not None:
                code_dict[current_node.char] = current_code
            traverse_tree(current_node.left_child, current_code + "0")
            traverse_tree(current_node.right_child, current_code + "1")

    traverse_tree(node)
    return code_dict


def create_encoded_string(data, codes):
    encoded_result = ""
    for character in data:
        encoded_result += codes[character]
    return encoded_result


def binary_string_to_integer(binary_str):
    value = 0
    for index in range(8):
        if binary_str[index] == "1":
            value += 2 ** (7 - index)
    return value


def decode_huffman(encoded_data):
    decoded_output = bytearray()
    
    letter_count = int.from_bytes(encoded_data[:2], "big")
    frequency_map = {}
    
    index = 2
    while index < letter_count * 4 + 2:
        frequency_map[encoded_data[index]] = int.from_bytes(encoded_data[index + 1:index + 4], "big")
        index += 4

    node_list = [TreeNode(char, freq) for char, freq in frequency_map.items()]
    
    while len(node_list) > 1:
        node_list.sort(key=lambda node: node.freq)
        first_node = node_list.pop(0)
        second_node = node_list.pop(0)
        parent_node = TreeNode(None, first_node.freq + second_node.freq, first_node, second_node)
        node_list.append(parent_node)

    root_node = node_list[0]
    huffman_codes_dict = generate_huffman_codes(root_node)

    padding_value = encoded_data[-1]
    
    binary_representation = ""
    
    for j in range(index, len(encoded_data[:-2])):
        binary_representation += format(encoded_data[j], '08b')
        
    binary_representation += format(encoded_data[j + 1], '08b')[:padding_value]

    i_position = 0
    current_word = ''
    
    while i_position < len(binary_representation):
        current_word += binary_representation[i_position]
        
        if current_word in huffman_codes_dict.values():
            for key in huffman_codes_dict:
                if huffman_codes_dict[key] == current_word:
                    decoded_output.append(key)
                    break
            current_word = ''
        
        i_position += 1
        
    return decoded_output

def compress_BWT_MTF_HA(input, output, block_size):
    with open(input, 'rb') as file:  
        data = file.read() 
    compressed_data, indices = compressBWT_in_blocks(data, block_size)
    mtf_result = MTF(compressed_data)
    huffman_encoded = build_huffman_tree(mtf_result)
    with open(output, 'wb') as file:  
        file.write(huffman_encoded)  
    return huffman_encoded, indices

def decompress(compressed_data, indices, block_size, output):
    mtf_result = decode_huffman(compressed_data)
    decompressed_mtf_result = MTF_decode(mtf_result)
    original_data = decompressBWT_in_blocks(decompressed_mtf_result, indices, block_size)
    with open(output, 'wb') as file:  
        file.write(original_data)  
    return original_data

block_size = 5000
compressed, indices = compress_BWT_MTF_HA('binary.exe', 'binary(BWT_MTF_HA)compr.exe', block_size)
original = decompress(compressed, indices, block_size, 'binary(BWT_MTF_HA)decompr.exe')   


