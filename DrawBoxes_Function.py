import cv2 as cv2
import numpy as np
from PIL import Image
import colorsys
import random
from keras import backend as K
"该文件包含的方法为数据的载入以及实时演示窗口，为图片显示的一些列必要方法"


def read_classes(classes_path): #需要的参数为目标种类txt文件的文件路径，目前该文件在model_data文件夹中
    "从数据文件中获取目标种类数据"
    with open(classes_path) as f:   #打开文件
        class_names = f.readlines()     #逐行阅读
    class_names = [c.strip() for c in class_names] #将每个字符提取进列表
    return class_names  #返回一个包含类别名的列表

def read_anchors(anchors_path):  #需要的参数为包含锚盒的数据的txt文件的路径，目前该文件在model_data文件夹中
    "从数据文件中获取初始化锚盒的数据"
    with open(anchors_path) as f:   #打开文件
        anchors = f.readline()      #逐行阅读
        anchors = [float(x) for x in anchors.split(',')]    #将每个数据提取进列表
        anchors = np.array(anchors).reshape(-1, 2)     #运用reshape的自动计算属性，将列变为2的同时自动计算了行的数量
    return anchors  #返回锚盒数据

def scale_boxes(boxes, image_shape):
    """ 按比例缩放盒子从而适配图片的尺寸"""
    height = image_shape[0]     #获取图片的高度
    width = image_shape[1]      #获取图片的宽度
    image_dims = K.stack([height, width, height, width]) #为该（长和宽）（长和宽）构成的列表增加一个维度
                                                         #假设原本为[200,300,200,300]
                                                         #现在变为[[200,300,200,300]]
    image_dims = K.reshape(image_dims, [1, 4])      #将原本的[200,300,200,300]（4，）变为（1，4）
    "结合K.stack和K.reshape使得该图片比例的矩阵维度可以和boxes的维度一致，方便逐个元素相乘"
    boxes = boxes * image_dims  #左上角或者右下角放大或者缩小相同的比例
    return boxes    #返回调整过比例的盒子数据

def preprocess_image_change_version(image, model_image_size):
    "将图片尺寸转换为模型输入图片尺寸(608,608)"
    image_RGB_= image[:, :, ::-1]  # BGR -> RGB
    resized_image = cv2.resize(image_RGB_,model_image_size) #将图片数据调整为模型输入图片尺寸
    image_data = np.array(resized_image, dtype='float32')   #将转换后的图片数据变为array数组模式
    image_data /= 255.  #对于数据进行归一化，方便递归的同时有利于boxes数据随着图片尺寸的变化来变化
    #image_data = np.expand_dims(image_data, 3)
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
                                                # 增多一个维度有利于形成（m,(R,G,B)）型数组，利于数据批量处理
    return image, image_data #返回处理后的图片和图片数据

def generate_colors(class_names):
    "依据种类的不同随机抽取不同的颜色"
    hsv_tuples = [(x / len(class_names), 1., 1.) for x in range(len(class_names))]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    random.seed(10101)  # Fixed seed for consistent colors across runs.
    random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
    random.seed(None)  # Reset seed to default.
    return colors

def draw_boxes_current_time1(frame, out_scores, out_boxes, out_classes, class_names, colors):
    "对opencv截取到的来自摄像头的图片进行绘制"
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    thickness = (image.size[0] + image.size[1]) // 300

    for i, c in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[c]
        box = out_boxes[i]
        score = out_scores[i]

        label = '{} {:.2f}'.format(predicted_class, score)

        label_size = cv2.getTextSize(text=label,
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX ,
                                     fontScale=np.floor(3e-3 * image.size[1] ).astype('int32')-0.5,
                                     thickness=thickness-1 )
        print("label_siez = "+str(label_size[0])+" "+str(label_size[1]))
        print("label_size.shape = "+str(label_size[0][0])+"  "+str(label_size[0][1]))

        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[0], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[1], np.floor(right + 0.5).astype('int32'))
        print(label, (left, top), (right, bottom))

        if top - label_size[0][1] >= 0:
            text_origin = np.array([left, top - label_size[0][1]]).astype('int32')

        else:
            text_origin = np.array([left, top + 1]).astype('int32')

        # My kingdom for a good redistributable image drawing library.
        cv2.rectangle(frame, (left, top), (right, bottom), colors[c],thickness-1)
        cv2.rectangle(frame,tuple(text_origin), tuple(text_origin + label_size[0]), colors[c],thickness = -1)

        cv2.putText(frame,
                    label,
                    tuple([left,top]),
                    cv2.FONT_HERSHEY_SIMPLEX ,
                    np.floor(3e-3 * image.size[1] ).astype('int32')-0.5,
                    color=(0,0,0),
                    thickness=thickness-1)
        #各参数依次是：图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细

def predict_current_time(sess,scores,boxes,classes,yolo_model,class_names):
    "实时检测函数，可以启动来进行实时监控"
    while (True):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()


        image, image_data = preprocess_image_change_version(frame, model_image_size=(608, 608))
        out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes],
                                                      feed_dict={yolo_model.input: image_data, K.learning_phase(): 0})

        print('Found {} boxes'.format(len(out_boxes)))
        colors = generate_colors(class_names)
        draw_boxes_current_time1(image, out_scores, out_boxes, out_classes, class_names, colors)
        "这个画图函数为改进版本，可以正常使用"

        # predict the numbers of cars and persones
        predict_cars_persones(out_classes, class_names,output=0)

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return out_scores, out_boxes, out_classes

def predict_cars_persones( out_classes, class_names,ASM_need='persones',output=0):
    "根据需求返回当前的人数或者车数"
    persones = int(0)
    cars = int(0)
    for i, c in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[c]

        # the first change:add the parameter output
        if predicted_class == 'person':
            persones += 1
        elif predicted_class == 'car':
            cars += 1

    if output == 1:
        if ASM_need == 'persones':
            print("此时人行道有 {} 个人".format(persones))
            return persones
        if ASM_need == 'cars':
            print("此时车道有 {} 辆车".format(cars))
            return cars
    else:
        print("this picture have {} persones,and {} cars ".format(str(persones), str(cars)))