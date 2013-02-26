import sys
import math
import Image
import numpy as np
import util
import sh
import random
import tempfile
import os

# pre/post-processor for /src/glitch
def glitch(im, min_pixelation=3, max_pixelation=18, max_attempts=20,
           min_diff=5000, max_diff=25000, darken=True):

    try:
        sh.glitch
    except sh.CommandNotFound:
        print 'Could not find glitch. Did you build and install it?'
        sys.exit(1)

    im = im.convert('RGB')
    im = util.resize_jam_background(im)
    width, height = im.size

    pixelation = random.random() % (max_pixelation - min_pixelation) + min_pixelation
    im = im.resize((int(width / pixelation), int(height / pixelation)))
    im = im.resize((int(width), int(height)))

    infile = tempfile.NamedTemporaryFile(suffix='.jpg', prefix='glitchtmp',
                                         delete=False)
    outfile = tempfile.NamedTemporaryFile(suffix='.jpg', prefix='glitchtmp',
                                          delete=False)
    infile.close()
    outfile.close()

    im.save(infile.name)

    # naive image diff to ensure image is not too different from original
    for attempt in xrange(max_attempts):
        sh.glitch(infile.name, outfile.name)
        inim = Image.open(infile.name)
        outim = Image.open(outfile.name)
        inpix = inim.resize((10, 10)).load()
        outpix = outim.resize((10, 10)).load()
        diff = 0
        for y in xrange(10):
            for x in xrange(10):
                for i in xrange(3):
                    diff += abs(inpix[x, y][i] - outpix[x, y][i])
        if diff > min_diff and diff < max_diff:
            break

    im = Image.open(outfile.name)
    if darken:
        im = im.point(lambda p: p * .8)

    os.unlink(infile.name)
    os.unlink(outfile.name)
        
    return im

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = glitch(image)
    image.save(sys.argv[2], quality=90)
