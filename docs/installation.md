# Guía de Instalación de Task Tracer

## Requisitos Previos
Antes de instalar Task Tracer, asegúrate de tener lo siguiente:

- **Python**: Task Tracer esté construido en Python, por lo que necesitas tener Python instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

## Pasos de Instalación

1. **Clonar el Repositorio**: Clona el repositorio de Task Tracer desde GitHub:

```bash
git clone https://github.com/DaytonPlus/task-tracer-backend.git
```

2. **Crear un Entorno Virtual**: Crea un entorno virtual para Task Tracer. Puedes usar `venv` o `virtualenv`. Por ejemplo:

```bash
python -m venv myenv
```

3. **Activar el Entorno Virtual**: Activa el entorno virtual:
```bash
# En Windows
myenv\Scripts\activate

# En macOS y Linux
source myenv/bin/activate
```

4. **Instalar Dependencias**: Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

5. **Configurar la Base de Datos**: Configura la base de datos en el archivo `settings.py`. Puedes usar SQLite o cualquier otra base de datos compatible con Django.

6. **Aplicar Migraciones**: Aplica las migraciones para crear las tablas de la base de datos:

```bash
python manage.py migrate
```

7. **Crear un Superusuario**: Crea un superusuario para acceder al panel de administración:
```bash
python manage.py createsuperuser
```

8. **Ejecutar el Servidor**: Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

9. **Acceder al Panel de Administración**: Abre tu navegador y ve a [http://localhost:8000/admin/](http://localhost:8000/admin/). Inicia sesión con las credenciales del superusuario.

¡Listo! Ahora puedes comenzar a utilizar Task Tracer para administrar tus tareas. Si tienes alguna pregunta o necesitas más detalles, no dudes en preguntar.




