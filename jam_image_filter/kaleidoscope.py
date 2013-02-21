import sys
from PIL import Image
import util

def kaleidoscope(original, max_width=400, max_height=400, darken=True):
    original = original.convert('RGB')
    original = util.max_size(original, max_width, max_height)
    width, height = original.size
    original_pix = original.load()

    length = min(height, width)

    new = Image.new('RGB', (length * 2, length * 2))
    new_pix = new.load()

    for part in xrange(8):

        reverse = part in [1, 4, 6, 7]
        flip = part in [3, 4, 5, 6]
        turn = part in [2, 3, 6, 7]

        for y in xrange(length):
            for x in xrange(length - y - 1, length):

                if turn:
                    to_x = length + y + 1
                    to_y = length + (length - x) - 1
                else:
                    to_x = x
                    to_y = length + y

                if reverse:
                    to_x = 2 * length - to_x - 1
                if flip:
                    to_y = 2 * length - to_y - 1

                try:
                    new_pix[to_x, to_y] = original_pix[x, y]
                except IndexError:
                    pass

    if darken:
        new = new.point(lambda p: p * .8)

    return new

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = kaleidoscope(image)
    image.save(sys.argv[2], quality=96)
