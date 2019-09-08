from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np


img_dir = 'data_set/'
original_dir = img_dir + 'ori/'
segment_dir = img_dir + 'seg/'

def generate_train_imgs(ID, sufix_original = 'ori_', sufix_segment = 'seg_'):
    """
    generate and save a pair if images.

    Parameters
    ----------
        ID - int
            the num index for saving the images
        sufix_original - string - optional
            the sufix for the files in the case of originals images.
        sufix_segment - string - optional
            the sufix for the files in the case if segmented images.
    Returns
    -------
        None

    Examples
    --------
    >>> num = 3
    >>> generate_train_imgs(num)
    """
    img_size = 128

    num_circles = random.randint(3, 8) #3 to 8 circles in each img_dir

    cordinates = np.random.randint(0, img_size, (num_circles, 2)) #rand cordinates

    circles_sizes = np.random.randint(3, 32, (num_circles)) #circles size

    generate_original(img_size, cordinates, circles_sizes, ID, sufix_original)
    generate_segment(img_size, cordinates, circles_sizes, ID, sufix_segment)

def generate_original(img_size, cordinates, circles_sizes, ID, sufix_original):
    """
    generate and save the original version of pair images.

    Parameters
    ----------
        img_size - int
            the dimensions of images in pixels
        cordinates - np.darray
            an numpy array of an array of size (n, 2) for define
            the center of the circles
        circles_sizes - np.darray
            an numpy array with the length of the circles with a shape of (n)
        ID - int
            the num index for saving the images
        sufix_original - string
            the sufix for the files in the case of originals images.
    Returns
    -------
        None
    Examples
    --------
    """
    rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGB', (img_size, img_size), rand_color)

    draw = ImageDraw.Draw(image)

    for i, r in enumerate(circles_sizes):
        x1 = cordinates[i, 0] - r
        y1 = cordinates[i, 1] - r
        x2 = cordinates[i, 0] + r
        y2 = cordinates[i, 1] + r

        rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        draw.ellipse((x1, y1, x2, y2), fill = rand_color)

    del draw

    #create a filter here for gen the noise
    image = image.filter(ImageFilter.BLUR)
    image = image.filter(ImageFilter.UnsharpMask(5))

    np_noise = np.random.rand(img_size, img_size) * 70
    noise_image = Image.fromarray(np_noise)
    noise_image = noise_image.convert('RGB')

    image = Image.blend(image, noise_image, alpha=0.5)

    image.save(original_dir + sufix_original + str(ID) + '.png')

def generate_segment(img_size, cordinates, circles_sizes, ID, sufix_segment):
    image = Image.new('RGB', (img_size, img_size))

    draw = ImageDraw.Draw(image)

    for i, r in enumerate(circles_sizes):
        x1 = cordinates[i, 0] - r
        y1 = cordinates[i, 1] - r
        x2 = cordinates[i, 0] + r
        y2 = cordinates[i, 1] + r

        draw.ellipse((x1, y1, x2, y2), fill = 'white')

    del draw
    image.save(segment_dir + sufix_segment + str(ID) + '.png')


def main():
    #okey is done come to generate the data set
    for i in range(256):
        generate_train_imgs(i)
        print('pair of data num:' + str(i)+ ' has been generated')

if __name__ == "__main__":
    main()
