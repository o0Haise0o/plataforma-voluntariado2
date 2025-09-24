# Plataforma de Voluntariado y Acción Social

Plataforma web desarrollada con Django para gestionar **causas**, **campañas**, **actividades** y **participación** de voluntarios en organizaciones sociales. La aplicación permite a las organizaciones gestionar sus campañas, inscribir voluntarios en actividades y hacer seguimiento a las participaciones.

## Descripción

Este proyecto es una plataforma para ayudar a organizaciones no lucrativas a organizar y gestionar sus actividades y campañas sociales. Los voluntarios pueden inscribirse a actividades, participar en campañas y llevar un registro de su participación.

### Funcionalidades:
- **Registro de causas**: Permite definir las áreas de trabajo como educación, medio ambiente, salud, etc.
- **Gestión de campañas**: Las organizaciones pueden crear campañas, asignarles causas, fechas y lugares.
- **Inscripción a actividades**: Los voluntarios pueden inscribirse a actividades asociadas a campañas y seguir su progreso.
- **Seguimiento de participación**: Los voluntarios pueden registrar el tiempo de participación y marcar si asistieron.

## Instalación

### Requisitos
- **Python 3.x**
- **Pip** (para instalar dependencias)
- **Django 5.x** o superior

### Pasos para instalar el proyecto:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/o0Haise0o/plataforma-voluntariado.git
   cd plataforma-voluntariado
Crea un entorno virtual (opcional pero recomendado):

bash
python3 -m venv venv
source venv/bin/activate  

Instala las dependencias:

bash
pip install -r requirements.txt
Realiza las migraciones para crear las tablas en la base de datos:

bash
python manage.py migrate
Crea un superusuario para acceder al panel de administración:

bash
python manage.py createsuperuser
Inicia el servidor de desarrollo:

bash
python manage.py runserver
Accede a la aplicación en tu navegador en http://127.0.0.1:8000.

Dependencias
Este proyecto utiliza las siguientes dependencias:

Django: Framework web para el desarrollo rápido.

SQLite: Base de datos ligera por defecto (configurable en el futuro si se desea).

djangorestframework (si decides agregar APIs REST en el futuro).


###Uso
Una vez que el servidor esté corriendo, puedes:

Acceder al panel de administración: http://127.0.0.1:8000/admin/

Crear y gestionar causas, campañas y actividades.

Ver el registro de participaciones de los voluntarios.

Interacciones para Voluntarios
Los voluntarios pueden registrarse en el sitio y gestionar su perfil.

Pueden inscribirse a actividades y seguir su progreso.

Estructura del Proyecto
text
Copiar código
plataforma-voluntariado/
├── acciones/                    # Aplicación principal de gestión de voluntarios y campañas
│   ├── migrations/              # Migraciones de la base de datos
│   ├── admin.py                 # Configuración del admin de Django
│   ├── apps.py                  # Configuración de la aplicación
│   ├── models.py                # Modelos de datos (User, Campaign, Activity, etc.)
│   ├── views.py                 # Vistas de la aplicación
│   └── urls.py                  # URLs relacionadas con la app
├── plataforma/                  # Configuración global del proyecto
│   ├── __init__.py              # Marca la carpeta como módulo de Python
│   ├── settings.py              # Configuración del proyecto (Base de datos, middleware, etc.)
│   ├── urls.py                  # URL principal
│   └── wsgi.py                  # Configuración para desplegar con WSGI
├── db.sqlite3                   # Base de datos SQLite (se genera automáticamente)
├── manage.py                    # Archivo de gestión de Django (comandos de administración)
├── requirements.txt             # Dependencias del proyecto (pip)
├── .gitignore                   # Archivos que deben ser ignorados por git
├── schema.ddl                   # Archivo DDL que define la estructura de la base de datos
└── README.md                    # Este archivo