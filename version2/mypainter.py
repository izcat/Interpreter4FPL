from expnode import *
import matplotlib.pyplot as plt 
import math

class Painter():
	orx = 0.0
	ory = 0.0
	scx = 1.0
	scy = 1.0
	ang = 0.0
	# 绘制的点横坐标
	Points = dict(X=[], Y=[])  
	# xlist = [] # 绘制的点横坐标
	# ylist = [] # 绘制的点纵坐标
	# 
	def set(Origin_x=0.0, Origin_y=0.0, Scale_x=1.0, Scale_y=1.0, Rot_angle=0.0):
		Painter.orx = Origin_x
		Painter.ory = Origin_y
		Painter.scx = Scale_x
		Painter.scy = Scale_y
		Painter.ang = Rot_angle
		Painter.Points['X'].clear()
		Painter.Points['Y'].clear()  

	def paint(T_start, T_end, T_step, Point_x, Point_y):
		# for T_value in range(T_start, T_end, T_step):
		T_value = T_start
		
		while T_value<=T_end:
			ExpNode.T_value = T_value
			x = Point_x.getValue()
			y = Point_y.getValue()

			# print("(%f, %f)" % (x, y))

			# 坐标变换
			# 比例变换
			x, y = x*Painter.scx, y*Painter.scy
			# 旋转变换
			x, y = x*math.cos(Painter.ang) + y*math.sin(Painter.ang), y*math.cos(Painter.ang) - x*math.sin(Painter.ang)
			# 平移变换
			x, y = x+Painter.orx, y+Painter.ory

			# points.append((x, y))
			Painter.Points['X'].append(x)
			Painter.Points['Y'].append(y)

			# print("(%f, %f)" % (x, y))
			T_value += T_step

	def showPic():
		plt.xlim(xmax=100, xmin=-100)
		plt.ylim(ymax=100, ymin=-100)
		# plt.plot(x,y,format_string,**kwargs) 
		# 第三个参数 https://blog.csdn.net/qiurisiyu2016/article/details/80187177
		# 'r', 'g', 'b', 'k'(Black),'y'(Yellow) 
		# '.' 点标记  ',' 像素点
		plt.plot(Painter.Points['X'], Painter.Points['Y'], 'k.')
		plt.show()

		# 清空点 下次重新绘图
		Painter.Points['X'].clear()
		Painter.Points['Y'].clear()  

		