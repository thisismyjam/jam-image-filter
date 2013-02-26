import os
import sys
import math
import Image
import ImageOps
import util
import colorsys
import random

def space(image):
    image = image.convert('RGB')
    colours = util.get_dominant_colours(image, 12)
    colours = util.order_colours_by_brightness(colours)
    indices = sorted(random.sample(range(len(colours)), 3))
    colours = [colours[i] for i in indices]
    light, bg, dark = map(tuple, colours)
    light = (200, 200, 100)
    dark = (100, 200, 100)
    bg = (0, 0, 50, 255)

    layer = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/' +
                       'assets/space.jpg')
    layer = util.random_crop(layer, util.WIDTH, util.HEIGHT)

    colours = util.get_dominant_colours(image, 10)
    colours = util.order_colours_by_saturation(colours)[:-3]
    colours = random.sample(colours, 5)
    colours = util.order_colours_by_hue(colours)

    layer = layer.convert('RGB')
    gradient = util.create_gradient(layer.size, colours)
    im = Image.blend(layer, gradient, .4)

    return im

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im = space(im)
    im.save(sys.argv[2], quality=90)
