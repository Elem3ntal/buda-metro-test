Metro
====================

Obtiene la ruta mas "corta"(en caso de existir) a una red de metro dada (mediante el archivo stgo.json), aplicando el algoritmo de Dijkstra.


Métodos disponibles
====================

 - generate_list
 - metro_route_finder


Endpoint.
====================

 - (GET)https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/: retorna la ruta -*en caso de existir*- entre dos estaciones de metro. argumentos:

  - from=conchali
  - destiny=santa rosa
  - color=red (color es optativo)

EJ:
https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=conchali&destiny=tobalaba&color=verde
https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/?from=tobalaba&destiny=conchali


 - (GET)https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/list/: retorna el listado de todas las estaciones de metro disponibles, indicando el nombre (name), la estación previa (prev) y siguiente (next) en caso de existir, la linea (line) y el color (color-opcional) en caso de que la estación sea *"exclusiva"*



Enlaces y referencias externas.
#################################


 - `Estaciones de metro <https://es.wikipedia.org/wiki/Anexo:Estaciones_del_Metro_de_Santiago>`_. Utilizado en el json de estaciones (no incluye el color de estación).
 - `Dijkstar. <https://pypi.org/project/Dijkstar/>`_ Paquete de para el *Algoritmo*:
 - `Chalice <https://github.com/aws/chalice>`_. Paquete para la arquitectura de **AWS λ**.


