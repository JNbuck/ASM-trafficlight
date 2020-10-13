from yad2k.models.keras_yolo import yolo_head
from keras.models import load_model
from Detection_Function import *
from TrafficLight_Function import *
from Mysql_Data import *  # 目前只导入登录程序,和数据库操作程序,后续补充完方法后完全导入

"该文件为程序线程执行文件，可以在此修改进程"

def main_1():

    sess = K.get_session()

    class_names = read_classes("model_data/coco_classes.txt")
    anchors = read_anchors("model_data/yolo_anchors.txt")
    image_shape = (480., 640.)
    # 该电脑的摄像头像素为（480，640）

    yolo_model = load_model("model_data/yolo.h5")

    # 查看层数
    # yolo_model.summary()

    yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))

    scores, boxes, classes = yolo_eval(yolo_outputs, image_shape)

    # 以上为框架启动 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 下面为线程执行 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    print('主线程开始时间：{}\n\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    # print("-----------------------------------------------------------------------------------------------------------")

    yellow_time = threading.Thread(target=task_thread1, name='T1')
    yellow_time.start()
    print('行人识别开始时间：{}\n\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    # time.sleep(4.5)
    # 添加识别程序
    persones = only_detection_number(sess, 'persones',yolo_model,scores,boxes,classes,class_names)
    # 添加人行道绿灯算法
    t = Person_green_light(persones, 10, 1.2)
    # 数据库语句
    cursor.execute("insert into lightdata(dtime,lno,dnumber) values(%s,%s,%s)",(time.strftime("%Y-%m-%d"),1,persones))

    print('行人识别结束时间：{}\n\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    yellow_time.join()

    persones_green_time = threading.Thread(target=task_thread2(t), name='T2')  # 预留五秒给算法做检测使用
    persones_green_time.start()  # 行人绿灯时间启动
    persones_green_time.join()

    wait_time = threading.Thread(target=task_thread3, name='T3')
    wait_time.start()  # wait_time在此处作为一段暂停给算法使用的时间

    print('车辆识别开始时间：{}\n\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    # 添加车行道绿地算法
    cars = only_detection_number(sess, 'cars',yolo_model,scores,boxes,classes,class_names)
    t = Car_green_light(cars, 5, 5, 1, 4, 1)
    # 数据库语句
    cursor.execute("insert into lightdata(dtime,lno,dnumber) values(%s,%s,%s)",(time.strftime("%Y-%m-%d"),2,cars))
    # 数据库语句
    print('车辆识别结束时间：{}\n\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    wait_time.join()  # 主程序暂停等待次程序执行完毕

    cars_green_time = threading.Thread(target=task_thread4(t), name='T')
    cars_green_time.start()
    # 数据库语句
    conn.commit()
    # 数据库语句
    cars_green_time.join()  # 主程序暂停等待次程序执行完毕

    # print("----------------------------------------------------------------------------------------------------------")
    print('主线程结束时间：{}\n\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S")))


def main_2():
    sess = K.get_session()

    class_names = read_classes("model_data/coco_classes.txt")
    anchors = read_anchors("model_data/yolo_anchors.txt")
    image_shape = (480., 640.)
    # 该电脑的摄像头像素为（480，640）

    yolo_model = load_model("model_data/yolo.h5")

    # 查看层数
    # yolo_model.summary()

    yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))

    scores, boxes, classes = yolo_eval(yolo_outputs, image_shape)

    predict_current_time(sess, scores, boxes, classes, yolo_model, class_names)


if __name__ == '__main__':

    "程序在此启动执行"

    # 登录MYSQL数据库
    conn = pymysql.connect(**connection('test'))
    # 获取数据库操作游标
    cursor = conn.cursor()

    cycles = int(input('the cycles index :'))  # 模拟循环次数
    count = 0
    while True:
        main_1()
        count += 1
        if count == cycles:
            break

    # 以倒序显示后四条data数据
    # cursor.execute("select * from lightdata order by dno limit 0,4")
    # print(cursor.fetchall())

    # 关闭数据库操作游标
    cursor.close()
    # 关闭数据库连接
    conn.close()

    # main_2()

