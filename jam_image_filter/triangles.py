import sys
import aggdraw
import math
import Image
import random
import numpy as np
import util
import os.path
import ImageOps

def get_triangle_path(mid_x, mid_y, min_length = 70, max_length = 70):
    angle = random.random() * (2 * math.pi / 3)
    points = []
    for angle in np.arange(angle, angle + 2 * math.pi, 2 * math.pi / 3):
        length = min_length + random.random() * (max_length - min_length)
        x = mid_x + math.cos(angle) * length
        y = mid_y + math.sin(angle) * length
        points.extend([x, y])
    return points

def triangles(original, n=30, size=150, width=700,
              height=700, min_distance=70, opacity=220):
    original = original.convert('RGB')
    colours = util.get_dominant_colours(original, 8)
    colours_ordered = util.order_colours_by_brightness(colours)
    brightest_colour = list(random.choice(colours_ordered[:3]))
    brightest_colour.append(0)

    new = Image.new('RGBA', (width, height), tuple(brightest_colour))

    draw = aggdraw.Draw(new)

    centres = []

    def is_too_close(x, y):
        for centre in centres:
            if math.sqrt(math.pow(centre[0] - x, 2) + 
                         math.pow(centre[1] - y, 2)) < min_distance:
                return True
        return False

    for i in xrange(n):

        colour = tuple(colours[int(random.randint(0, len(colours) - 1))])
        x = random.randint(size / 2, width - 1 - size / 2)
        y = random.randint(size / 2, height - 1 - size / 2)

        if is_too_close(x, y):
            continue

        centres.append((x, y))

        brush = aggdraw.Brush(colour, opacity)
        points = get_triangle_path(x, y, size / 2, size / 2)
        draw.polygon(points, None, brush)
    draw.flush()

    brightest_colour = brightest_colour[0:3]

    texture = Image.open(os.path.dirname(os.path.abspath(__file__)) + '/' +
                         'assets/airbrush.png')
    texture = texture.convert('RGBA')
    r, g, b, a = texture.split()
    texture = ImageOps.grayscale(texture)
    texture = ImageOps.colorize(texture, (0, 0, 0), tuple(brightest_colour))
    texture = texture.convert('RGBA')
    texture.putalpha(a)

    r, g, b, a = new.split()

    texture = texture.crop((0, 0, width, height))
    texture_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    texture_layer.paste(texture, mask=new)
    new.paste(texture_layer, mask=texture_layer)

    im = Image.new('RGB', (width, height), tuple(brightest_colour))
    im.paste(new, mask=a)

    return im

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = triangles(image)
    image.save(sys.argv[2], quality=90)
