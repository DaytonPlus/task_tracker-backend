Aquí tienes la documentación de las APIs:

## **Middlewares**

#### **Globales**

- **EnsureJSONMiddleware**: Este middleware garantiza que todas las solicitudes enviadas sean del tipo JSON. Si no lo son, se responderá con un error 415 (`Unsupported Media Type`)
- **rest_framework.tokenauth**: Este middleware se utiliza para proteger rutas que no sean abiertas. Pasa si la solicitud tiene un token de autenticación y es válido, si esto no se cumple retorna un 401 (`Unauthorized`).

## **Rutas**

#### **Rutas de Autenticación**

Las rutas de autenticación como su nombre lo dice son para que los usuarios tengan acceso a los diferentes servicios de esta aplicación, ya sea creando una cuenta o usando una existente (`el objetivo es obtener el token de acceso`), además de otros servicios para validar el token o obtener información de un usuario (Estas dos últimas son `Rutas Protegidas`)

- **`/api/auth/login/`**: Punto de acceso para que un usuario inicie sesión.
- [más detalles](#ruta_login)

- **`/api/auth/register/`**: Punto de acceso para que un usuario cree su cuenta.
- [más detalles](#ruta_register)

- **`/api/auth/check/`**: Punto de acceso para verificar si un usuario ha iniciado sesión. 
- [más detalles](#ruta_check)

- **`/api/auth/profile/`**: Punto de acceso para obtener, actualizar o eliminar los datos del usuario actual 
- [más detalles](#ruta_profile)

#### Rutas Principales (Protegidas)

Las rutas protegidas requieren autenticación con un token generado por `rest_framework.authtoken`. Para acceder a estas rutas, es necesario agregar en la cabecera de la consulta (`header`) el token obtenido en el login o el register en el header: `Authorization: Token $token`.

- **`/api/v1/projects/`**: Punto de acceso para crear un proyecto o obtener los datos de todos los proyectos.
- [más detalles](#Ruta_projects)

- **`/api/v1/projects/:id/`**: Punto de acceso para obtener o actualizar los datos de un proyecto especificado por el **id** (`:id`)
- [más detalles](#Ruta_Project)

- **`/api/v1/projects/:id/tasks`**: Punto de acceso para crear una tarea o obtener los datos de todas las tareas (de un proyecto especificado por el **id** (`:id`)
- [más detalles](#Ruta_Tasks)

- **`/api/v1/projects/:id/tasks/:taskid`**: Punto de acceso para obtener o actualizar los datos de una tarea especificada por un **id** (`:taskid`) en un proyecto específicos por el **id** (`:id`)
- [más detalles](#Ruta_Task)

##### Detalles

Las Rutas se restringen por varias condiciones:

> Un método http diferente al disponible en el servidor HTTP_405_METHOD_NOT_ALLOWED: 
`{"detail":"Method \"GET\" not allowed."}`

> Un tipo de contenido diferente de `application/json`, el servidor responde: `{"error": "Invalid Content-Type"}`


#### Rutas


###### Ruta_login

Permisos: [Abierto]

Método [POST]

```json
// Obtener token (Autenticación)
fetch(`${HOST_API}/api/auth/login/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: usuario,
    password: clave,
  })
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
No existe el [username]

# 400 (BAD REQUEST)
Campos requeridos faltantes: [username, password]
Contraseña incorrecta

# 200 (OK)
Responde: {token: "..", data: {id: 1, username: .., ...}}
```

###### Ruta_register

Permisos: [Abierto]

Método [POST]

```javascript
// Crear un nuevo usuario
fetch(`${HOST_API}/api/auth/register/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: usuario, 
    password: clave,
    full_name: nombre_y_apellidos,
    email: correo,
    contact_number: telefono,
    identification_number: ci,
    gender: genero,
    role: rol,
  })
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias repetidos: [username, email, identification_number]
Campos requeridos faltantes: [username, password, full_name, email, contact_number, identification_number, gender, role]
Tipos de datos invalidos: [rol, gender]
rol = backend | frontend | fullstack | DevOps Engineer | qa | uxui | project_manager
gender = m | f

# 200 (OK)
Responde: {token: "..", data: {id: 1, username: .., ...}}
```


###### Ruta_check

Permisos: [Protegido(Usuario)]

Método [POST]

```json
// Verificar la validez del token
fetch(`${HOST_API}/api/auth/check/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 401 (UNAUTHORIZED)
Token Invalido

# 200 (OK)
Responde: Tu token es válido
```


###### Ruta_Profile

Permisos: [Protegido(Usuario)]

Método [GET]

```javascript
// Obtener datos del usuario actual
fetch(`${HOST_API}/api/auth/profile/`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias repetidos: [username, email]

# 200 (OK)
Responde con los datos {id: 1, username: .., ...}
```

Método [PUT]

```javascript
// Actualizar datos de un usuario
fetch(`${HOST_API}/api/auth/profile/`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  },
  body: {
    // optional user fields to update
  }
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias repetidos: [username, email, identification_number]
Tipos de datos invalidos: [rol, gender]
rol = backend | frontend | fullstack | DevOps Engineer | qa | uxui | project_manager
gender = m | f

# 200 (OK)
Responde con los datos {id: 1, username: .., ...}
```

Método [DELETE]

```javascript
// Eliminar el usuario actual 
fetch(`${HOST_API}/api/auth/profile/`, {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 200 (OK)
Responde: Usuario eliminado correctamente!
```


##### Rutas del CRUD

###### Ruta_Projects

Permisos: [Protegido(Usuario)]

Método [GET]

```javascript
// Obtener proyectos
const params = {
  // Parametros de búsqueda (multi) [id, name, description: descripcion, objective, start_date, end_date, created_at, updated_at]
  name: "Task 1",
  status: "new",
  // Parametros de organización (multi) [orderby]
  orderby: "name"
};
const querys = "?" + Object.keys(params).map((key) => `${key}=${encodeURIComponent(params[key])}`).join("&");

fetch(`${HOST_API}/api/v1/projects${querys}/`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 200 (OK)
Responde con los datos [{id: 1,name: .., ...}, ...]
•  Si no hay datos responde []
```

Método [POST]

```javascript
// Crear un nuevo proyecto
fetch(`${HOST_API}/api/v1/projects/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  },
  body: JSON.stringify({
    name: nombre,
    description: descripcion,
    objective: objetivo,
    start_date: fechaDeInicio,
    end_date": fechaDeFin,
  })
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias repetidos: [name]
Campos requeridos faltantes: [name, description, objective, start_date, end_date]
Tipos de datos invalidos: [start_date, end_date]

# 200 (OK)
Responde con los datos {id: 1,name: .., ...}
```

###### Ruta_Project

Permisos: [Protegido(Usuario)]

Método [GET]

```javascript
// Obtener datos de proyecto 
fetch(`${HOST_API}/api/v1/projects/${P_ID}`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`

# 200 (OK)
Responde con los datos {id: 1,name: .., ...}
```

Método [PUT]

```javascript
// Actualizar un proyecto
fetch(`${HOST_API}/api/v1/projects/${P_ID}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  },
  body: JSON.stringify({
    // optional fields to update
  })
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias: [name]
Tipos de datos invalidos: [start_date, end_date]

# 404 (NOT FOUND)
Proyecto con `P_ID`

# 200 (OK)
Responde con los datos {id: 1,name: .., ...}
```

Método [DELETE]

```javascript
// Eliminar un proyecto
fetch(`${HOST_API}/api/v1/projects/${P_ID}`, {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`

# 200 (OK)
Responde:  {"detail": "Deleted project success and (c) vinculed tasks"}
```

Método [POST]

```javascript
// Unirte a un proyecto
fetch(`${HOST_API}/api/v1/projects/${P_ID}/join`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Ya estas vinculado con el proyecto de `P_ID`
Respuesta:  {"detail": "You already joined to this project"}

# 404 (NOT FOUND)
Proyecto con `P_ID`

# 200 (OK)
Responde: {"detail": "You joined now to the project"}
```

Método [POST]

```javascript
// Salir de un proyecto
fetch(`${HOST_API}/api/v1/projects/${P_ID}/leave`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
No estas vinculado con el proyecto de `P_ID`
Respuesta:  {"detail": "You already not joined to this project"}

# 404 (NOT FOUND)
Proyecto con `P_ID`

# 200 (OK)
Responde: {"detail": "You leaved now to the project"}
```


###### Ruta_Tasks

Permisos: [Protegido(Usuario)]

Método [GET]

```javascript
// Obtener tareas de un proyecto
const params = {
  // Parametros de búsqueda (multi) [id, name, description: descripcion, objective, start_date, end_date, created_at, updated_at]
  name: "Task 1",
  status: "new",
  // Parametros de organización (multi) [orderby]
  orderby: "name"
};
const querys = "?" + Object.keys(params).map((key) => `${key}=${encodeURIComponent(params[key])}`).join("&");

fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks${querys}/`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```


Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`

# 200 (OK)
Responde con los datos [{id: 1,name: .., ...}, ...]
•  Si no hay datos responde []
```

Método [POST]

```json
// Crear una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  },
  body: JSON.stringify({
    name: nombre,
    description: descripcion,
    start_date: fechaDeInicio,
    end_date: fechaDeFin
  })
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias: [name]
Campos requeridos faltantes: [name, description, start_date, end_date]
Tipos de datos invalidos: [start_date, end_date]

# 404 (NOT FOUND)
Proyecto con `P_ID`

# 201 (CREATED)
Responde con los datos {id: 1,name: .., ...}
```

###### Ruta_Task

Permisos: [Protegido(Usuario)]

Método [GET]

```json
// Obtener información de una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/${T_ID}/`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias: [name]
Tipos de datos invalidos: [start_date, end_date]

# 404 (NOT FOUND)
Proyecto con `P_ID`
Tarea con `T_ID`

# 200 (OK)
Responde con los datos {id: 1,name: .., ...}
```

Método [PUT]

```json
// Actualizar información de una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/${T_ID}/`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  },
  body: JSON.stringify({
    // optional fields to update
  })
})
```

Respuestas HTTP

```
# 400 (BAD REQUEST)
Únicos o llaves primarias: [name]
Tipos de datos invalidos: [start_date, end_date]
status = accepted | resolved | closed
Otros [status] que son autoasignados [new, assigned]

# 404 (NOT FOUND)
Proyecto con `P_ID`
Tarea con `T_ID`

# 200 (OK)
Responde con los datos actualizados {id: 1,name: .., ...}
```

Método [POST]

```json
// Asignarte una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/${T_ID}/assign`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`
Tarea con `T_ID`

# 400 (BAD REQUEST)
Ya has sido asignado 

# 200 (OK)
Has sido asignado a la tarea
```

Método [POST]

```json
// Desasignarte de una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/${T_ID}/unassign`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`
Tarea con `T_ID`

# 400 (BAD REQUEST)
No estas asignado a la tarea

# 200 (OK)
Has sido desasignado a la tarea
```

Método [POST]

```json
// Cerrar una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/${T_ID}/close`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`
Tarea con `T_ID`

# 400 (BAD REQUEST)
La tarea (x) ya ha sido terminada

# 200 (OK)
La tarea (x) ha sido cerrada
```

Método [POST]

```json
// Desasignarte de una tarea
fetch(`${HOST_API}/api/v1/projects/${P_ID}/tasks/${T_ID}/resolve`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${TOKEN}`
  }
})
```

Respuestas HTTP

```
# 404 (NOT FOUND)
Proyecto con `P_ID`
Tarea con `T_ID`

# 400 (BAD REQUEST)
La tarea (x) ya ha sido cerrada

# 200 (OK)
La tarea (x) ha sido terminada
```

