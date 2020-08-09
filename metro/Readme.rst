Metro
====================

Obtiene la ruta mas "corta"(en caso de existir) a una red de metro dada (mediante el archivo stgo.json), aplicando el algoritmo de Dijkstra.


Métodos disponibles
====================

Relacionados con la funcionalidad del "Algoritmo"

- generate_list, dado los argumentos 'city' (actualmente, disponible 'stgo' y 'buda_city', retorna un listado de diccionarios con el detalle de las estaciones de metros en la "red".
- metro_route_finder: dado los argumentos 'from', 'destiny' y 'color' (optativo), 'city'(optativo, stgo por defecto), indica la ruta más "corta" entre estación y estación (considerando que el costo de moverse entre estaciones es de "1")


Endpoint.
====================

- (GET)https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/: retorna la ruta -*en caso de existir*- entre dos estaciones de metro. argumentos:

 - from=conchali
 - destiny=santa rosa
 - color=red (color es optativo)
 - city=stgo (city es optativo, puede ser stgo o buda_city)

EJ *(emplos)*:
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=conchali&destiny=tobalaba&color=verde
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=tobalaba&destiny=conchali
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=a&destiny=f&city=buda_city
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=a&destiny=f&city=buda_city&color=red
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=a&destiny=i&city=buda_city&color=green
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=a&destiny=i&city=buda_city&color=red


- (GET)https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/list/: retorna el listado de todas las estaciones de metro disponibles, se debe enviar por parámetro el nombre de la ciudad a obtener, retorna los datos de la estación, como el nombre (name), la estación previa (prev) y siguiente (next) en caso de existir, la linea (line) y el color (color-opcional) en caso de que la estación sea *"exclusiva"*

EJ:
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/list/?city=stgo
 - https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/list/?city=buda_city

Sobre las estaciones de metro.
===============================

las estaciones de "metro" estan presentes en **chalicelib** con en nombre de la 'ciudad', el archivo json es un listado con los datos:

:: code-block::javascript

    [
      {
        "name": "alcántara",  // como nombre identificador, el mismo debe ser ocupado en prev y next
        "prev": "el golf",  // indica a la estacion a la cual se puede "retroceder"
        "next": "escuela militar"  // indica a la estacion a la cual se puede "avanzar"
        "line": "l1",  // actualmente sin uso,
        "color": "red"  // opcional, en caso de existir, indica la exclusividad para el tren de "color"

      },
      {}

    ]



Enlaces y referencias externas.
#################################


 - `Estaciones de metro <https://es.wikipedia.org/wiki/Anexo:Estaciones_del_Metro_de_Santiago>`_. Utilizado en el json de estaciones (no incluye el color de estación).
 - `Dijkstar. <https://pypi.org/project/Dijkstar/>`_ Paquete de para el *Algoritmo*:
 - `Chalice <https://github.com/aws/chalice>`_. Paquete para la arquitectura de **AWS λ**.


