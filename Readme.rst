Primeros pasos.
#################################

Se debe asegurar la existencia del environment de desarrollo para **python 3.8** [1]_. por lo que, en la carpeta raíz del proyecto (Lambdas) se debe ejecutar:

::

    make full-install

Sobre full-install?
=============================

**full-install** ejecutara 4 sub procesos del **Makefile**

::

    full-install: clean prepare-dev create-virtual install-requirements-python

- **clean**: limpia *(elimina)* el environment de python en caso de existir.
- **clean**: Ejecuta (va a requerir super usuario) la instalación de los paquetes necesarios para ejecutar/desarrollar con la version de python configurada (3.8)
- **create-virtual**: En caso de no existir el environment del ambiente (lambdas), lo crea.
- **install-requirements-python**: Instala en environment (de lambdas) el listado de paquetes del requirements.txt

Estructura de los proyectos.
#################################

a modo general
=============================

EL repositorio contiene todo el ambiente de micro servicios, cada proyecto(carpeta) posee un requirements propio que indica la paquetería a utilizar.


ejecuciones locales
=============================
Para realizar ejecuciones locales, se recomienda incluir en el requirements de Lambdas los requirements del proyecto, entrar al proyecto y ejecutar el archivo principal "app.py"

hacer deploy?
=============================
para hacer deploy de una función, se debe poseer credenciales de aws validas en la carpeta personal.
es decir,

archivo ~/.aws/config

::

    [default]
    aws_access_key_id=YOUR_ACCESS_KEY_HERE
    aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
    region=YOUR_REGION (such as us-west-2, us-west-1, etc)

Asegurado la existencia de las credenciales, *"simplemente"* se ingresa a la carpeta de la funcionalidad a subir, y se ejecuta:
    chalice deploy


Esto subida el código correspondiente a aws y generara un endpoint en api gateway para su consumo, generando un output como el siguiente [2]_:

::

    Creating deployment package.
    Updating policy for IAM role: metro-dev
    Updating lambda function: metro-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-2:3141592653:function:metro-dev
      - Rest API URL: https://dognx5fm7b.execute-api.us-west-2.amazonaws.com/api/



.. [#] No se asegura la completa compatibilidad para otras versiones de Python.
.. [#] En su configuración por defecto (proyecto)/.chalice/config.json considerara que el lambda/servicio se crea en modo "desarrollo".
