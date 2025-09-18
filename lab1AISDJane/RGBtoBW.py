from PIL import Image

# Открываем цветное изображение
color_image = Image.open('D:\Desktop\lab1AISD\BW_image2.png')

# Преобразуем изображение в черно-белое
bw_image = color_image.convert('L')

# Сохраняем черно-белое изображение
bw_image.save('D:\Desktop\lab1AISD\\BW_image22.png')


# Показываем изображение
bw_image.show()
