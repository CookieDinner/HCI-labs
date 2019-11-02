from pylab import *
from skimage import io
from skimage import img_as_float
import skimage.morphology as mp
from skimage import feature
import scipy.ndimage
import imageio.core.util


def ignore_warnings(*args, **kwargs):
    pass


imageio.core.util._precision_warn = ignore_warnings

images = ["samolot01.jpg", "samolot02.jpg", "samolot03.jpg",
          "samolot04.jpg", "samolot05.jpg", "samolot06.jpg",
          "samolot07.jpg", "samolot08.jpg", "samolot09.jpg",
          "samolot10.jpg", "samolot11.jpg", "samolot12.jpg",
          "samolot13.jpg", "samolot14.jpg", "samolot15.jpg",
          "samolot16.jpg", "samolot17.jpg", "samolot18.jpg",]

edge_colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 1], [1, 1, 0], [1, 0, 1]]

selem = mp.selem.disk(3)

for i in range(18):
    img = io.imread(images[i], as_gray=True)
    img = img_as_float(img)

    true_image = io.imread(images[i])
    true_image = img_as_float(true_image)

    edges = feature.canny(img, sigma=5)
    edges = mp.binary_dilation(edges, selem=selem)
    labeled, objects = scipy.ndimage.label(edges)

    for j in range(len(edges)):
        for k in range(len(edges[j])):
            for l in range(6):  # number of edge colors
                if labeled[j][k] and (labeled[j][k] % 6) == l:  # if appropriate label is present
                    true_image[j][k] = edge_colors[l]

    print("Processed: ", images[i], "Now saving to Processed/"+images[i]+"...")
    io.imsave(("Processed/" + images[i]), true_image)
    subplot(4, 5, i + 1)
    io.imshow(true_image)


io.show()
