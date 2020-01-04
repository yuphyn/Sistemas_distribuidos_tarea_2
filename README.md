### Sistemas distribuidos tarea 2

## Integrantes:

* Cesar Quiroz  Mansilla 201573578-6
* jorge Contreras Cabreras

### Actividad 1

Para la actividad uno debe dirigirse dentro de la carpeta actividad 1 y correr el siguiente comando:

>docker-compose build

>docker-compose up --scale clients=N

+ Donde N es el numero de clientes a conectarse.

Para poder ejecutar comandos por consola debe abrir otra terminal y ejecutar:

> docker attach \<Nombre del container\>

los nombres del conteiner tienen la siguiente forma actividad1_clients_N con N corespondiente al cliente con ID N-1. 
