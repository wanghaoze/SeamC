# SeamC

This is a practice of Seam Carving algorithm

Based on flask & python & HTML & JavaScript.

Other used tools: Linux & Windows & uwsgi & nginx.

We have already implement it onto my Aliyun Server.

You can view our product at  http://39.96.57.111/ 

manage.py is for the Linux version.

app.py for the Windows version.

python version： 3.6.8

Please install the requirements.txt first  
using :
```
pip install -r requirements.txt
```

The SeamCaver.py and SeamCaver_two.py are core code.  
SeamCaver_two.py is based on SeamCaver.py, used jit to acclerate the process  
Usage:
```
python SeamCaver_two.py -resize -im inputImg_path -out outputImg_path  -dy deltaHeight -dx deltaWidth [-vis]
python SeamCaver_two.py -resize -im inputImg_path -out outputImg_path -mask maskImg_path -dy deltaHeight -dx deltaWidth [-vis]
python SeamCaver_two.py -remove -im inputImg_path -out outputImg_path -rmask rmaskImg_path [-vis]
```
example:
```
python SeamCaver_two.py -resize -im output/no-mask-resize2.jpg -out output/no-mask-resize2.jpg -dy 66 -dx -212 -vis
python SeamCaver_two.py -resize -im output/mask-resize2.jpg -out output/mask-resize4.jpg -mask output/mask-resize3.jpg -dy 0 -dx -458 -vis
python SeamCaver_two.py -remove -im output/rmask-remove2.jpg -out output/rmask-remove4.jpg -rmask output/rmask-remove3.jpg -vis
```
## Home Page

![](https://github.com/wanghaoze/SeamC/blob/master/output/homepage.png)

## About us

![](https://github.com/wanghaoze/SeamC/blob/master/output/about-us.png)

## Process tools

### 智能缩放功能用于无蒙版缩放

![](https://github.com/wanghaoze/SeamC/blob/master/output/no-mask-resize.png)

![](https://github.com/wanghaoze/SeamC/blob/master/output/no-mask-resize1.png)

![](https://github.com/wanghaoze/SeamC/blob/master/output/no-mask-resize2.jpg)

原图片

![](https://github.com/wanghaoze/SeamC/blob/master/output/no-mask-resize3.jpg)

效果图

### 保护蒙版功能用于带蒙版缩放

会给图片蒙版处加一正权值缩放，被保护的部分几乎不会改变

![](https://github.com/wanghaoze/SeamC/blob/master/output/mask-resize.png)

![](https://github.com/wanghaoze/SeamC/blob/master/output/mask-resize1.png)



![](https://github.com/wanghaoze/SeamC/blob/master/output/mask-resize2.jpg)

原图片

![](https://github.com/wanghaoze/SeamC/blob/master/output/mask-resize3.jpg)

保护蒙版图

![](https://github.com/wanghaoze/SeamC/blob/master/output/mask-resize4.jpg)

效果图

### 抠图蒙版功能用于物体移除

![](https://github.com/wanghaoze/SeamC/blob/master/output/rmask-remove.png)

![](https://github.com/wanghaoze/SeamC/blob/master/output/rmask-remove1.png)

![](https://github.com/wanghaoze/SeamC/blob/master/output/rmask-remove2.jpg)

原图片

![](https://github.com/wanghaoze/SeamC/blob/master/output/rmask-remove3.jpg)

蒙版图

![](https://github.com/wanghaoze/SeamC/blob/master/output/rmask-remove4.jpg)

效果图

If you have a problem, contact me with whzgoodfellow@gmail.com.

All right reserved. For academic use only. 

Please indicate the source if you used it.  
————————————————  
Copyright statement: This article is an original project of Github blogger "wanghaoze" and Sichuan University Innovation Project Team. It follows the CC 4.0 BY-SA copyright agreement. Please reprint the original source link and this statement for reprint.
Original link: https://github.com/wanghaoze/SeamC 

版权声明：本文为Github 博主「wanghaoze」及四川大学创新项目团队的原创项目，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接： https://github.com/wanghaoze/SeamC 
