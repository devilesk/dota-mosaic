import os
import numpy as np
from skimage import color
from PIL import Image

def closest_color(color_index, p):
    v = 99999999
    i = ''
    for c in color_index:
        d = (color_index[c][0] - p[0])*(color_index[c][0] - p[0]) + (color_index[c][1] - p[1])*(color_index[c][1] - p[1]) + (color_index[c][2] - p[2])*(color_index[c][2] - p[2])
        if d < v:
            v = d
            i = c
    return i

def average_lab(im):
    width, height = len(im[0]), len(im)
    pixel_count = width * height
    l = 0
    a = 0
    b = 0
    for x in range(0, height):
        for y in range(0, width):
            l += im[x][y][0]
            a += im[x][y][1]
            b += im[x][y][2]
    l = l / pixel_count
    a = a / pixel_count
    b = b / pixel_count
    return np.array([l, a, b])

def get_image_index(image_path):
    files = [x.replace('.png', '') for x in os.listdir(image_path)]
    image_index = {}

    for f in files:
        img_filename = os.path.join(image_path, f + ".png")
        img = Image.open(img_filename).convert('RGB')
        image_index[f] = average_lab(color.rgb2lab(img))
    return image_index

def mosaic(image_path, dst, tile_path, tile_width, tile_height):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    final_img = Image.new('RGB', (width * tile_width, height * tile_height))
    img_data = color.rgb2lab(img)
    image_index = get_image_index(tile_path)
    for x in range(0, width):
        for y in range(0, height):
            pixel = np.array(img_data[y][x])
            t = closest_color(image_index, pixel)
            in_file = os.path.join(tile_path, t + ".png")
            tile = Image.open(in_file).convert('RGB')
            final_img.paste(tile, (x * tile_width, y * tile_height))
    final_img.save(dst)
