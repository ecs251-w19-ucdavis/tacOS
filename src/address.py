M = 20
import hashlib as h

class Address(object):
  def __init__(self, ip, port):
    self.ip = ip
    self.port = int(port)

  def __hash__(self):
    return int(bin(int(h.sha1('{}:{}'.format(self.ip, self.port).encode()).hexdigest(), 16))[:M], 2)
    # return int(bin(hash(("{}:{}".format(self.ip, self.port))))[:M], 2)
    # return hash(("{}:{}".format(self.ip, self.port)))

  def __cmp__(self, other):
    return other.__hash__() < self.__hash__()

  def __eq__(self, other):
    return other.__hash__() == self.__hash__()

  def __str__(self):
    return "{}:{}".format(self.ip, self.port)
