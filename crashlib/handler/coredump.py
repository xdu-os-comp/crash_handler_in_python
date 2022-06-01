import os
from ..report import report_app, error_log
from ..config import cfgglobal
from ..utils import EventMgr, SubscribeEvent

@SubscribeEvent({})
async def crash_handler(e: EventMgr, pid, sig, ulimit, fd):
    '''Save coredump from fd.'''

    written = False

    with report_app(pid) as rpt:
        BLOCK, size = 0x20000, 0
        core_path = rpt('core')
        with open(core_path, 'wb') as f:
            f.seek(0, os.SEEK_SET)
            while True:
                buf = os.read(fd, BLOCK)
                size = size + len(buf)
                if ulimit >= 0 and size > ulimit:
                    error_log('Aborting coredump writing, size exceeds current limit %d', ulimit)
                    break
                if not buf:
                    written = True
                    break
                f.write(buf)

        # Notify other handlers that need the coredump file.
        await e.notify('coredump', written and rpt or None)

        if written:
            if cfgglobal.get_inst().get_bool('compress', 'coredump'):
                import gzip
                core_gz_path = rpt('core.gz')
                with gzip.open(core_gz_path, 'wb') as g:
                    with open(core_path, 'rb') as f:
                        g.writelines(f)
                        # If no exception occurs, delete origin core file.
                        os.unlink(core_path)
        else:
            os.unlink(core_path)

        # Notify other handlers that need the coredump file.
        await e.notify('logging', rpt or None)

