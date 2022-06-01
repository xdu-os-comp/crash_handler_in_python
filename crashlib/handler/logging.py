import os, json
from systemd import journal
from ..report import report_app, error_log
from ..config import cfgglobal
from ..utils import EventMgr, SubscribeEvent

'''
This is an example of the post-coredump activeity.
If you prefer a instant window show up, do not use this way.
'''
@SubscribeEvent({'logging'})
async def crash_handler(e: EventMgr, pid, sig, ulimit, fd):
    rpt = await e.wait('logging')
    to_show = rpt("information.json")
    print("Logging something to the syslog...")
    journal.send("[pycrash] A application had crashed! Here's the brief information...",PRIORITY=3)
    with open(to_show,'r') as fp:
        data = json.load(fp)
        journal.send("[pycrash] Process {} named {} had exit with signal {} in {}.".format(data['pid'],data['name'],data['signal'],data['time']),PRIORITY=3)
        journal.send("[pycrash] Its execution path is {} and the full command is {}.".format(data['exec_path'],data['command']),PRIORITY=3)
        journal.send("[pycrash] We have a coredump at {}, and the information.js is in the same folder.".format(data['coredump']),PRIORITY=3)
