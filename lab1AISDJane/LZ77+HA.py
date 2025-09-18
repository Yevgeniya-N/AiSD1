def LZ77(data, buffer=16):
    i = 0
    n = len(data)
    window_size = 4096
    buffer_size = buffer
    compressed_data = []

    while i < n:
        match_len = 0
        match_pos = 0
        for j in range(max(0, i - window_size), i):
            k = 0
            while k < buffer_size and i + k < n and data[j + k] == data[i + k]:
                k += 1
            if k > match_len:
                match_len = k
                match_pos = i - j
        if match_len >= 2:
            if i + match_len < n:
                compressed_data.append((match_pos, match_len, data[i + match_len]))
                i += match_len + 1
            else:
                compressed_data.append((0, 0, data[i]))
                i += 1
        else:
            compressed_data.append((0, 0, data[i]))
            i += 1
    result = bytearray()
    for pos, length, char in compressed_data:
        result.extend(pos.to_bytes(2, 'big'))
        result.extend(length.to_bytes(2, 'big'))
        result.append(char)
    return bytes(result)


def LZ77_decode(data):
    i = 0
    n = len(data)
    decompressed_data = bytearray()
    while i < n:
        pos = int.from_bytes(data[i:i + 2], 'big')
        length = int.from_bytes(data[i + 2:i + 4], 'big')
        char = data[i + 4]
        if pos == 0 and length == 0:
            decompressed_data.append(char)
        else:
            start = len(decompressed_data) - pos
            for j in range(length):
                decompressed_data.append(decompressed_data[start + j])
            decompressed_data.append(char)
        i += 5
    return bytes(decompressed_data)

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

def LZ77HA_compress(input, output):
    with open(input, 'rb') as file:  
        data = file.read()  
        
    compressed1 = LZ77(data)
    compressed2 = build_huffman_tree(compressed1)
    
    with open(output, 'wb') as file:  
        file.write(compressed2)  
        
def LZ77HA_decompress(input, output):
    with open(input, 'rb') as file:  
        data = file.read()  
        
    decompressed1 = decode_huffman(data)
    decompressed2 = LZ77_decode(decompressed1)
    
    with open(output, 'wb') as file:  
        file.write(decompressed2)  
        

LZ77HA_compress('gray_image.raw', 'gray_image_LZ77HAcompressed.raw')
LZ77HA_decompress('gray_image_LZ77HAcompressed.raw', 'gray_image_LZ77HAdecompressed.raw')  
 
