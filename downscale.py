from PIL import Image, ImageOps
import cv2
import numpy as np

image_path='input.png'
output_path='output.png'
downscale_factor = 5
upscale_factor = downscale_factor
color_bit_depth = 8
border_thickness = 2
border_color=(255, 255, 255)
custom_palette_hex = ["#000000","#1D2B53","#7E2553","#008751","#AB5236","#5F574F","#C2C3C7","#FFF1E8","#FF004D","#FFA300","#FFEC27","#00E436","#29ADFF","#83769C","#FF77A8","#FFCCAA"]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

custom_palette = [hex_to_rgb(color) for color in custom_palette_hex]

def jpg_to_png():
    try:im = Image.open('input.jpg')
    except FileNotFoundError:
        try:im = Image.open('input.jpeg')
        except FileNotFoundError:return
        else:
            print("converting jpeg")
            im.save(image_path)
    else:
        print("converting jpg")
        im.save(image_path)
        
def add_border(input_image):
    input_image = np.array(input_image)
    input_image = input_image[:, :, ::-1].copy()
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    kernel = np.ones((border_thickness, border_thickness), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    mask = dilated_edges > 0
    border_image = np.zeros_like(input_image)
    border_image[mask] = border_color
    bordered_image = cv2.addWeighted(input_image, 1, border_image, 1, 0)
    bordered_image_pil = Image.fromarray(cv2.cvtColor(bordered_image, cv2.COLOR_BGR2RGB))
    return bordered_image_pil
    
def quantize_color(input_image):
    if input_image.mode != 'RGB': input_image = input_image.convert('RGB')
    palette_image = Image.new('P', (1, 1))
    palette_image.putpalette(sum(custom_palette, ()))
    return input_image.quantize(palette=palette_image)

def posterize(input_image):
    return ImageOps.posterize(input_image, color_bit_depth)

def downscale(input_image):
    new_size = (input_image.width // downscale_factor, input_image.height // downscale_factor)
    return input_image.resize(new_size, Image.NEAREST)

def upscale(input_image):
    new_size = (input_image.width * upscale_factor, input_image.height * upscale_factor)
    return input_image.resize(new_size, Image.NEAREST)

jpg_to_png()
image = Image.open(image_path)
image = downscale(image)
image = posterize(image)
#image = add_border(image)
image = quantize_color(image)
image = upscale(image)
image.save(output_path)
print("done :)")

#gameboy: "#9bbc0f","#8bac0f","#306230","#0f380f"
#pico8: "#000000","#1D2B53","#7E2553","#008751","#AB5236","#5F574F","#C2C3C7","#FFF1E8","#FF004D","#FFA300","#FFEC27","#00E436","#29ADFF","#83769C","#FF77A8","#FFCCAA"
#cmyk: "#00FFFF","#FF00FF","#FFFF00","#000000","FFFFFF"
#rgb: "#FF0000","#00FF00","#0000FF","#FFFFFF","#000000"
