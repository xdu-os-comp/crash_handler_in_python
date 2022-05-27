# crash_handler_in_python 
一个使用了 Python 实现的 Linux Coredump 软件。

## 依赖
pwntool 
python-filelock 
gdb

## 使用方式
`echo "|/path/to/crash_handler_in_python/chandler %p %s %c" > /proc/sys/kernel/core_pattern `

## 保存路径
`"|/path/to/crash_handler_in_python/report` 下面
有个 error 文件，是用来保存最后一次失败的时候报告的错误。

## 原理
TODO