# MyPythonTools
Some tools writen in python

1.AccountByName2ByDate is highly customized,  it may not meet your requirement.

2.EncryptQuickSrc is a tool for encrypting quick-cocos2d-x source code, it's tested on quick-3.3-final.
usage: python main.py -i <src directory, just lua src dir> -o <output encrypted zip file path> -k <xxtea key> -s <sign>
It encrypt the lua source files without compiling. 
So you don't need to worry about that you are running you game on lua or luajit.

EncryptQuickSrc是一个quick-cocos2d-x的加密工具，是参照quick-3.3-final的加密方法写的。
它不会编译lua源文件，而只是加密它。
quick运行时也只是解密并运行lua源代码。已经在quick-3.3-final上测试OK没问题。
