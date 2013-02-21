import os
import sys
import math
import Image
import ImageOps
import util
import colorsys
import random

def tats(image):
    image = image.convert('RGB')
    colours = util.get_dominant_colours(image, 9)
    colours = util.order_colours_by_brightness(colours)

    bg = random.choice(colours[:3])
    light = random.choice(colours[3:6])
    dark = random.choice(colours[6:])

    dist = math.sqrt(sum(map(lambda (a, b): math.pow(a - b, 2), zip(light, dark))))
    if dist < 100:
        light = util.modify_hls(light, l=lambda l: l + 100)

    light = util.modify_hls(light, s=lambda s: s + 100)
    dark = util.modify_hls(dark, s=lambda s: s + 100)

    layer = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/' +
                       'assets/tats.png')
    layer.load()
    r, g, b, a = layer.split()
    layer = layer.convert('RGB')
    layer = ImageOps.grayscale(layer)
    layer = ImageOps.colorize(layer, tuple(dark), tuple(light))
    layer.putalpha(a)
    im = Image.new('RGB', layer.size, tuple(bg))
    im.paste(layer, mask=layer)
    return im

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    im = tats(im)
    im.save(sys.argv[2], quality=96)
