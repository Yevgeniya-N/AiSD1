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


def HA_compress(input, output):
    with open(input, 'rb') as file:  
        data = file.read()  
        
    compressed = build_huffman_tree(data)
    
    with open(output, 'wb') as file:  
        file.write(compressed)  
        
def HA_decompress(input, output):
    with open(input, 'rb') as file:  
        data = file.read()  
        
    decompressed = decode_huffman(data)
    
    with open(output, 'wb') as file:  
        file.write(decompressed)  
        

HA_compress('blackwhite_image1111.raw', 'BW_HAcompressed_new.raw')
#HA_decompress('BW_HAcompressed.raw', 'BW_HAdecompressed.raw')  


