# Version 4

改进内容：
 - 在version3的基础上，分离语法分析器 `myparser` 模块与语义分析器 `mypainter` 模块
 - 重新设计了语法分析过程中的运行提示，增加了层级level参数，使递归调用的输出信息更友好
 - 重写了 `mypainter` 模块，改用面向对象方式
   - `Painter` 类 接收绘图源程序代码，调用语法分析器 `myparser.Parser`
   - 将获取到的语法树交给 `analyse` 方法进行语义分析
   - 语义分析完成后，`showPic` 执行绘图
 - 改进 `main` 程序入口模块，增加了打开文件选项，可以直接选择写好绘图源程序打开
