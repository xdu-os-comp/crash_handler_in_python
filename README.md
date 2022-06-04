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

## 原理
1. 当系统内核检测到有程序崩溃的时候，他会读取 `/proc/sys/kernel/core_pattern`设置，找到里面的需要把崩溃数据提取到哪里。

2. 他会将数据通过管道输出到那个地方，本程序的 `handler` 程序被启动，开始处理过程。

3. 处理器先根据传入的的信息在 `/var/log/pycrash-report`下面生成文件夹，在那里存储从管道传过来的崩溃数据(coredump)。

4. 当 coredump 收集完毕/到达 ulimit 限制而终止后，通知信息收集程序开始分析 coredump。

5. 收集的信息如下：

   1. 系统信息：生成时间，生成时间戳，机器架构，系统发行版和版本号，内核版本号，标准 C 库版本号，电脑安装的所有桌面，电脑 CPU 型号，内存大小，交换分区大小，ulimit 大小

   2. 不需要 coredump 就能读取的信息：进程名称，进程可执行文件所在地址，进程执行的命令行命令，进程退出信号，进程的 PID、PPID、UID、GID，其父进程和子进程

   3. 需要读取 coredump 才能获取的信息：寄存器信息，内存地址映射，堆栈和线程信息(通过 gdb)，该 coredump 是否压缩过

   信息最后会输出为一个 information.js 文件，存在和 coredump 相同的目录下。

6. 当信息成功后，如果需要压缩，通知压缩函数开始使用 gz 算法压缩。

7. 将崩溃信息的简要版本输出到系统日志中。

8. 如果是在刚开始有报错的话，输出的错误日志会在`/var/log/pycrash.log`下面。其他的错误日志会在 `/var/log/pycrash-report`下面。