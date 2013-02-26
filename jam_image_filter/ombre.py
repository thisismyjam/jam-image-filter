import os
import sys
import math
import Image
import ImageOps
import util
import colorsys
import random

def ombre(image):
    image = image.convert('RGB')
    colours = util.get_dominant_colours(image, 12)
    colours = util.order_colours_by_brightness(colours)
    light = random.choice(colours[:3])
    dark = random.choice(colours[-3:])

    layer = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/' +
                       'assets/ombre.jpg')
    layer = util.random_crop(layer, util.WIDTH, util.HEIGHT)
    
    layer = layer.convert('RGB')
    layer = ImageOps.grayscale(layer)
    layer = ImageOps.colorize(layer, dark, light)
    return layer

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im = ombre(im)
    im.save(sys.argv[2], quality=90)
