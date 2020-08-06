import tensorflow as tf
from yad2k.models.keras_yolo import yolo_boxes_to_corners
from DrawBoxes_Function import *
"该文件包含执行yolo算法的一系列算法，以及识别到的人或车数量的统计与输出"


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

def yolo_non_max_suppression(scores, boxes, classes, max_boxes = 30, iou_threshold = 0.5):

    max_boxes_tensor = K.variable(max_boxes, dtype='int32')     # 用于tf.image.non_max_suppression()的张量
    K.get_session().run(tf.variables_initializer([max_boxes_tensor])) # 初始化变量 max_boxes_tensor

    #使用tensorflow框架下的函数，进行非极大值抑制
    nms_indices = tf.image.non_max_suppression(boxes, scores, max_boxes, iou_threshold, name=None)

    #提取数据
    scores = K.gather(scores, nms_indices)
    boxes = K.gather(boxes, nms_indices)
    classes = K.gather(classes, nms_indices)
    return scores, boxes, classes

def yolo_eval(yolo_outputs, image_shape = (720., 1280.), max_boxes=60, score_threshold=0.5, iou_threshold=.6): #路口参数为(0.15,.2)

    box_confidence, box_xy, box_wh, box_class_probs = yolo_outputs

    boxes = yolo_boxes_to_corners(box_xy, box_wh)
    scores, boxes, classes = yolo_filter_boxes(box_confidence, boxes, box_class_probs, score_threshold)
    boxes = scale_boxes(boxes, image_shape)

    scores, boxes, classes = yolo_non_max_suppression(scores, boxes, classes, max_boxes, iou_threshold)

    return scores, boxes, classes



def only_detection_number(sess,need,yolo_model,scores,boxes,classes,class_names):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    image, image_data = preprocess_image_change_version(frame, model_image_size=(608, 608))
    out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes],
                                                  feed_dict={yolo_model.input: image_data, K.learning_phase(): 0})

    print('Found {} boxes'.format(len(out_boxes)))

    if need =='persones':
        persones = predict_cars_persones(out_classes, class_names,ASM_need='persones',output=1)
    else:
        cars = predict_cars_persones(out_classes, class_names,ASM_need='cars',output=1)

    cap.release()
    cv2.destroyAllWindows()

    if need == 'persones':
        return persones
    if need == 'cars':
        return cars