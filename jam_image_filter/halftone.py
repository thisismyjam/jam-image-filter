import sys
import aggdraw
import math
import Image
import util
import random
from ImageEnhance import Contrast

def rnd():
    return 1 + random.randint(-1, 1) / 6.0

def halftone(original, radius=3, border=21, black_and_white=False):
    original = util.resize_jam_background(original, util.WIDTH + border * 2,
                                          util.HEIGHT + border * 2)
    original = original.convert('RGB')
    width, height = original.size

    if black_and_white:
        bg = (255, 255, 255)
        fg = (0, 0, 0)
    else:
        colours = util.get_dominant_colours(original, 10)
        colours = util.order_colours_by_brightness(colours)
        fg = tuple(random.choice(colours[-6:]))
        bg = tuple(random.choice(colours[:3]))
        if fg == bg:
            bg = (255, 255, 255)
            fg = (0, 0, 0)

        original = Contrast(original).enhance(1.5)

    pix = original.load()

    new = Image.new('RGB', (width, height), bg)

    draw = aggdraw.Draw(new)
    pen = aggdraw.Pen(fg)
    brush = aggdraw.Brush(fg)

    x_incr = 2 * radius
    y_incr = math.sqrt(3) * radius
    for y in xrange(0, height + 1, int(y_incr)):
        odd_offset = radius * (y / int(y_incr) % 2)
        for x in range(odd_offset, width + 1, x_incr):
            avg_gray = util.get_avg_gray(pix, x, y, radius)
            if avg_gray > .9:
                r = radius
                rnd = lambda: 1
            else:
                r = radius * avg_gray
                rnd = lambda: 1 + random.randint(-1, 1) / 5.0
            draw.ellipse((x - r * rnd(), y - r * rnd(), x + r * rnd(), y + r * rnd()), pen, brush)
    draw.flush()

    new = util.centre_crop(new, util.WIDTH, util.HEIGHT)
    new = new.point(lambda p: p - 20)

    return new

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = halftone(image)
    image.save(sys.argv[2], quality=96)
