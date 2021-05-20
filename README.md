# Prueba Talana

*  Se crearon las REST API necesarias

## Intalacion
    
    virtualenv env --python=python3.8
    source env/bin/activate
    cd test_talana
    pip install 
    ./manage.py migrations
    ./manage.py migrate

## Colocar la configuracion del correo en /settings.py

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = <correo>
    EMAIL_HOST_PASSWORD = '<passord>'

## Comando para celery

     celery -A backend worker -l DEBUG 
