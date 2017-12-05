class Client(object):
    socket = None
    ip = ""
    buffer = ""
    lastcheck = 0

    def __init__(self, socket, ip, buffer, lastcheck):
        self.socket = socket
        self.ip = ip
        self.buffer = buffer
        self.lastcheck = lastcheck