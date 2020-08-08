# Configuración del core de python/environment.
VIRTUAL_ENV = .env
RUNTIME_VERSION = 3.8
REQUIREMENTS = requirements.txt


# Configuración de Colores. Para darle alegría a la vida
HEADER = '\033[96m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

##end_settings_configuration
full-install: clean prepare-dev create-virtual install-requirements-python


clean:
	@+echo $(HEADER)"Desinstalando paquetes y entorno virtual"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@rm -rf ./$(VIRTUAL_ENV)
	@+echo $(OKGREEN)"[OK] Entorno virtual desinstalado"$(END)
	@+echo ""

clean-cache:
	@+echo $(HEADER)"Limpiando Cache de Python"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@find . -name "*.pyc" -exec rm -f {} \;
	@+echo $(OKGREEN)"[OK] Cache limpiada"$(END)
	@+echo ""

prepare-dev:
	@+echo  $(HEADER)"Instalando paqueteria de sistema"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	sudo apt-get -y install python$(RUNTIME_VERSION) python3-pip python3-dev python3-pygments;
	python3 -m pip install virtualenv;
	@+echo $(OKGREEN)"[OK] Sistema Listo "$(END)

create-virtual:
	@+echo  $(HEADER)"Instalando y activando entorno virtual"
	@+echo "---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv -p python$(RUNTIME_VERSION) $(VIRTUAL_ENV); \
	fi
	@+echo ""$(END)

install-requirements-python:
	@+echo $(HEADER)"Instalando paquetes requeridos por el entorno"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@ $(VIRTUAL_ENV)/bin/pip --no-cache-dir install -Ur $(REQUIREMENTS)
	@ touch $(VIRTUAL_ENV)/bin/activate
	@+echo $(OKGREEN)"[OK] Paquetes instalados"$(END)
	@+echo ""

virtual:
	@+echo  $(HEADER)"Instalando y activando entorno virtual"
	@+echo "---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv -p python$(RUNTIME_VERSION) $(VIRTUAL_ENV); \
	fi
	@+echo ""$(END)
