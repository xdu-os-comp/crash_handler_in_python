from .cfgmgr import CfgMgr
from ..utils import get_internal_path

_cfg_global = None

def get_inst():
    '''Get config.ini settings or default settings.'''

    global _cfg_global
    if not _cfg_global:
        _cfg_global = CfgMgr(get_internal_path('config.ini'), {
            'report': {
                'maximum': 5,
                'location': '/var/log/pycrash-report',
                'time_pattern': '%Y%m%d%H%M%S',
            },
            'coredump': {
                'compress': True
            }
        })
    return _cfg_global
