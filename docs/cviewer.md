# `cviewer`文档

项目根目录下的`cviewer`可用于获取已记录的崩溃信息。

```plaintext
usage: cviewer [-h] [--no-legend] [--no-fold] [--mappings] [--json {pretty,short,off}] [--debugger DEBUGGER]
               [-A DARG] [-n N] [-1] [-S SINCE] [-r] [-o OUTPUT]
               COMMAND ...

positional arguments:
  COMMAND               operation
    list                List available records (default)
    info                Show detailed information about the specified record
    dump                Dump raw coredump file to stdout
    debug               Start a debugger for the specified record

options:
  -h, --help            show this help message and exit
  --no-legend           Do not print the column headers
  --no-fold             Do not limit column width
  --mappings            Show mappings field if it exists
  --json {pretty,short,off}
                        Generate JSON output
  --debugger DEBUGGER   Use the given debugger
  -A DARG, --debugger-arguments DARG
                        Pass the given arguments to the debugger
  -n N                  Show maximum number of rows
  -1                    Show information about most recent entry only
  -S SINCE, --since SINCE
                        Only print records since the date
  -r, --reverse         Show the newest entries first
  -o OUTPUT, --output OUTPUT
                        Output redirection

```

## 子命令

对于每一个子命令，后面都可以指定一系列匹配字串，例如`cviewer list 123 foo`中有`123`和`foo`。

对于每一个字串，与下列信息之一对应就算匹配：

* `PID`
* 程序名称（完全）
* 程序路径（完全）

如果有多个字串，则仅显示匹配全部字串的记录。

* `list`（默认）

  显示记录列表。

  * `--no-legend`

    不显示列表的表头。

  * `--no-fold`

    对于较长的目录，不要进行换行。这对于使用`gerp`等命令抓取信息时特别有用。

  * `-n N`

    显示最多`N`条记录。

  * `-1`

    仅显示一条记录。这等价于`-n 1`。

  * `-S SINCE, --since SINCE`

    `SINCE`是`today`或`yyyy-mm-dd`的格式。只获取指定时间之后的记录。

  * `-r, --reverse`

    将列表逆序翻转。

* `info`

  显示第一个匹配的项目的详细信息。

  * `--mappings`

    显示`mappings`字段。此信息在一般的程序中很冗长，所以默认将其关闭。

  * `--json {pretty,short,off}`

    * `pretty`

      带缩进的`json`格式。

    * `short`

      尽可能短的`json`格式。

    * `off`

      可读的输出（不是`json`）。

  * `-S SINCE, --since SINCE`

    与`list`中的相同。

  * `-r, --reverse`

    与`list`中的相同。

* `dump`

  输出第一个匹配的项目的`coredump`（如果有）。

  * `-o OUTPUT, --output OUTPUT`

    `dump`的输出位置，默认为标准输出。

  * `-S SINCE, --since SINCE`

    与`list`中的相同。

  * `-r, --reverse`

    与`list`中的相同。

* `debug`

  调试第一个匹配的项目的`coredump`（如果程序和`coredump`都存在）。程序会把它们传入调试器。

  * `--debugger DEBUGGER`

    指定`debugger`，默认为`gdb`。

  * `-A DARG, --debugger-arguments DARG`

    自定义传给调试器的参数。

  * `-S SINCE, --since SINCE`

    与`list`中的相同。

  * `-r, --reverse`

    与`list`中的相同。
