# Version 3

本次版本不涉及代码修复和功能修改，version2可以正常运行标准绘图源程序    
    
在完成作业要求的基础上，本次更新增加了**自定义颜色**的语法    
即    
**FOR T FROM T_start TO T_end STEP T_step DRAW (Point_x, Point_Y)**    
**[OF (RED|GREEN|BLUE|YELLOW|BLACK)]**

更改内容如下
 - `mylexer` 模块新增记号类别 `TokenType` : **OF**，**RED**，**GREEN**，**BLUE**，**YELLOW**， **BLACK**
 - `mylexer` 模块新增字符与记号的字典映射 `TokenTypeDict` :
   - OF = Token(TokenType.OF, "OF")
   - RED = Token(TokenType.COLOR, "RED")
   - GREEN = Token(TokenType.COLOR, "GREEN")
   - BLUE = Token(TokenType.COLOR, "BLUE")
   - YELLOW = Token(TokenType.COLOR, "YELLOW")
   - BLACK = Token(TokenType.COLOR, "BLACK")
 - `myparser` 模块作少量改动，`ForStatement` 方法新增颜色识别语句，将获取颜色结果传给 `Painter` 
 - `mypainter` 模块内的 `paint` 方法
   - plt.plot(Painter.Points['X'], Painter.Points['Y'], '.'+Draw_color)
   - 参考自 https://blog.csdn.net/qiurisiyu2016/article/details/80187177
   - 第三个参数  'r', 'g', 'b', 'k'(Black),'y'(Yellow) 
   - '.' 点标记  ',' 像素点
		
