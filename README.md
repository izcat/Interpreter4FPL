# Interpreter For Functional Painting Language
> 西电 编译原理大作业

## 实验目的
实现函数绘图语言的解释器，通过实验加深对编译器构造原理和方法的理解，巩固所学知识。
 -	会用正规式设计简单语言的词法
 -	会用产生式设计简单语言的语法
 -	会用递归下降子程序编写语言的解释器


    
## 实验要求

### 语句原则：

1. 各类语句可以按任意次序书写，且语句以分号结尾。源程序中的语句以它们出现的先后顺序处理。

2.  ORIGIN、ROT和SCALE 语句只影响其后的绘图语句，且遵循最后出现的语句有效的原则。
       例如，若有下述ROT语句序列： 	
            ROT IS 0.7 ；
            ROT IS 1.57 ；
       则随后的绘图语句将按1.57而不是0.7弧度旋转。 

3. 无论ORIGIN、ROT和SCALE语句的出现顺序如何，图形的变换顺序总是：比例变换→旋转变换→平移变换 

4. 语言对大小写不敏感，例如for、For、FOR等，均被认为是同一个保留字。 

5. 语句中表达式的值均为双精度类型，旋转角度单位为弧度且为逆时针旋转，平移单位为点。  

### 循环绘图（FOR-DRAW ）语句
  语法：FOR T FROM 起点 TO 终点 STEP 步长 DRAW(横坐标, 纵坐标);

  语义：令T从起点到终点、每次改变一个步长，绘制出由(横坐标，纵坐标)所规定的点的轨迹。

  举例：FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));

  说明：该语句的作用是令T从0到2*PI、步长 PI/50，绘制出各个点的坐标(cos(T)，sin(T))，即一个单位圆。

### 比例设置(SCALE)语句
  语法：SCALE IS (横坐标比例因子，纵坐标比例因子);

  语义：设置横坐标和纵坐标的比例，并分别按照比例因子进行缩放。

  举例：SCALE IS (100, 100);

  说明：将横坐标和纵坐标的比例设置为1:1，且放大100倍。

### 坐标平移(ORIGIN)语句
  语法：ORIGIN IS (横坐标，纵坐标); 

  语义：将坐标系的原点平移到横坐标和纵坐标规定的点处。

  举例：ORIGIN IS (360, 240); 

  说明：将原点从(0, 0)平移到(360, 240) 处

### 角度旋转(ROT)语句
  语法：ROT  IS 角度； 

  语义：逆时针旋转角度所规定的弧度值。
      具体计算公式：
      旋转后X=旋转前X*COS(角度)+旋转前Y*SIN(角度) 
      旋转后Y=旋转前Y*COS(角度)-旋转前X*SIN(角度)
    
  举例：ROT IS PI/2;

  说明：逆时针旋转PI/2，即逆时针旋转90度。

### 注释语句 
  作用：便于理解；
        屏蔽暂时不需要的语句。    
  语法：//  This is a comment line   
        或   --  此行是注释   
  语义：// 或 -- 之后，直到行尾，均是注释   



-------



## 实验过程
    
### Version 1
代码详见 https://github.com/izcat/Interpreter4FPL/tree/master/version1

完成词法分析 

#### 词法分析器功能

- 输入：函数绘图语言源程序，以字符串形式传递给 `Lexer` 参数
- 输出：返回源程序进行词法分析得到的全部 Token，类型为列表

#### Update:

  此版本 `Lexer` 会无法正确识别带小数点的浮点数！在version2中的 `Lexer` 才是正确写法！

    
### Version 2
代码详见 https://github.com/izcat/Interpreter4FPL/tree/master/version2

已实现实验要求的函数绘图语言的全部功能
解释器执行的第一个程序结果（显示 'OK' 字样）：
![图片](https://github.com/izcat/Interpreter4FPL/blob/master/version2/0testOK.png "结果")


#### 修复Bug

  由于新加入主界面的模块 `main.py` 无法正常 import 写好的 `parser`模块，因为会与 Python 的同名库冲突。   
  将全部模块改名，加上'my'前缀

#### 不足

  词法分析器与语义分析器没有完全分离，本解释器在语法分析阶段，未生成源代码的整体语法树，直接将绘制的点信息交给painter处理  
  缺少异常处理机制  
  没有完全面向对象开发
    
    
### Version 3
代码详见 https://github.com/izcat/Interpreter4FPL/tree/master/version3

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
    
    
### Version 4
代码详见 https://github.com/izcat/Interpreter4FPL/tree/master/version4

改进内容：

- 在version3的基础上，分离语法分析器 `myparser` 模块与语义分析器 `mypainter` 模块
- 重新设计了语法分析过程中的运行提示，增加了层级level参数，使递归调用的输出信息更友好
- 重写了 `mypainter` 模块，改用面向对象方式
  - `Painter` 类 接收绘图源程序代码，调用语法分析器 `myparser.Parser`
  - 将获取到的语法树交给 `analyse` 方法进行语义分析
  - 语义分析完成后，`showPic` 执行绘图
- 改进 `main` 程序入口模块，增加了打开文件选项，可以直接选择写好绘图源程序打开

    
## 结果展示
    
![pic3](https://github.com/izcat/Interpreter4FPL/blob/master/test%26pic/几何标志.png)
![pic2](https://github.com/izcat/Interpreter4FPL/blob/master/test%26pic/五环.png)
![pic1](https://github.com/izcat/Interpreter4FPL/blob/master/test%26pic/test0.jpg)


