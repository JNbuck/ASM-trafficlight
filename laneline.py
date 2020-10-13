import cv2 as cv2
import numpy as np
from decimal import Decimal

# 定义一个和输入图像同样大小的全黑图像mark，这个mark也称为掩膜
def roi_mask(img,vertics):
    mask = np.zeros_like(img)
    # 根据输入图像的通道数，忽略的像素点是多通道的白色，还是单通道的白色
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        mask_color = (255,)*channel_count
    else:
        mask_color = 255
    # cv2.fillPloy()函数可以填充凸多边形，只需要提供凸多边形的顶点即可
    cv2.fillPoly(mask,[vertics],mask_color)
    masked_img = cv2.bitwise_and(img,mask)
    return masked_img

# 将不连续的直线转化为连续的直线，并绘制出来
def draw_lines(img, lines, color=[255, 0, 0], thickness=2,car_load=3,line_y_max = 0,line_y_min = 593):


    # 以下的一堆列表是试验模式，后期修改为array数组模式
    left_lines = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]
    k_arr = []
    indexes = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            k = (y2 - y1) / (x2 - x1)
            k_arr.append(k)

    for i in range(len(k_arr)):
        if k_arr[i] == 0:
            continue
        else:
            crek = k_arr[i]
            index = []
            for j in range(len(k_arr)):
                if (crek <= k_arr[j] + 0.2) and (crek >= k_arr[j] - 0.2):
                    index.append(j)
                    k_arr[j] = 0
            indexes.append(index)

    lines_arr = np.array(lines)
    lines_arr = np.squeeze(lines_arr)

    m = 0
    while m < car_load*2+2:
        for index in indexes:
            for i in index:
                left_lines[m].append(lines_arr[i][0])
                left_lines[m + 1].append(lines_arr[i][1])
                left_lines[m].append(lines_arr[i][2])
                left_lines[m + 1].append(lines_arr[i][3])
            m = m + 2

    n = 0
    while n < car_load*2+2:
        # 最小二乘直线拟合
        left_line_k, left_line_b = np.polyfit(left_lines[n], left_lines[n + 1], 1)
        cv2.line(img,
                 (int((line_y_max - left_line_b) / left_line_k), line_y_max),
                 (int((line_y_min - left_line_b) / left_line_k), line_y_min),
                 color, thickness)
        n = n + 2


def draw_lines_simple(img,lines,color = [0,0,255],thickness = 2):

    for line in lines:
        for x1,y1,x2,y2 in line:

            cv2.line(img,(x1,y1),(x2,y2),color,thickness)


def detection_lane(filename,gauss,car_load,line_y_max,line_y_min,apex_arr,simple=None,savename=None):
    # 载入图片
    img = cv2.imread(filename, 1)
    # 将载入的图片转化为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 对灰度图进行高斯模糊
    blur_gray = blur = cv2.GaussianBlur(gray, gauss, 0)  # 高斯模糊
    # 对转化好的高斯模糊灰度图进行canny边缘检测
    # Canny边缘检测算法
    canny_lthreshold = 100
    canny_hthreshold = 260
    edges = cv2.Canny(blur_gray, canny_lthreshold, canny_hthreshold)

    # 设置roi区域，为了后续只检测roi区域内的直线
    vertices = np.array(apex_arr, np.int32)
    roi_image = roi_mask(edges, vertices)

    # 使用Hough变换，对直线进行检测
    # 设置霍夫变换的基本参数
    rho = 1
    theta = np.pi / 180
    threshold = 15  # 15
    min_line_lenght = 40  # 40
    max_line_gap = 20  # 20
    # 调用cv2中的霍夫变换函数，都目标区域进行处理
    lines = cv2.HoughLinesP(roi_image, rho, theta, threshold, min_line_lenght, max_line_gap)
    line_image = np.copy(img)
    while simple:
        draw_lines(line_image,lines ,[255, 0, 0], 3)
        break

    draw_lines(line_image, lines, [255, 0, 0], 3, car_load, line_y_max, line_y_min)

    # cv2.imshow('img',img)
    # cv2.imshow('gray',gray)
    # cv2.imshow('blur_gray',blur_gray)
    # cv2.imshow('edges',edges)
    cv2.imshow('roi_image', roi_image)
    cv2.imshow('line_image', line_image)

    while simple:
        cv2.imwrite(savename,line_image)
        break
    cv2.waitKey(0)


filename = 'images\\test1.png'
gauss = (7,7)
car_load = 3
line_y_max = 179    # 希望的线条延伸到的地方 test1 (179,593) test (179,384)
line_y_min = 593

left_bottom = [7, 559]  # 左边区域三角形左下角顶点
# right_bottom = [edges.shape[1],edges.shape[0]]
apex1 = [484, 117]  # 左边区域梯形左顶点
apex2 = [653, 155]  # 左边区域梯形右顶点
apex3 = [586, 590]  # 左边区域梯形右下角顶点
all_apex_1 = [left_bottom, apex1, apex2, apex3]
all_apex_2 = [[76, 324], [250, 184], [446, 188], [551, 332]]

detection_lane(filename,gauss,3,line_y_max,line_y_min,all_apex_1)