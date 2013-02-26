import os
import sys
import math
import Image
import ImageOps
import util
import colorsys
import random

def bokeh(image):
    image = image.convert('RGB')
    colours = util.get_dominant_colours(image, 8)
    colours = util.order_colours_by_brightness(colours)[2:7]
    colour = random.choice(colours)
    colour = util.modify_hsv(colour, s=lambda s: 255, v=lambda v: 255)
    light = (255, 244, 180)

    layer = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/' +
                       'assets/bokeh.png')
    layer = util.random_crop(layer, util.WIDTH, util.HEIGHT)
    r, g, b, a = layer.split()
    layer = layer.convert('RGB')
    layer = ImageOps.grayscale(layer)
    layer = ImageOps.colorize(layer, colour, light)
    layer.putalpha(a)
    im = Image.new('RGB', layer.size)
    im.paste(layer, (0, 0), layer)
    return im

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im = bokeh(im)
    im.save(sys.argv[2], quality=90)
