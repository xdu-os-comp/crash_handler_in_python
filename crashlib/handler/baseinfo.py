from ..utils import EventMgr, SubscribeEvent

@SubscribeEvent({'coredump'})
async def crash_handler(e: EventMgr, pid, sig, ulimit, fd):
    '''Collect info in /proc/$$/*, coredump, ...'''

    coredump_path = await e.wait('coredump')
    # TODO: collect data...
