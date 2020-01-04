import time

print("Arquitectura levantada")
print("Para ejecutar una terminal de cliente ejecutar:")
print("docker exec -it IDCONTAINER python ./client.py")
print("Para obtener la id del container usar docker container ls")

while True:
    time.sleep(100)