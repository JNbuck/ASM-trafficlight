# ASM - 智能红绿灯系统

[![AUR](https://img.shields.io/badge/GPL-v3-red)](https://github.com/JNbuck/ASM-trafficlight/blob/master/LICENSE)
[![](https://img.shields.io/badge/Author-JNbuck团队-orange)](https://github.com/JNbuck)
[![](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/JNbuck/ASM-trafficlight)
[![GitHub stars](https://img.shields.io/github/stars/JNbuck/ASM-trafficlight?style=social)](https://github.com/JNbuck/ASM-trafficlight)
[![GitHub forks](https://img.shields.io/github/forks/JNbuck/ASM-trafficlight?style=social)](https://github.com/JNbuck/ASM-trafficlight)

> 这是作者参加ASM期间为了方便代码管理而创建的开源项目，希望其他参赛队伍不要盗用

## 目录

- [背景](#背景)
- [安装方法](#安装方法)
- [使用方法](#使用方法)
- [维护者](#维护者)
- [贡献](#贡献)
- [联系交流方式](#联系交流方式)
- [LICENSE](#LICENSE)

## 背景

**ASM题目之一：红绿灯智能算法问题** 

![problem](https://github.com/JNbuck/ASM-trafficlight/blob/master/images/problem.jpg)

## 安装方法

由于目前只是测试性程序，如果需要使程序稳定运行在本机可以使用以下方法

> * 使用该文件前，需要在使用设备上安装环境，包括tensorflow开发环境，keras开发环境，opencv包等一系列环境，使用pip便捷安装即可
>
> * 将本项目使用`git clone SSH路径`克隆到使用的设备上
>
> * 由于模型数据过大，已经将模型数据放置在百度网盘
>
>   >链接：https://pan.baidu.com/s/1lMK9qDhdIT3Rd64uPh2IFw 
>   >提取码：umny
>
>   通过百度网盘下载得到该yolo.h5文件，该文件是该yolo目标识别模型的参数集，将该文件放置在根目录model_data文件夹中即可
>
> * 安装mysql数据库，并保持该数据库处于启动状态，下载以下链接内的数据库，并导入到mysql数据库中
>
>   >链接：
>   >提取码：


## 使用方法

>* 运行TrafficLight_Running.py文件即可启动该红绿灯程序
>* 在TrafficLight_Running.py文件中，有个主程序main，将其中的connection中的test改为test1，即可登录作者的数据库进行访问，目前该方法无法使用，因为作者还在申请固定域名。
>* 使用DrawBoxes_Function中的已经写好的完整方法可以实现实时监测，请自行添加到main方法中运行

## 维护者

@[**Ho-george**](https://github.com/Ho-george)

@[**JNbuck** Junduo Xu](https://github.com/JNbuck)

## 贡献

**希望以后有贡献**

## 联系交流方式

**技术疑问交流**

>QQ交流群 ： 
>
>作者博客：
>
>requestes作者！！！



## LICENSE

* 个人学习使用遵循GPL开源协议
* 商用需联系作者授权











