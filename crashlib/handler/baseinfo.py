from ..utils import EventMgr, SubscribeEvent
import pwnlib.elf.corefile as core
from ..report import report_app
import psutil, platform, signal, json

@SubscribeEvent({'coredump'})
async def crash_handler(e: EventMgr, pid, sig, ulimit, fd):
    '''Collect info in /proc/$$/*, coredump, ...'''
    information = {}
    information['pid'] = pid
    information['platform'] = platform.platform()
    coredump_path = await e.wait('coredump')
    to_be_read = core.Coredump(coredump_path)
    information['signal'] = signal.Signals(sig).name
    information['name'] = psutil.Process(pid).name()

    with report_app(pid) as rpt:
        with open(rpt("information.json"),"w+") as fp:
            json.dump(information,fp)
            print("Fxxk you!")




