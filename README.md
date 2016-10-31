# genesis
Framework para facilitar y optimizar el despliegue de infraestructuras inalámbricas de sensorización y localización en tiempo real

## genesis.py
  genesis.py es un sript de linea de comandos que forma parte del framework genesis.
  Su tarea es crear el archivo de configuración (.ini) que necesita el pylayers para simular planos, en base a la traducción de archivos SVG que contienen la estructura de estos.
  
  Los archivos SVG son generados con el programa de graficos DraftSight, que es un software gratuito multiplataforma que nos ayuda en la conversión de archivos DWG a SVG, permitiendo exportar cada una de las capas por separado. Se eligió SVG como formato intermediario por su fácil tratamiento.

## Requerimientos para ejecución del script

  Instalación basada en una instalación limpia de ubuntu 16.04 LTS.

### Instalar paquetes

1. Descargar Anaconda para la versión 2.7 de python

    [Página de descarga](https://www.continuum.io/downloads)
  
2. Instalar Anaconda
  
    Ejemplo para Anaconda 4.2.0
    ```
    bash Anaconda2-4.2.0-Linux-x86_64.sh
    ```
3. Descargar la versión 0.5 de pylayers y descomprimir

    [Descargar](https://github.com/pylayers/pylayers/archive/v0.5.zip)
  
4. Instalar pylayers

    Ejecutar el siguiente comando dentro del directorio descomprimido
    ```
    ./installer_unix
    ```

5. Aplicar los siguientes comandos
  ```
  sudo apt update
  sudo apt install build-essential python-dev protobuf-compiler libprotobuf-dev libtokyocabinet-dev python-psycopg2 libgeos-c1v5 libgdal1-dev libspatialindex-dev
  conda install libgcc
  pip install rtree imposm svgwrite svgpathtools
  ```


### Instalar DraftSight para convertir archivos DWG a SVG

[Página de descarga](http://www.3ds.com/products-services/draftsight-cad-software/free-download/)
  
  Este solo se requiere si se desea convertir planos DWG a SVG. Los nombres de los archivos SVG deben de coincidir con alguno de los materiales disponibles en el archivo slabDB.ini, pueden diferir de minúsculas y mayusculas.
  * ABSORBENT
  * AIR
  * WALL
  * PARTITION
  * WINDOW
  * DOOR
  * CEIL
  * FLOOR
  * WINDOW_GLASS
  * WOOD
  * 3D_WINDOW_GLASS
  * WALLS
  * PILLAR
  * METAL
  * CONCRETE_15CM3D
  * CONCRETE_20CM3D
  * CONCRETE_6CM3D
  * CONCRETE_7CM3D
  * PLASTERBOARD_10CM
  * PLASTERBOARD_14CM
  * PLASTERBOARD_7CM
  * METALIC

## Manual de uso

  El script reliza la tarea de conversión de las imágenes .svg a un archivo .ini que contiene la información de los materiales y las estructuras para formar un plano en 3D.
  
### Conversión

  La opción `-c` indica al script la tarea de convertir los archivos SVG que se encuentren en el directorio dicho. El archivo 'reference.svg' siempre debe de existir dentro del directorio. Este contiene la medida de referencia del plano, que por default la toma de 1 metro.
  ```
  python genesis.py -c <directorio>
  ```
  Si la referencia es diferente de 1 metro, se tiene que especificar con la opción `-r`. Opcionalmente se le puede especificar la altura del edificio con la opción `-e` que por default es de 3 metros
  ```
  python genesis.py -c <directorio> -r 2 -e 4
  ``` 
  Como resultado se obtiene un archivo `output.ini` que se encuentra en el directorio de ejecución del script.
  
### Simulación
  
  La opción `-s`indica al script simular el archivo output.ini generado anteriormente
  ```
  python -i genesis.py -s
  ``` 
  
