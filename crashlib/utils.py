import os.path, sys, asyncio

def get_internal_path(name):
    '''Get absolute file path inside the install directory.'''

    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), name)

class LocationWrapper:
    def __init__(self, dir):
        self._dir = dir

    def get_location(self):
        return self._dir

    def __enter__(self):
        os.makedirs(self._dir, exist_ok=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, file):
        return os.path.join(self._dir, file)


class EventMgr:
    '''Manage events during tasks running.'''
    def __init__(self, waits):
        self._events = {}
        for k, v in waits.items():
            # (count, event for wait, event for notify)
            if v != 0:
                self._events[k] = [v, asyncio.Future(), asyncio.Future()]

    async def notify(self, event, *args):
        if event not in self._events:
            return # Return directly if there are no coroutines waiting.
        self._events[event][1].set_result(args)
        await asyncio.ensure_future(self._events[event][2])

    async def wait(self, event):
        if event not in self._events:
            raise NameError(f'No event named {event}')
        future = self._events[event][1]
        await asyncio.ensure_future(future)
        self._events[event][0] = self._events[event][0] - 1
        if not self._events[event][0]:
            self._events[event][2].set_result(None)
        result = future.result()
        if len(result) == 0:
            return
        elif len(result) == 1:
            return result[0]
        else:
            return result

def run_tasks(funcs, *args):
    '''Run the event loop until coroutines in funcs are done or exception occurs.'''

    futures, waits = [], {}
    for func in funcs:
        if isinstance(func, tuple):
            for event in func[1]:
                waits[event] = waits.get(event, 0) + 1
            func = func[0]
        if asyncio.iscoroutinefunction(func):
            futures.append(func)
        else:
            func(*args)

    # Handle async funcs.
    if futures:
        loop = asyncio.get_event_loop()
        e = EventMgr(waits)
        done, pending = loop.run_until_complete(asyncio.wait([future(e, *args) for future in futures], return_when=asyncio.FIRST_EXCEPTION))

        # If an exception is raised, there will be some pending coroutines,
        # so we should cancel them.
        for routine in pending:
            routine.cancel()

        for routine in done:
            # If the future is done and has an exception set, this exception is raised.
            routine.result()

        loop.close()

def SubscribeEvent(events):
    '''Decorator for async function of run_tasks.'''
    return lambda f : (f, events)
