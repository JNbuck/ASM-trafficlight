import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import scipy.io
import scipy.misc
import numpy as np
import pandas as pd
import PIL
import tensorflow as tf
import cv2 as cv2
from keras import backend as K
from keras.layers import Input, Lambda, Conv2D
from keras.models import load_model, Model
from yolo_utils_test import read_classes, read_anchors, generate_colors, preprocess_image, draw_boxes, scale_boxes,\
    predict_cars_persones
from yad2k.models.keras_yolo import yolo_head, yolo_boxes_to_corners, preprocess_true_boxes, yolo_loss, yolo_body
from Opencv_test import *



def yolo_filter_boxes(box_confidence, boxes, box_class_probs, threshold = .6):
    box_scores = box_confidence * box_class_probs
    box_classes = K.argmax(box_scores, axis=-1)
    box_class_scores = K.max(box_scores, axis=-1, keepdims=False)
    filtering_mask = box_class_scores >= threshold
    scores = tf.boolean_mask(box_class_scores, filtering_mask)
    boxes = tf.boolean_mask(boxes, filtering_mask)
    classes = tf.boolean_mask(box_classes, filtering_mask)
    return scores, boxes, classes

def iou(box1, box2):
    xi1 = max(box1[0], box2[0])
    yi1 = max(box1[1], box2[1])
    xi2 = min(box1[2], box2[2])
    yi2 = min(box1[3], box2[3])
    inter_area = (xi2 - xi1) * (yi2 - yi1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area
    iou = inter_area / union_area
    return iou

def yolo_non_max_suppression(scores, boxes, classes, max_boxes = 10, iou_threshold = 0.5):
    max_boxes_tensor = K.variable(max_boxes, dtype='int32')     # tensor to be used in tf.image.non_max_suppression()
    K.get_session().run(tf.variables_initializer([max_boxes_tensor])) # initialize variable max_boxes_tensor
    nms_indices = tf.image.non_max_suppression(boxes, scores, max_boxes, iou_threshold, name=None)
    scores = K.gather(scores, nms_indices)
    boxes = K.gather(boxes, nms_indices)
    classes = K.gather(classes, nms_indices)
    return scores, boxes, classes

def yolo_eval(yolo_outputs, image_shape = (720., 1280.), max_boxes=10, score_threshold=.576, iou_threshold=.5):
    box_confidence, box_xy, box_wh, box_class_probs = yolo_outputs
    boxes = yolo_boxes_to_corners(box_xy, box_wh)
    scores, boxes, classes = yolo_filter_boxes(box_confidence, boxes, box_class_probs, score_threshold)
    boxes = scale_boxes(boxes, image_shape)
    scores, boxes, classes = yolo_non_max_suppression(scores, boxes, classes, max_boxes, iou_threshold)
    return scores, boxes, classes

sess = K.get_session()

class_names = read_classes("model_data/coco_classes.txt")
anchors = read_anchors("model_data/yolo_anchors.txt")
image_shape = (480., 640.)
#该电脑的摄像头像素为（480，640）

yolo_model = load_model("model_data/yolo.h5")

yolo_model.summary()

yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))

scores, boxes, classes = yolo_eval(yolo_outputs, image_shape)


def predict(sess, image_file):

    # image = cv2.imread("images/"+image_file)
    # image, image_data = preprocess_image_change_version(image, model_image_size=(608, 608))
    image, image_data = preprocess_image("images/" + image_file, model_image_size = (608, 608))

    out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes],
                                                  feed_dict = {yolo_model.input:image_data, K.learning_phase(): 0})

    print('Found {} boxes for {}'.format(len(out_boxes), image_file))
    colors = generate_colors(class_names)
    draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)

    #predict the numbers of cars and persones
    predict_cars_persones(out_scores, out_boxes, out_classes, class_names)

    image.save(os.path.join("out",image_file), quality=90)
    output_image = scipy.misc.imread(os.path.join("out", image_file))
    imshow(output_image)
    image.show()
    return out_scores, out_boxes, out_classes


def predict_current_time(sess):
    while (True):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        image, image_data = preprocess_image_change_version(frame, model_image_size=(608, 608))
        out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes],
                                                      feed_dict={yolo_model.input: image_data, K.learning_phase(): 0})

        print('Found {} boxes'.format(len(out_boxes)))
        colors = generate_colors(class_names)
        draw_boxes_current_time(image, out_scores, out_boxes, out_classes, class_names, colors)

        # predict the numbers of cars and persones
        predict_cars_persones(out_scores, out_boxes, out_classes, class_names)


        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return out_scores, out_boxes, out_classes


#out_scores, out_boxes, out_classes = predict(sess, "test5.jpg")
predict_current_time(sess)









