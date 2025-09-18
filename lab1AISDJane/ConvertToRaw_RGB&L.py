from PIL import Image
import struct
import numpy as np

def ConvertToRaw(in_image, out_image):
    with Image.open(in_image) as img:
        img.load()
        (width, height) = img.size
        color_mode = img.mode
        header = struct.pack('II', width, height)
        if color_mode == 'L': 
            print("Mode = L")
            header += b'GRY'
            pixels = np.zeros((height, width), dtype=np.uint8)
            for y in range(height):
                for x in range(width):
                    pixel = img.getpixel((x, y))
                    pixels[y, x] = pixel  
            pixels_raw = pixels.tobytes()
        elif color_mode == 'RGB':  
            print("Mode = RGB")
            header += b'RGB'
            pixels = np.zeros((height, width, 3), dtype=np.uint8)
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    pixels[y, x] = (r, g, b)
            pixels_raw = pixels.tobytes()
        else:
            raise ValueError(f"Неподдерживаемый цветовой режим изображения: {color_mode}")

        with open(out_image, 'wb') as raw_img:
            raw_img.write(header)
            raw_img.write(pixels_raw)

    return out_image

def ConvertFromRaw(in_image, out_image):
    with open(in_image, 'rb') as raw_img:
        header = raw_img.read(8)
        width, height = struct.unpack('II', header)
        
        image_type = raw_img.read(3)
        if image_type == b'GRY':
            color_mode = 'L'
            pixels = np.frombuffer(raw_img.read(), dtype=np.uint8).reshape((height, width))
        elif image_type == b'RGB':
            color_mode = 'RGB'
            pixels = np.frombuffer(raw_img.read(), dtype=np.uint8).reshape((height, width, 3))
        else:
            raise ValueError(f"Неподдерживаемый цветовой режим изображения: {image_type}")
        img = Image.fromarray(pixels, mode=color_mode)
        img.save(out_image) 

    return out_image

ConvertToRaw('gray_image.jpg', 'gray_image.raw')