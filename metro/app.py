from collections import defaultdict
from contextlib import contextmanager
from functools import lru_cache
import json

from chalice import Chalice
from dijkstar import find_path
from dijkstar import Graph
import unidecode

app = Chalice(app_name='metro')


@contextmanager
def ignore(*exceptions):
    """
    Contexto que permite ignorar las excepciones que puedan ocurrir.

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.7.
    """
    exceptions = exceptions or (Exception,)
    try:
        yield
    except exceptions as e:
        print(e)


def sanitizer(string):
    """
    toma una cadena de texto y ejecuta un proceso de limpieza que consiste en:
        - Eliminar acentos.
        - Texto en minúscula.
        - sin espacios a la izquierda y a la derecha.


    Parameters
    ----------
     - (string) a limpiar

    Returns
    -------
     - (string) ''

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.7.
    """
    string = string or ''
    return unidecode.unidecode(string).lower().strip()


@lru_cache()
def retrieve_file():
    """
    carga (y guarda en memoria mediante lru_cache) el listado de las estaciones.

    Parameters
    ----------
     - None

    Returns
    -------
     - list(dict) / listado de diccionarios.

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.7.
    """
    return json.load(open('chalicelib/stgo.json'))


@app.route('/')
def metro_route_finder(**kwargs):
    """

    Parameters
    ----------
     - dict: {
         'from': 'conchali',
         'destiny': 'tobalaba',
         'color': 'azul'
     }

    Returns
    -------
     - dict: {
        'from': 'conchali',  # convertido a como lo interpreta el programa
        'destiny': 'conservia', # convertido a como lo interpreta el programa
        'route': [], # siempre, independiente si la ruta es posible o no.
        'reason': 'impossible route',  # en caso de que ruta sea vacía, indica el motivo.
        'present_in_graph': { # si uno de los destinos no esta en el ruta, estos son informados.
            'conchali': True,
            'conservia': False
        }
    }

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.7.
    """
    params = {}

    with ignore():
        params.update(**kwargs)
        params = dict(app.current_request.query_params)
        params = {key: sanitizer(value) for key, value in params.items()}

    color = params.get('color', '')
    start = params.get('from', '')
    destiny = params.get('destiny', '')
    graph = Graph()

    stations = []
    for station in retrieve_file():
        station = {key: sanitizer(value) for key, value in station.items()}

        # obtención de valores
        name = station.get('name')
        prev = station.get('prev')
        next_s = station.get('next')
        color_station = station.get('color', color)

        # análisis de extremos y color
        if not prev:
            prev = f'terminal-{name}'
        if not next_s:
            next_s = f'terminal-{name}'

        same_color = True if len(color) == 0 else color == color_station

        if not same_color:
            continue

        # se añade al grafo los nodos de las estaciones de metros, no aplica el
        # costo de movimiento, por lo que se deja en 1
        graph.add_edge(name, prev, 1)
        graph.add_edge(name, next_s, 1)

    #  nodes se declara afuera del ignore, en caso de no existir una ruta, se ignora la excepción.
    extra_response = defaultdict(dict)
    nodes = []

    if not all(map(lambda x: x in graph, (start, destiny))):
        if start:
            extra_response['present_in_graph'][start] = start in graph
        if destiny:
            extra_response['present_in_graph'][destiny] = destiny in graph

    with ignore():
        nodes = find_path(graph, start, destiny).nodes
    if not nodes:
        extra_response['reason'] = 'impossible route'

    return {
        **{
            'from': start,
            'destiny': destiny,
            'route': nodes
        },
        **extra_response
    }


@app.route('/list')
def generate_list():
    """
    retorna el listado de estaciones disponibles.

    Parameters
    ----------
     -

    Returns
    -------
     - dict:
     {
        'stations': [
            {
                'name': 'alcantara',
                'prev': 'el golf',
                'line': 'l1',
                'next': 'escuela militar',
                'color': 'verde' # optativo
            },
            ...
        ]
     }

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.8.
    """
    stations = [
        {key: sanitizer(value) for key, value in station.items()}
        for station in retrieve_file()

    ]
    return {
        'stations': stations
    }


"""
__name__ es 'app' cuando la invocación es desde aws (ya que importa este archivo se importa), 
por lo que, __main__ (o principal) queda para las ejecuciones en local/testing
"""

if __name__ == '__main__':
    sets = [
        {'from': 'conchali', 'destiny': 'tobalaba', 'color': 'azul'},
        {'from': 'conchali', 'destiny': 'tobalaba'},
        {'destiny': 'hospital el pino', 'from': 'vespucio norte'},
        {'destiny': 'toesca', 'from': 'franklin'},
        {'destiny': 'conservia', 'from': 'salsacia'},
        {'destiny': 'conchali', 'from': 'salsacia'},
    ]
    for values in sets:
        print(metro_route_finder(**values))
    print(generate_list())
