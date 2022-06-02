from ..utils import EventMgr, SubscribeEvent, create_time
from ..config import cfgglobal
from ..report import report_app
import pwnlib.elf.corefile as core
import psutil, platform, signal, json, subprocess, time

@SubscribeEvent({'coredump'})
async def crash_handler(e: EventMgr, pid, sig, ulimit, fd):
    # Connect information from the information we had.

    information = {}

    # Process-independent information
    information['time'] = create_time().ctime()
    information['timestamp'] = create_time().timestamp()
    information['arch'] = platform.machine()
    osi = platform.freedesktop_os_release()
    information['dist'] = osi['NAME']
    information['dist_ver'] = osi['PRETTY_NAME']
    information['kernel'] = platform.uname()[2]
    information['libc_ver'] = platform.libc_ver()[0] + ' ' + platform.libc_ver()[1]
    information['desktop_installed'] = subprocess.getstatusoutput("ls /usr/bin/*session")[1]
    # I did not able to detect the dual physical cpus, but it is pretty rear.
    information['processor'] = subprocess.getstatusoutput("cat /proc/cpuinfo | grep name | head -n 1")[1].lstrip("model name      : \t")
    information['memory_total'] = psutil.virtual_memory()[0]
    information['swap_total'] = psutil.swap_memory()[0]
    information['ulimit'] = ulimit

    # Process information which could be attached without coredump
    p = psutil.Process(pid)
    information['name'] = p.name()
    information['exec_path'] = p.exe()
    # We have to concat arguments manually because we have no idea getting cmd string
    information['command'] = ' '.join(p.cmdline())
    # Save original argument list. This is useful if some arg contains spaces.
    information['argv'] = p.cmdline()
    information['signal'] = {
        'name': signal.Signals(sig).name,
        'id': sig,
    }
    information['pid'] = p.pid
    information['ppid'] = p.ppid()
    temp = p.uids()
    information['uid'] = {'real': temp.real, 'effective': temp.effective, 'saved': temp.saved}
    temp = p.gids()
    information['gid'] = {'real': temp.real, 'effective': temp.effective, 'saved': temp.saved}
    # The same as his parents and children
    temp1 = []
    parents = p.parents()
    for i in parents:
        h = {}
        h["pid"]  = i.pid
        h["name"] = i.name()
        temp1.append(h)
    information['parents'] = temp1

    temp2 = []
    children = p.children()
    for i in children:
        h = {}
        h["pid"]  = i.pid
        h["name"] = i.name()
        temp2.append(h)
    information['children'] = temp2

    # Coredump information
    coredump_path = await e.wait('coredump')
    if coredump_path:
        to_be_read = core.Coredump(coredump_path)

        # Get registers in hex, so more codes are needed to write here:-P
        a = to_be_read.registers
        temp = []
        for i in a.values():
            temp.append(hex(i))
        information['registers'] = dict(zip(list(a.keys()),temp))
        temp.clear()

        # Get mappings
        data = to_be_read.mappings
        for i in data:
            d = {}
            d['name']  = i.name
            d['start'] = hex(i.start)
            d['stop']  = hex(i.stop)
            d['page_offset'] = hex(i.page_offset)
            d['size']  = hex(i.size)
            d['flags'] = hex(i.flags)
            temp.append(d)
        information['mappings'] = temp

        # Get backtrace using gdb
        command = "gdb " + information['exec_path'] + " " + coredump_path + " --ex \"thread apply all bt full\" --batch"
        information['gdb_exec_operation'] = command
        # Add exception checks.
        try:
            subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
            subp.wait(5)
            if subp.poll() == 0:
                information['gdb_backtrace'] = subp.communicate()[0]
            else:
                information['gdb_backtrace'] = "Exec failed!"
        except:
            pass # May there is no gdb present.

    with report_app(pid) as rpt:
        if coredump_path:
            compressed = cfgglobal.get_inst().get_bool('compress', 'coredump')
            information['coredump'] = {
                'path': rpt(compressed and 'core.gz' or 'core'),
                'compressed': compressed,
            }
        to_save = rpt("information.json")
        print(f"Saving information.json report to ",to_save)
        with open(to_save,"w") as fp:
            json.dump(information,fp,indent=4,separators=(',',':'))
            print("Lonely day with my poor laptop")

