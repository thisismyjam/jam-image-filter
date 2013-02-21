import sys
import math
import scipy.ndimage as ndimage
import scipy
import Image
import ImageFilter
import numpy as np
import util

def blur(original, sigma=10, darken=True):
    original = util.resize_jam_background(original)
    original = original.convert('RGB')

    if darken:
        original = original.point(lambda p: p * .8)

    image = scipy.misc.fromimage(original, flatten=False)

    image = image.transpose((2, 0, 1))
    r = ndimage.gaussian_filter(image[0], sigma=sigma)
    g = ndimage.gaussian_filter(image[1], sigma=sigma)
    b = ndimage.gaussian_filter(image[2], sigma=sigma)
    image = np.array([r, g, b]).transpose((1, 2, 0))

    return scipy.misc.toimage(image)

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    image = blur(image)
    image.save(sys.argv[2], quality=90)
