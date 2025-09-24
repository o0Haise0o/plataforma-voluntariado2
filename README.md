# Instalación

## Requisitos

Antes de instalar el proyecto, asegúrate de tener lo siguiente instalado:

1. **Python 3.x** (se recomienda Python 3.10 o superior)
2. **Pip** (administrador de dependencias de Python)
3. **Django 5.x o superior**
4. **Git** (para clonar el repositorio desde GitHub)
5. **Opcional:** Entorno virtual `venv` (para aislar las dependencias del proyecto).

---

## Instalación de los requisitos

### Linux (Ubuntu/Debian)

Instalar Python y pip:

```bash
sudo apt install python3 python3-pip -y
```

Verificar instalación:

```bash
python3 --version
pip3 --version
```

Instalar Git:

```bash
sudo apt install git -y
```

Verificar Git:

```bash
git --version
```

Instalar Django:

```bash
pip3 install "Django>=5.0"
```

---

### Windows

1. **Python y pip**

   * Descarga e instala desde [python.org/downloads](https://www.python.org/downloads/)
   * Durante la instalación, marca la opción **“Add Python to PATH”**.

   Verificar instalación (en PowerShell o CMD):

   ```powershell
   python --version
   pip --version
   ```

2. **Git**

   * Descarga e instala desde [git-scm.com/downloads](https://git-scm.com/downloads)
   * Verificar instalación:

   ```powershell
   git --version
   ```

3. **Django**

   ```powershell
   pip install "Django>=5.0"
   ```

---

## Pasos para instalar el proyecto

### 1. Clona el repositorio

Linux / macOS:

```bash
git clone https://github.com/o0Haise0o/plataforma-voluntariado2.git
cd plataforma-voluntariado2
```

Windows (PowerShell o CMD):

```powershell
git clone https://github.com/o0Haise0o/plataforma-voluntariado2.git
cd plataforma-voluntariado2
```

---

### 2. Crea un entorno virtual (opcional pero recomendado)

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\activate
```

---


### 3. Realiza las migraciones

```bash
python manage.py migrate
```

---

### 4. Crea un superusuario

```bash
python manage.py createsuperuser
```

---

### 5. Inicia el servidor de desarrollo

```bash
python manage.py runserver
```

Accede a la aplicación en tu navegador:
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

##  Dependencias principales

* **Django** → Framework web para el desarrollo rápido.
* **SQLite** → Base de datos ligera por defecto.
---

## Estructura del Proyecto

```
plataforma-voluntariado/
├── acciones/              # Aplicación principal de gestión
│   ├── migrations/        # Migraciones de la base de datos
│   ├── admin.py           # Configuración del admin de Django
│   ├── apps.py            # Configuración de la aplicación
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas de la aplicación
│   └── urls.py            # URLs de la app
├── plataforma/            # Configuración global del proyecto
│   ├── __init__.py
│   ├── settings.py        # Configuración general
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── db.sqlite3             # Base de datos (autogenerada)
├── manage.py              # Comandos de Django
├── requirements.txt       # Dependencias del proyecto
├── schema.ddl             # Estructura de la base de datos
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Documentación
```

---
