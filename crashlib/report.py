import shutil
from .utils import get_internal_path, LocationWrapper
from .config import cfgglobal
from datetime import datetime
from filelock import FileLock
import io, os, sys, time, json, psutil, inspect

_path = get_internal_path(cfgglobal.get_inst().get('location', 'report'))
report_root = LocationWrapper(_path)
'''Make sure the report path exists.'''

def report_app(pid):
    '''Make sure the report path for pid exists.'''

    global _path
    time_pattern = cfgglobal.get_inst().get('time_pattern', 'report')
    exe = psutil.Process(pid).name()
    folder = '%s-%s-%d' % (datetime.now().strftime(time_pattern), exe, pid)
    return LocationWrapper(os.path.join(_path, folder))

def init_report(pid):
    '''Create folder for further report and add record.
    
    It will redirect stdout and stderr if they are not tty.'''

    with report_root as root:
        with report_app(pid) as rpt:
            list_path, lock_path = root('list'), root('list.lck')
            with FileLock(lock_path):
                report_count = cfgglobal.get_inst().get_int('maximum', 'report')
                records = []
                try:
                    with open(list_path, 'r') as f:
                        records = json.load(f)
                except:
                    pass # Ignore.

                # If records is not list, abort parsing.
                if not isinstance(records, list):
                    records = []

                # Limit record count.
                if report_count > 0:
                    records.reverse()

                    while len(records) + 1 > report_count:
                        record = records.pop()
                        if 'location' in record:
                            location = record['location']
                            # Prevent accidental deletion of files not in the report path.
                            if not os.path.isabs(location):
                                location_abs = root(location)
                                if os.path.isdir(location_abs):
                                    try:
                                        shutil.rmtree(location_abs, ignore_errors=True)
                                    except Exception as e:
                                        error_log('Fail to remove %s: %s', location, str(e))

                    records.reverse()

                # If report is allowed, add the record.
                if report_count:
                    records.append({
                        'location': os.path.basename(rpt.get_location()),
                        'pid': pid,
                    })

                with open(list_path, 'w') as f:
                    json.dump(records, f, indent=2)
            link = root('0.latest')
            try:
                os.unlink(link)
            except:
                pass
            os.symlink(rpt.get_location(), link)
            if not os.isatty(2):
                log = rpt('log')
                try:
                    f = os.open(log, os.O_WRONLY | os.O_CREAT, 0o644)
                except OSError:  # on a permission error, don't touch stderr
                    return
                if sys.stdout: sys.stdout.flush()
                os.dup2(f, 1)
                if sys.stderr: sys.stderr.flush()
                os.dup2(f, 2)
                sys.stderr = os.fdopen(2, 'wb')
                if sys.version_info.major >= 3:
                    sys.stderr = io.TextIOWrapper(sys.stderr)
                sys.stdout = sys.stderr

def error(raw_msg):
    '''Print out an error message.'''

    if sys.stderr:
        print('ERROR: %s' % raw_msg, file=sys.stderr)

def error_log(msg, *args):
    '''Output something to the error log.'''

    caller = inspect.getframeinfo(inspect.currentframe().f_back)
    error('%s:%d(pid %d) %s: %s' % (
        os.path.basename(caller.filename),
        caller.lineno,
        os.getpid(),
        time.asctime(),
        msg % args
        ))
