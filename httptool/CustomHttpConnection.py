import httplib
import DnsManager
import socket
import ssl
class CustomHTTPConnection(httplib.HTTPConnection):
  def connect(self):
    self.sock = socket.create_connection((DnsManager.resolve(self.host),self.port),self.timeout)
class CustomHTTPSConnection(httplib.HTTPSConnection):
  def connect(self):
    sock = socket.create_connection((DnsManager.resolve(self.host), self.port), self.timeout)
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)
