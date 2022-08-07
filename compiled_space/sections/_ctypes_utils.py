import logging
import ctypes



class CStructure(ctypes.LittleEndianStructure):
    def __init__(self, data):
        super(CStructure, self).__init__()
        assert ctypes.sizeof(self) == self._size_, (ctypes.sizeof(self), self)
        if isinstance(data, dict):
            self.from_dict(data)
        else:
            self.from_bin(data)

    def to_bin(self):
        try:
            return buffer(self)[:]
        except Exception:
            return bytes(self)

    def to_dict(self):
        result = {}
        for field in self._fields_:
            name = field[0]
            attr = getattr(self, name)
            if hasattr(attr, '_length_'):
                result[name] = tuple(attr)
            else:
                if isinstance(attr, float): attr = round(attr, 6)
                result[name] = attr
        return result

    def from_dict(self, data):
        for key, val in data.items():
            if hasattr(self, key):
                if hasattr(val, '__len__'):
                    exec('self.%s = tuple(val)' % (key))
                else:
                    exec('self.%s = val' % key)

    def from_bin(self, data):
        ctypes.memmove(ctypes.addressof(self), data, self._size_)
        self.tests()

    def test_failed(self, field, value, expr, expected_value):
        logging.info('\nTest failed')
        logging.info('obj: %s' % self)
        logging.info('field "%s" = %s' % (field, value))
        logging.info('test: %s %s' % (expr, expected_value))

    def tests(self):
        if not hasattr(self, '_tests_'):return
        for field, testsDict in self._tests_.items():
            for expr, expected_value in testsDict.items():
                value = getattr(self, field)
                if hasattr(value, '__len__'):
                    for idx, it in enumerate(expected_value):
                        exec('if not value[idx] '+ expr +' it:self.test_failed(field+"[%s]", value, expr, it)' % idx)
                else:
                    if isinstance(value, float): value = round(value, 6)
                    exec('if not value '+ expr +' expected_value:self.test_failed(field, value, expr, expected_value)')
