from configparser import ConfigParser

class CfgMgr:
    def __init__(self, path, defaults = {}):
        '''Load config from specified file.'''

        if not isinstance(defaults, dict):
            raise TypeError(defaults)
        parser = ConfigParser()
        try:
            parser.read(path)
        except:
            pass
        self._parser = parser
        self._defaults = dict(defaults)

    def get(self, name, section):
        '''Get string value.'''

        parser = self._parser
        try:
            return parser.get(section, name)
        except:
            return str(self._defaults[section][name])

    def get_bool(self, name, section):
        parser = self._parser
        try:
            return parser.getboolean(section, name)
        except:
            return bool(self._defaults[section][name])

    def get_int(self, name, section):
        parser = self._parser
        try:
            return parser.getint(section, name)
        except:
            return int(self._defaults[section][name])

    def get_float(self, name, section):
        parser = self._parser
        try:
            return parser.getfloat(section, name)
        except:
            return float(self._defaults[section][name])

