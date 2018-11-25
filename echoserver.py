import sys
import socket
from concurrent.futures import ThreadPoolExecutor

class Server:
  def __init__(self, port, broadcast):
    self.port = port
    self.host = 'localhost'
    self.client_sock = []
    self.broadcast = broadcast
  
  def server_start(self):
    MAX_CLIENT = 100
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      pool = ThreadPoolExecutor(MAX_CLIENT)
    except:
      print("[!] Failed to create thread pool. Terminated")
      exit(-1)
    try:
      self.socket.bind((self.host, self.port))
      self.socket.listen(MAX_CLIENT)
    except:
      print("[!] Failed to bind socket. Terminated")
      exit(-1)
    print("[+] Thread pool created and Socket binded")
    while True:      
      sock, addr = self.socket.accept()
      print("[+] Connection established from {}".format(addr))
      self.client_sock.append(sock)
      pool.submit(self.__communicate__,sock,addr)
  def __broadcast_msg__(self, msg):
    for client in self.client_sock:
      try:
        client.send(msg)
      except:
        client.close()
        self.client_sock.remove(client)

  def __communicate__(self, sock, addr):
    while True:
      data = sock.recv(10000)
      if not data:
        print("[+] Connection from {} closed".format(addr))
        sock.close()
        break
      request = data.decode()
      print("[+] From {} : {}".format(addr, request))
      if broadcast: self.__broadcast_msg__(request.encode())
      else:
        sock.send(request.encode())

def usage():
  print("syntax : python echoserver.py <port> [-b]")
  print("sample : python echoserver.py 1234 -b")

if __name__=="__main__":
  port = 0
  broadcast = False
  if len(sys.argv) not in [2,3]:
    usage()
    exit(-1)
  if len(sys.argv) == 2:
    try:
      port = int(sys.argv[1])
    except:
      usage()
      exit(-1)
  else:
    try:
      port = int(sys.argv[1])
      assert(sys.argv[2] == '-b')
      broadcast = True
    except:
      usage()
      exit(-1)
  
  S = Server(port, broadcast)
  S.server_start()