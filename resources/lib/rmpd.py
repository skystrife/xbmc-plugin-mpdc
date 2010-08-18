import socket
import mpd

# reconnecting wrapper for mpd client
class RMPDClient(mpd.MPDClient):
    def __init__(self):
        self._host = None
        self._port = None
        self._password = None
        super(RMPDClient, self).__init__()

    def __getattr__(self, attr):
        obj = super(RMPDClient, self).__getattr__(attr)
        if not callable(obj):
            return obj
        return lambda *args: self._wrap(obj, args)

    def _wrap(self, func, args):
        try:
            return func(*args)
        except (socket.error, mpd.MPDError):
            self._reconnect()
            return func(*args)

    def _reconnect(self):
#        print "Connection error (timeout), reconnecting..."
        self.disconnect()
        self.connect(self._host, self._port)
        if not self._password == None:
			self.password(self._password)

    def connect(self, host, port):
        self._host = host
        self._port = port
        super(RMPDClient, self).connect(host, port)

    def password(self, password):
        self._password = password
        # FIXME: UGLY, requires knowledge of base class implementation details
        super(RMPDClient, self).__getattr__("password")(password)
