
__all__ = ['process_crash']

from pathlib import Path
from pkgutil import iter_modules
from importlib import import_module
from ..utils import run_tasks
import sys

# Load all modules under current folder and collect functions named 'crash_handler'.
handlers_dir = str(Path(__file__).resolve().parent)
handlers = []
for (_, path, _) in iter_modules([handlers_dir]):
    path = f'{__name__}.{path}'
    import_module(path)
    # print(f'Loaded {path}')
    mod = sys.modules[path]
    for attr_name in dir(mod):
        if attr_name == 'crash_handler':
            attr = getattr(mod, attr_name)
            handlers.append(attr)
# print(handlers)

def process_crash(pid, sig, ulimit, fd = 0):
    '''Collect data from crashed program via pid, sig...
    
    Handler should be declared as follows:

    `def handler(pid, sig, ulimit, fd)`
    `async def handler(e : EventMgr, pid, sig, ulimit, fd)`
    '''

    run_tasks(handlers, pid, sig, ulimit, fd)
