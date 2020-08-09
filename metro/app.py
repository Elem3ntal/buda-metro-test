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
def ignore(*exceptions, quiet=False):
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
        None if quiet else print(e)


def retrieve_next(current=None, replaces=None, flow=None, default=None):
    """
    retorna la estación de metro en caso de que la siguiente/anterior este en el listado de
    estaciones a omitir.

    Parameters
    ----------
     - (string) current: estación actual
     - (dict) dict: estaciones a omitir
     - (string) flow: "flujo" siguiente/previa
     - (any) default: retorno en caso de no existir.

    Returns
    -------
     - (string/any) estación de metro en el flujo(flow) correspondiente

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.9.
    """
    panic_loop = 0
    while current in replaces:
        current = replaces[current][flow]
        panic_loop -= - 1
        if panic_loop > len(replaces):
            return default
    return current


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
def retrieve_file(city=''):
    """
    carga (y guarda en memoria mediante lru_cache) el listado de las estaciones.

    Parameters
    ----------
     - (string) city como archivo a cargar

    Returns
    -------
     - list(dict) / listado de diccionarios.

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.7.
    """
    if not city.endswith('.json'):
        city = f'{city}.json'
    return json.load(open(f'chalicelib/{city}'))


@app.route('/')
def metro_route_finder(**kwargs):
    """

    Parameters
    ----------
     - dict: {
         'from': 'conchali',
         'destiny': 'tobalaba',
         'color': 'azul',
         'city': 'buda-city'
     }

    Returns
    -------
     - dict: {
        'params': { # params como copia de los parámetros ingresados.
            'from': 'a',  # punto de partida
            'destiny': 'f', # punto de llegara
            'color': 'red', # valor opcional, indicando el tipo de tren a tomar
            'city': 'buda_city' # valor opcional, por defecto es stgo.
        },
        'nodes': ['a', 'b', 'c', 'h', 'f']
        },
        # solo estará presente cuando una de las ciudades solicitadas no este en la red
        'present_in_graph': {
            'a': False,
            'f': True
        },
        # solo aparecerá en caso de que la ruta no se pueda generar, o no exista la ciudad
        'reason': 'impossible route'
    }

    :Author:
        - Javier 'rod' Rodríguez.

    :Created:
        - 2020.08.7.
    """
    params = {}

    with ignore(quiet=True):
        params.update(**kwargs)
        params = dict(app.current_request.query_params)
        params = {key: sanitizer(value) for key, value in params.items()}

    color = params.get('color', '')
    start = params.get('from', '')
    destiny = params.get('destiny', '')
    city = params.get('city', 'stgo')
    graph = Graph()

    stations = []
    with ignore():
        stations = [
            {key: sanitizer(value) for key, value in station.items()}
            for station in retrieve_file(city=city)
        ]
    if not stations:
        return {
            'params': params,
            'nodes': [],
            'reason': f'the city {city} do not exist or has no stations.'
        }

    find_replaces = defaultdict(dict)
    available_stations = []

    # se buscan las estaciones que no pueden estar en la red por la restricción de color
    for station in stations:
        name = station.get('name')
        prev = station.get('prev')
        next_s = station.get('next')
        color_station = station.get('color', color)
        same_color = True if len(color) == 0 else color == color_station

        if not same_color:
            find_replaces[name]['prev'] = prev
            find_replaces[name]['next'] = next_s
            continue
        available_stations.append(station)

    # se buscan los reemplazos de las espacios dejados por las estaciones excluidas por el color
    for station in available_stations:

        name = station.get('name')
        prev = retrieve_next(
            current=station.get('prev'),
            replaces=find_replaces,
            flow='prev'
        )
        next_s = retrieve_next(
            current=station.get('next'),
            replaces=find_replaces,
            flow='next'
        )

        # análisis de extremos y color
        if not prev:
            prev = f'terminal-{name}'
        if not next_s:
            next_s = f'terminal-{name}'

        # se añade al grafo los nodos de las estaciones de metros, no aplica el
        # costo de movimiento, por lo que se deja en 1
        graph.add_edge(name, prev, 1)
        graph.add_edge(name, next_s, 1)

    #  nodes se declara afuera del ignore, en caso de no existir una ruta, se ignora la excepción.
    extra_response = defaultdict(dict)
    nodes = []

    if start not in graph:
        extra_response['present_in_graph'][start] = start in graph
    if destiny not in graph:
        extra_response['present_in_graph'][destiny] = destiny in graph

    with ignore():
        nodes = find_path(graph, start, destiny).nodes
    if not nodes:
        extra_response['reason'] = 'impossible route'

    return {
        **{
            'params': params,
            'nodes': nodes
        },
        **extra_response
    }


@app.route('/list')
def generate_list(**kwargs):
    """
    retorna el listado de estaciones disponibles.

    Parameters
    ----------
     - (str) city = nombre de ciudad/mapa a retornar.

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
    city = kwargs.get('city')

    with ignore(quiet=True):
        city = app.current_request.query_params['city']

    stations = []
    with ignore(quiet=True):
        stations = [
            {key: sanitizer(value) for key, value in station.items()}
            for station in retrieve_file(city=city)

        ]
        return {
            'stations': stations
        }
    return {
        'error': f'the city {city} do not exist or has no stations.'
    }


"""
__name__ es 'app' cuando la invocación es desde aws (ya que importa este archivo se importa), 
por lo que, __main__ (o principal) queda para las ejecuciones en local/testing
"""

if __name__ == '__main__':
    sets_routes = (
        [
            {'from': 'conchali', 'destiny': 'tobalaba', 'color': 'azul'},
            {'from': 'conchali', 'destiny': 'tobalaba'},
            {'destiny': 'hospital el pino', 'from': 'vespucio norte'},
            {'destiny': 'toesca', 'from': 'franklin'},
            {'destiny': 'conservia', 'from': 'salsacia'},
            {'destiny': 'conchali', 'from': 'salsacia'},
        ],
        [
            {'from': 'a', 'destiny': 'f', 'city': 'buda_city'},
            {'from': 'a', 'destiny': 'f', 'color': 'red', 'city': 'buda_city'},
            {'from': 'a', 'destiny': 'i', 'color': 'green', 'city': 'chile'},
        ]
    )
    sets_cities = [
        'stgo',
        'buda_city',
        'tangananica'
    ]
    for sets in sets_routes:
        for values in sets:
            print(metro_route_finder(**values))
    for city in sets_cities:
        print(generate_list(city=city))
