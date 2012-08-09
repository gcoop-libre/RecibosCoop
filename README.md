# RecibosCoop

RecibosCoop es una aplicación web muy sencilla, permite simplificar
la elaboración e impresión de recibos en una cooperativa de trabajo:

![](https://raw.github.com/gcoop-libre/RecibosCoop/master/images/screen.png)

Cada recibo cargado en la aplicación se puede exportar cómo un archivo pdf:

![](https://raw.github.com/gcoop-libre/RecibosCoop/master/images/lista.png)

El recibo se genera con dos copias en la misma hoja A4, para que se pueda
imprimir y firmar:

![](https://raw.github.com/gcoop-libre/RecibosCoop/master/images/recibo.png)

Este software se desarrolló dentro de la cooperativa Gcoop, pero se puede adaptar
fácilmente para que sea de utilidad a otras cooperativas.

## Instalación

Para instalar el sistema, es aconsejable crear un entorno
e instalar todas las dependencias:

    mkvirtualenv recibos
    workon recibos
    pip install -r requirements.txt

Estamos usando submodules de git. Es necarios clonar las
dependencias:

    git submodule init
    git submodule update

También se necesita un programa para generar archivos PDF desde la
aplicación:

    apt-get install wkhtmltopdf

Tener en cuenta que `wkhtmltopdf` por defecto requiere X11, aunque permite
ejecutarse desde consola con la [siguiente solución en stackoverflow][http://stackoverflow.com/questions/9604625/wkhtmltopdf-cannot-connect-to-x-server].

Luego tienes que iniciar la base de datos (solamente la primera
vez):

    python deploy.py

Incluimos unos archivos llamados 'socios.csv' y 'cooperativa.csv' de ejemplo
para agilizar la carga de datos inicial.


## Ejecutar en modo desarrollo

Una vez instaladas las dependencias, para abrir la aplicación
tendrías que ejecutar:

    python app.py

## Ejecutar en modo producción

Usamos [gunicorn][gunicorn], así que simplemente tienes que
ejecutar el siguiente comando:

    gunicorn app:app -w 4 -D

Luego, para administrar los recursos de la aplicación puedes
ejecutar:

    gunicorn-console

[gunicorn]: http://gunicorn.org/
