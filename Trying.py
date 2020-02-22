import colorsys
import imghdr
import os
import random
from keras import backend as K
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont





def preprocess_image_change_version(image, model_image_size):
    image_RGB_= image[:, :, ::-1]  # BGR -> RGB
    resized_image = cv2.resize(image_RGB_,model_image_size)
    image_data = np.array(resized_image, dtype='float32')
    image_data /= 255.
    #image_data = np.expand_dims(image_data, 3)
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    return image, image_data


def preprocess_image(img_path, model_image_size):
    image = Image.open(img_path)
    resized_image = image.resize(tuple(reversed(model_image_size)), Image.BICUBIC)
    image_data = np.array(resized_image, dtype='float32')
    image_data /= 255.
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    return image, image_data

image_file = "test5.jpg"
image1, image_data1 = preprocess_image("images/" + image_file, model_image_size = (608, 608))
print(image_data1.shape)


image = cv2.imread("images/"+image_file)
image2, image_data2 = preprocess_image_change_version(image, model_image_size = (608, 608))
print(image2.shape)
print(image_data2.shape)


