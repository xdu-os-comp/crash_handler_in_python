# crash_handler_in_python 
一个使用了 Python 实现的 Linux Coredump 软件。

Written by killertimer, additional programming by SuperBart.

Special thanks to Pierre.

## 依赖
pwntool psutil python-filelock gdb python-systemd

## 使用方式
`echo "|/path/to/crash_handler_in_python/chandler %p %s %c" > /proc/sys/kernel/core_pattern `

使用 `cviewer`查看

## 保存路径
默认是在  `/var/log/pycrash-report`文件下面存储`coredump`信息，这个可以在配置文件 `config.ini`里面修改。

程序默认报错是在 `/var/log/pycrash.log`。
