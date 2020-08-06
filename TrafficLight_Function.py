from math import *
import threading
import time


"该文件为红绿灯的时间分配的一系列方法"


def Car_green_light(cars,speed_time,start_distant,spacing_distance,average_length,response_time):
    "计算车道的绿灯时间"

    # Last_wait_time(即lw_time) 为最后一辆车的等待时间
    lw_time = (cars-1) * sqrt(2 * speed_time *(start_distant - spacing_distance)/30)
    # Last_constant_speed_time(即lcs_time)为最后一辆车匀速行驶到30m/s的时间
    lcs_time =((cars-1) * spacing_distance + cars*average_length - 30*speed_time/2) / 30

    T = lw_time + lcs_time + speed_time + response_time*cars  #总时间

    if(T>=15 and T<=70):
        return T
    elif(T<=15):
        T = 15
        return T
    elif(T>=70):
        T = 70
        return T

def Person_green_light(persones,sidewalk_length,person_speed):
    "计算人行道的绿灯时间"
    # Last_wait_time(即lw_time) 为最后一个人的等待时间
    lw_time = persones/5 + 1
    # walk_time(即w_time) 为一个人走完人行道的时间
    w_time = sidewalk_length / person_speed

    T = lw_time + w_time #总时间

    if(T>=15 and T<=70):
        return T
    elif(T<=15):
        T = 15
        return T
    elif(T>=70):
        T = 70
        return T

def task_thread1(T=5):
    "模拟黄灯时间"
    print("黄灯时间为："+str(T))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print('线程名称：{} 参数：{} 开始时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(int(T))
    print('线程名称：{} 参数：{} 结束时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def task_thread2(T):
    "模拟绿灯时间"
    print("行人绿灯时间为："+str(T))
    T -= 5
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print('线程名称：{} 参数：{} 开始时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(int(T))
    print('线程名称：{} 参数：{} 结束时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def task_thread3(T=5):
    "模拟等待时间"
    print("缓冲时间为："+str(T))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print('线程名称：{} 参数：{} 开始时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(int(T))
    print('线程名称：{} 参数：{} 结束时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def task_thread4(T):
    "模拟绿灯时间"
    print("车辆绿灯时间为：" + str(T))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print('线程名称：{} 参数：{} 开始时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(int(T))
    print('线程名称：{} 参数：{} 结束时间：{}'.format(threading.current_thread(), threading.active_count(),
                                         time.strftime("%Y-%m-%d %H:%M:%S")))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")