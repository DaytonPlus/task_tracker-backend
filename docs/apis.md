Aquí tienes la documentación de la API:

## **Middlewares**

### **Global**

- **EnsureJSONMiddleware**: Este middleware garantiza que todas las solicitudes enviadas sean del tipo JSON. Si no lo son, se responderá con un error 415 (`Unsupported Media Type`).

### **Django Auth Token**

Este middleware se utiliza para proteger rutas. Pasa si la solicitud tiene un token de autenticación y es válido, si esto no se cumple retorna un 401 (`Unauthorized`).

## **Rutas**

### **Rutas de Autenticación**

- **`/api/auth/login/`**: Punto de acceso para el inicio de sesión del usuario. Deberías enviar un objeto JSON con `username` y `password` en una consulta POST.

- **`/api/auth/register/`**: Punto de acceso para el registro de usuarios. Deberías enviar un objeto JSON con detalles del usuario como `username`, `password`, en una consulta POST.

- **`/api/auth/check/`**: Punto de acceso para verificar si un usuario ha iniciado sesión. Este valida el token usando el middleware de autenticación. Para comprobarlo, debes enviar en una consulta POST con el token obtenido en el `login` o el `register` en el header: `Authorization: Token $token`

### **Rutas Principales (Protegidas)**

Las rutas protegidas requieren autenticación con un token generado por `rest_framework.authtoken`. Para acceder a estas rutas, es necesario agregar en la cabecera de la consulta (`header`) el token obtenido en el login o el register en el header: `Authorization: Token $token`.

- **`/api/v1/projects/`**: Punto de acceso para el CRUD con los proyectos. Puedes enviar un objeto JSON con detalles del proyecto para crear uno nuevo, o un ID de proyecto para actualizar o eliminar un proyecto existente.

- **`/api/v1/projects/:id/tasks`**: Punto de acceso para el CRUD de las tareas relacionadas con un proyecto específico. Reemplaza `:id` con el ID del proyecto. Puedes enviar un objeto JSON con detalles de la tarea para crear una nueva tarea, o un ID de tarea para actualizar o eliminar una tarea existente dentro de un proyecto.

- **`/api/v1/projects/:id/tasks/:taskid`**: Punto de acceso para una tarea específica dentro de un proyecto específico. Reemplaza `:id` con el ID del proyecto y `:taskid` con el ID de la tarea. Puedes enviar un objeto JSON con detalles actualizados de la tarea para actualizarla, o simplemente el ID de la tarea para eliminarla.

