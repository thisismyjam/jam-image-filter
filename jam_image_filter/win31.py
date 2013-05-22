import Image
import random
import glob
import sys
import os

def win31(im):
    tiles = glob.glob(os.path.abspath(os.path.dirname(__file__)) + '/win31/*.bmp')
    tile = random.choice(tiles)
    new = Image.open(tile)
    new = new.resize((new.size[0] * 2, new.size[1] * 2))
    return new

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = win31(image)
    image.save(sys.argv[2], quality=90)
