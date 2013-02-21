import os
import sys
import math
import Image
import ImageOps
import util
import colorsys
import random

def leopard(image):
    image = image.convert('RGB')
    colours = util.get_dominant_colours(image, 12)
    colours = util.order_colours_by_brightness(colours)
    indices = sorted(random.sample(range(len(colours)), 3))
    colours = [colours[i] for i in indices]
    colours = util.spread_colours_by_lightness(colours)
    light, bg, dark = map(tuple, colours)

    layer = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/' +
                       'assets/leopard.png')
    layer.load()
    r, g, b, a = layer.split()
    layer = layer.convert('RGB')
    layer = ImageOps.grayscale(layer)
    layer = ImageOps.colorize(layer, dark, light)
    layer.putalpha(a)
    im = Image.new('RGB', layer.size, bg)
    im.paste(layer, mask=layer)
    return im

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im = leopard(im)
    im.save(sys.argv[2], quality=96)
