# 🚀 Task Tracer

**Task Tracer** es una aplicación robusta construida con **Django Rest Framework**. Esta aplicación permite realizar operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) para el seguimiento de tareas. Utiliza **PostgreSQL** como base de datos y **CORS local** para manejar las solicitudes de origen cruzado.

## 📋 Requisitos

Para ejecutar esta aplicación, necesitarás:

- **Python** (última versión)
- **PostgreSQL**

## 🛠️ Instalación

Sigue estos pasos para instalar y ejecutar la aplicación:

### Paso 1: Instalar las dependencias

Primero, necesitas instalar las dependencias. Puedes hacerlo ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```

> ⚠️ **Importante**: Asegúrate de tener instalada la última versión de Python.

### Paso 2: Crear la base de datos

Ahora, vamos a crear la base de datos con los siguientes comandos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 3: Ejecutar el servidor

Finalmente, puedes ejecutar el servidor con el siguiente comando:

```bash
python manage.py runserver
```

¡Listo! La aplicación está corriendo en [http://localhost:8000/](http://localhost:8000/)

## 📚 Documentación

Para más detalles sobre cómo usar la aplicación, consulta la [documentación oficial](docs/index.md).

## 📧 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarnos a través de [nuestro correo electrónico](daytonprogrammer@gmail.com).

## 📃 Licencia

Task Tracer está bajo la licencia [MIT](#). Consulta el archivo `LICENSE` para más detalles.

