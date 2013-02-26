import sys
import aggdraw
import math
import Image
import scipy.spatial.distance as distance
import numpy as np
from ImageEnhance import Contrast
import util
import random

def stitch(im, pixelation=12):
    im = im.convert('RGB')

    im = util.resize_jam_background(im)
    width, height = im.size

    # pixelate
    im = im.resize((int(math.ceil(width / float(pixelation))),
                    int(math.ceil(height / float(pixelation)))))
    pix = im.load()

    # random bg colour
    colours = util.get_dominant_colours(im, 2)
    colours = map(tuple, colours)
    colours += [(0,0,0), (255,255,255)]
    bg_index = random.randint(0, len(colours) - 1)

    width, height = im.size
    new = Image.new('RGB', (width * pixelation, height * pixelation), colours[bg_index])
    draw = aggdraw.Draw(new)
    width, height = new.size

    # draw stitches
    for y in xrange(0, height, pixelation):
        for x in xrange(0, width, pixelation):
            pen = aggdraw.Pen(pix[x / pixelation, y / pixelation], 2)
            draw.line((x, y, x + pixelation - 3, y + pixelation - 3), pen)
            draw.line((x + pixelation - 3, y, x, y + pixelation - 3), pen)
    draw.flush()

    return new

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = stitch(image)
    image.save(sys.argv[2], quality=90)
