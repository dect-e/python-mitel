import time
from threading import Lock


class LastPPAction:
    ppn = None
    trType = None
    rfpId = None
    relTime = None
    localTimeStamp = None  # not specified by AXI; added locally to keep relTime meaningful
    _ommclient = None
    _changes = None
    _changelock = Lock()

    def __init__(self, ommclient, attributes=None):
        self.__dict__["_ommclient"] = ommclient
        self.__dict__["_changes"] = {}
        if attributes is not None:
            self._init_from_attributes(attributes)

        self.__dict__["localTimeStamp"] = time.time()

    def __getattr__(self, item):
        return self.__dict__[item]

    def __setattr__(self, key, value):
        if key == "uid" and "uid" in self.__dict__:
            raise Exception("Cannot change uid !")
        with self._changelock:
            self._changes[key] = value
            self.__dict__[key] = value

    def _init_from_attributes(self, attributes):
        for key, val in list(attributes.items()):
            self.__dict__[key] = val

    def get_attributes(self):
        attributes = {}
        for key, val in list(self.__dict__.items()):
            if "_" in key:
                attributes[key] = val
        return attributes

    def commit(self):
        if not self._changes:
            return True
        with self._changelock:
            for change in self._changes:
                print(change)
            return True
