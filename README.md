### ASM大赛开发文档遇到问题的总结


1. 开发环境

   > 1. 使用tensorflow安装后与原来的cand环境不吻合，没办法嵌入到其中
   >
   >    解决方法： 使用tensorflow环境后来安装库，或者使用cd 到编译器的cand中python.exe 所在文件夹，然后使用命令`activate tensorflow`激活环境后，重新安装tensorflow合适的版本，命令为`pip install tensorflo`就可以顺利的安装完成

2. pip下载速度慢的问题

   > 由于下载的大多数库都是存在于外国网站的，然后在清华大学镜像站中基本囊括了所有的外国库
   >
   > 解决方法：1. 例如我要安装scipy这个库以往的命令都说`pip install scipy`
   >
   > ​                 现在我们使用`pip install scipy  -i https://pypi.tuna.tsinghua.edu.cn/simple`
   >
   > ​                 通过访问清华大学镜像站来减少下载时间
   >
   >    2. 如果依然卡顿飘红，则在user内添加一个pip文件夹，再在pip文件夹里面添加一个pip.ini文件
   >
   >       然后写入
   >
   >       ```
   >       [``global``]
   >       index``-``url ``=` `https:``/``/``pypi.tuna.tsinghua.edu.cn``/``simple
   >       [install]
   >       trusted``-``host``=``mirrors.aliyun.com
   >       ```



3. keras框架编写的程序，可视化打不开

   > 在排除 1. pudot没有安装 
   >
   > 			2. Graphviz2.38没有安装 
   >    			3. 没有将Graphviz2.39\bin添加到系统变量path
   >
   > 终极解决方法：使用管理员权限打开pycharm，报错来自于pycharm无法调用C盘graphviz的权限
   
4.模型数据的下载将会放在百度云，后续链接会放上来