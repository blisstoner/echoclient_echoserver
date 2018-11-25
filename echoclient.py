import sys
import socket
from concurrent.futures import ThreadPoolExecutor

class Client:
  def __init__(self,host,port):
    self.host = host
    self.port = port
  
  def __listen__(self):
    while True:
      response = self.sock.recv(10000)
      if not response:
        print("[!] Connection closed")
        exit(0)
      print(response.decode())

  def __send__(self):
    while True:
      msg = input()
      self.sock.send(msg.encode())
  
  def __connection__(self):
    try:
      pool = ThreadPoolExecutor(2)
    except:
      print("[!] Failed to create thread pool. Terminated")
      exit(-1)
    pool.submit(self.__listen__)
    pool.submit(self.__send__)

  def client_start(self):
    self.sock = socket.socket()
    self.sock.connect((self.host, self.port))
    #except:
    #  print("[!] Connecting fail. Terminated")
    #  exit(-1)
    print("[+] Connection established from {}".format(self.host))
    self.__connection__()

def usage():
  print("syntax : python echoclient.py <host> <port>")
  print("sample : python echoclient.py 127.0.0.1 1234")


if __name__=="__main__":
  host = ''
  port = 0
  if len(sys.argv) != 3:
    usage()
    exit(-1)
  try:
    host = sys.argv[1]
    port = int(sys.argv[2])
    print(host,port)
  except:
    usage()
    exit(-1)  
  
  C = Client(host,port)
  C.client_start()