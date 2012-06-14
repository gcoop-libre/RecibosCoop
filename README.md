Instalación
-----------

Para instalar el sistema, es aconsejable crear un entorno
e instalar todas las dependencias:

    mkvirtualenv recibos
    workon recibos
    pip install -r requirements.txt

Estamos usando submodules de git. Es necarios clonar las
dependencias:

    git submodule init
    git submodule update

Una vez instaladas las dependencias, para abrir la aplicación
tendrías que ejecutar:

    python app.py
