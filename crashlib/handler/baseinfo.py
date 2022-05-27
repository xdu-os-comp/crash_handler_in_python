from ..utils import EventMgr, SubscribeEvent
import pwnlib.elf.corefile as core
from ..report import report_app
import psutil, platform, signal, json
import subprocess

@SubscribeEvent({'coredump'})
async def crash_handler(e: EventMgr, pid, sig, ulimit, fd):
    '''Collect info in /proc/$$/*, coredump, ...'''
    information = {}
    information['pid'] = pid
    information['platform'] = platform.platform()
    information['signal'] = signal.Signals(sig).name
    information['name'] = psutil.Process(pid).name()
    coredump_path = await e.wait('coredump')
    information['coredump'] = coredump_path
    if coredump_path == None:
        print("Error: Coredump Not Found!")
    else:
        to_be_read = core.Coredump(coredump_path)
        information['exec_path'] = to_be_read.exe.name
        command = "gdb " + information['exec_path'] + " " + coredump_path + " --ex \"thread apply all bt full\" --batch"
        information['gdb_exec_operation'] = command
        subp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        subp.wait(5)
        if subp.poll() == 0:
            information['gdb_backtrace'] = subp.communicate()[0]
        else:
            information['gdb_backtrace'] = "Exec failed!"

    with report_app(pid) as rpt:
        with open(rpt("information.json"),"w+") as fp:
            json.dump(information,fp,indent=4,separators=(',',':'))
            print("Fxxk you!")

