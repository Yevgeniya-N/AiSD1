from PIL import Image
import numpy as np

def convert_image_to_raw(image_path):
    img = Image.open(image_path)
    bw_img = img.convert('L') 
    image_bytes = bw_img.tobytes()
    (height, width) = bw_img.size
    bw_bytes = bytearray()
    for byte in image_bytes:
        if byte >= 128:
            bw_bytes.append(255)
        else:
            bw_bytes.append(0)
            
    return bytes(bw_bytes)

def save_raw_to_file(raw_data, output_file_path):
    with open(output_file_path, 'wb') as f:
        f.write(raw_data)

image_path = 'D:\\Desktop\\lab1AISD\\blackwhite_image.jpg'  
output_file_path = 'D:\\Desktop\\lab1AISD\\blackwhite_image1111.raw'  

raw_data = convert_image_to_raw(image_path)
save_raw_to_file(raw_data, output_file_path)

print(f"Данные записаны в {output_file_path}")
 

