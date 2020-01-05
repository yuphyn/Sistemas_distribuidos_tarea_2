### Sistemas distribuidos tarea 2

## Integrantes:

* Cesar Quiroz  Mansilla 201573578-6
* jorge Contreras Cabreras 201573547-6

### Actividad 1 y 2

Para la actividad 1 uno debe dirigirse dentro de la carpeta actividad 1 y correr el siguiente comando:

>docker-compose build

>docker-compose up --scale clients=N

+ Donde N es el numero de clientes a conectarse.

Para la actividad 2 uno debe dirigirse dentro de la carpeta actividad 2 y correr el siguiente comando:

>docker-compose build

>docker-compose up --scale client=N

+ Donde N es el numero de clientes a conectarse.

Para poder ejecutar comandos por consola debe abrir otra terminal y ejecutar:

> docker attach "Nombre del container"

los nombres del conteiner tienen la siguiente forma actividad1_clients_N con N corespondiente al cliente con ID N. 
También es posible acceder con el id del container, para obtenerlos basta con escribir: docker ps -a
