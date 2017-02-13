import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imresize, imread
from sklearn.model_selection import train_test_split
from PIL import Image
import random

def _preprocess(imgs):
    """
    input: takes in numpy array representing images
    output: cleaned and processed data
    """

    img_mean = np.mean(imgs, axis=0)
    img_std = np.std(imgs, axis=0)

    normalized = imgs - img_mean / img_std

    return normalized

def transparent_background(image_path):
    """
    input: Nordstrom Image Path
    output: Nordstrom Image without white background
    """
    offset = (0,0)

    #TRANSPARENT
    img = Image.open(image_path)
    img = img.convert('RGBA')
    pixel = img.load()
    w, h = img.size
    for y in xrange(h):
        for x in xrange(w):
            if pixel[x,y] == (255, 255, 255, 255):
                pixel[x,y] = (255, 255, 255, 0)
    img = img.resize((64,64), Image.ANTIALIAS)

    #PASTE ON RANDOM BACKGROUND
    background_file = Image.open(random.choice(os.listdir('bgs/')))
    background_file.convert('RGBA')
    background_file = background_file.resize((64,64), Image.ANTIALIAS)
    background_file.paste(img, offset, img)
    background_file.convert('RGB')

    return background_file

def load_image(image_path):
    """
    input: path to image
    output: image in numpy array
    """
    img = transparent_background(image_path)
    dims=64
    img = imresize(img, (dims, dims))

    return img

def load_images(path, label):
    """
    input: file path containing images, and the labes it should be assigned (1 or 0)
    output: the images converted into a numpy matrix
    """

    try:
        files = [path + '/' + f for f in os.listdir(path) if ".jpg" in f]
    except:
        print "Files not found"
        exit()
    imgs = [load_image(f)  for f in files]
    dims = 64
    imgs = [i for i in imgs if i.shape == (dims, dims, 3)] ## make sure dimensions work
    # imgs = _preprocess(imgs)
    labels = np.array([[label, 1 - label] for i in imgs])
    data = np.array(imgs)

    return data, labels


def get_data(path_1, path_2):
    """
    input: path1 specifying data of the type we are trying to identify (1)
           path2 specifying data of the type we are not (0)
    output: the labeled data set
    """

    positive_data, positive_label = load_images(path_1, 1)
    negative_data, negative_label = load_images(path_2, 0)

    data = np.concatenate((positive_data, negative_data))
    labels = np.concatenate((positive_label, negative_label))

    return data, labels

def get_test_and_validation_data(path_1, path_2):
    """
    input: the location of datasets
    output: test and validation data and labels
    """

    data, labels = get_data(path_1, path_2)
    return train_test_split(data, labels, test_size=0.2)
