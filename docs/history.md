# 开发历史 
我们是在四月下旬开始开发的，当时 Pierre 拉着我认识了老梁，我们仨一起参加了这个竞赛。题目是获取 coredump 并获取信息。

## 开发初期

当时我们对这玩意相当于基本不明白，然后我们查看了很多的东西。包括但不限于 DrKonqi (KDE 程序崩溃程序)，systemd-coredump 的代码，看了两天也没看明白多少。

说到 DrKonqi，我们当时一起分析了这些代码，发现这些代码需要 KCrash。于是我们又看了 KCrash 的代码，我们在那里也没有多少收获，只是知道了这玩意是工作在 systemd-coredump 上面的，而且仅对 KDE 框架开发的程序有效。

我们又看了 systemd-coredump 的代码，终于是有了些收获。

## 获取 coredump
老梁(Killtimer)从 systemd-coredump 和 /proc/sys/kernel/core_pattern 中获知，系统会将崩溃信息输出到标准输出里面。然后他写了一个很简单的 C 语言程序，来获取这些信息。这个程序基本上就是循环读取从标准输出里面获取的信息，然后保存到一个文件里面。这个程序是我们这个项目里面第一个代码，真的就是里程碑意义了。

```c
#include <stdio.h>
#include <string.h>

int main()
{
	FILE *f = fopen("/home/killtimer/Desktop/dmp.txt", "wb");
	if (f)
	{
		unsigned char buf[1024];
		size_t len;
		for (;;)
		{
			len = fread(buf, 1, 1024, stdin);
			if (!len)
				break;
			fwrite(buf, len, 1, f);
		}
		fclose(f);
	}
	return 0;
}
```

## 使用 python 获取信息

我们一开始我们想利用 systemd-coredump 暴露的接口，我们联系了出题的吉老师。吉老师说这个方法很不可行，他给了我们一些已经实现的方案，其中使用 python 开发的 apport 程序引起了我们的注意。正好 python 已经提供了很多的第三方库，来帮助我们获取信息。老梁花了两个晚上的时间，开发出了这个程序的框架。我在这个框架上面，填充了收集信息的功能，和一个输出简要信息到系统日志的功能。我把我信息的格式给他，他写出来了日志查看器。我最后是核实了一遍，确实能在 /var/log 下使用。好的，该交了。

## 最后我的想法

还行吧，虽然这一个多月的开发时间大多被学校的一堆破事给占据了。但在开发时间里，我们的工作还是很有效率的。本人不太精通 python，只能说人家给个框架，我填补一些功能。感谢 Killtimer 和 Pierre 给我这个机会吧。

SuperBart 2022-06-04
