import cv2 as cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import psutil
import time


def take_photo():
    cap = cv2.VideoCapture(0)
    i = 5
    while (True):

        image_file = os.path.join('images', 'test' + str(i) + '.jpg')
        ret, frame = cap.read()

        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)  #将颜色通道进行调换
        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  #将BGR通道转化为单通道

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('t'):
            cv2.imwrite(image_file, frame)
            i += int(1)

    cap.release()
    cv2.destroyAllWindows()


def preprocess_image_change_version(image, model_image_size):
    image_RGB_= image[:, :, ::-1]  # BGR -> RGB
    resized_image = cv2.resize(image_RGB_,model_image_size)
    image_data = np.array(resized_image, dtype='float32')
    image_data /= 255.
    #image_data = np.expand_dims(image_data, 3)
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    return image, image_data




def draw_boxes_current_time(frame,out_scores, out_boxes, out_classes, class_names, colors):
    # font = ImageFont.truetype(font='font/FiraMono-Medium.otf',size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    #设置字体

    #以下一行为将PIL.image转化为cv2格式
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    font = ImageFont.truetype(font='C:/Windows/Fonts/ChaparralPro-Regular.otf',
                                size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    thickness = (image.size[0] + image.size[1]) // 300



    for i, c in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[c]
        box = out_boxes[i]
        score = out_scores[i]

        label = '{} {:.2f}'.format(predicted_class, score)

        draw = ImageDraw.Draw(image)
        label_size = draw.textsize(label, font)

        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
        print(label, (left, top), (right, bottom))

        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        # My kingdom for a good redistributable image drawing library.
        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline=colors[c])
        draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=colors[c])
        draw.text(text_origin, label, fill=(0, 0, 0), font=font)
        del draw

    process_list = []
    for proc in psutil.process_iter():
        process_list.append(proc)

    image.show()

    for proc in psutil.process_iter():
        if not proc in process_list:
            proc.kill()






