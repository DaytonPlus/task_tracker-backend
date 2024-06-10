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

- **`/api/auth/profile/`**: Punto de acceso para obtener información de un usuario especifico (`busqueda por nombre`).
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

```json
// Obtener token (Autenticación)
{
 Url: "{HOST_API}/api/auth/login/",
 Method: "POST",
 Headers: {
  "Content-Type": `application/json`
 },
 Body: {
  "username": "{Usuario}", 
  "password": "{Contraseña}"
 }
}
```

HTTP Responses

***

> Si el usuario no existe:
> × HTTP_404_NOT_FOUND
> `{"detail":"No User matches the given query."}`

***

> Si la contraseña es incorrecta 
> × HTTP_400_BAD_REQUEST
> `{detail: "Invalid Password"}`

***

Si ambos son correctos:
> ✓ HTTP_200_OK
> `{token: "..."}`

***

###### Ruta_register

Permisos: [Abierto]

```json
// Crear un nuevo usuario
{
 Url: "{HOST_API}/api/auth/register/",
 Method: "POST",
 Headers: {
  "Content-Type": "application/json"
 },
 Body: {
  "username": "{Usuario}", 
  "password": "{Contraseña}",
  "confirm": "{Contraseña}"
 }
}
```

HTTP Responses

***

> Si el `username` existe:
> × HTTP_400_BAD_REQUEST
> `{"detail":"El nombre de usuario ya existe o es invalido!"}`
***
El `username` no esta registrado:
> ✓ HTTP_200_OK
> `{token: "..."}
***
###### Ruta_check
Permisos: [Protegido(Usuario)]
```json
// Verificar el token
{
 Url: "{HOST_API}/api/auth/check/",
 Method: "POST",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 },
 Body: {
  "username": "{Usuario}", 
  "password": "{Contraseña}"
 }
}
```

HTTP Responses

***

> El token invalido o sin token
> HTTP_401_Unauthorized
> `{"detail":"Invalid token."}`

***

> El token valido
> ✓ HTTP_200_OK
> `{"detail":"Your token is valid"}`

***

###### Ruta_Profile

Permisos: [Protegido(Usuario)]

```json
// Obtener un perfil de un usuario
{
 Url: "{HOST_API}/api/auth/profile/",
 Method: "POST",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 },
 Body: {
  "username": "{Usuario}"
 }
}
```

HTTP Responses

***

> El `username` no existe:
> × HTTP_404_NOT_FOUND
> `{"detail":"No User matches the given query."}`

***

> El `username` existe:
> ✓ HTTP_200_OK
> `{"data":{"id":{..},"username":"{..}","email":"{..}}"}}`

***

##### Rutas del CRUD

###### Ruta_Projects

Permisos: [Protegido(Usuario)]

```json
// Obtener todos los proyectos
{
 Url: "{HOST_API}/api/v1/projects/",
 Method: "GET",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 }
}
```

HTTP Responses:

***

> ✓ HTTP_200_OK
> `[{id:0,name: "Proj1",...}, ...]`
> *Si no hay elementos (proyectos)*
> `[]`

***

```json
// Crear un nuevo proyecto
{
 Url: "{HOST_API}/api/v1/projects/",
 Method: "POST",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 },
 Body: {
  "name": "{Nombre}",
  "description": "{Descripción}",
  "objective": "{Objetivo}",
  "start_date": "{FechaDeInicio}",
  "end_date": "{FechaDeFin}"
 }
}
```

HTTP Responses:

***

> Si el `name` existe:
> × HTTP_400_BAD_REQUEST
> `{"name":["project with this name already exists."]}`

***

> Falta algún dato requerido:
> × HTTP_400_BAD_REQUEST
> `[{"NombreDelCampo": ["This field is required"]},{...}]

***

> Tipo de fecha incorrecto:
> × HTTP_400_BAD_REQUEST
> `{"NombreDelCampo":["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."], ...}`

***

> ✓ HTTP_201_CREATED
> `[{id:0,name:...},...]`

***

###### Ruta_Project

Permisos: [Protegido(Usuario)]

```json
// Obtener datos de proyecto 
{
 Url: "{HOST_API}/api/v1/projects/{id}",
 Method: "GET",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 }
}
```

HTTP Responses:

> Si no existe el proyecto con el `{id}`
> × HTTP_404_NOT_FOUND
> `{"detail":"No Project matches the given query."}`

***

> ✓ HTTP_200_OK
> `{id:0,name: "Proj1",...}`

***

```json
// Actualizar un proyecto 
{
 Url: "{HOST_API}/api/v1/projects/{id}",
 Method: "PUT",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 }
}
```

HTTP Responses:

> Si no existe el proyecto con el `{id}`
> × HTTP_404_NOT_FOUND
> `{"detail":"No Project matches the given query."}`

***

> Si algunos de los datos unicos `[name]` a actualizar existe:
> × HTTP_400_BAD_REQUEST
> `{"name":["project with this name already exists."]}`

***

> Tipo de fecha incorrecto:
> × HTTP_400_BAD_REQUEST
> `{"NombreDelCampo":["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."], ...}`

***

> ✓ HTTP_201_CREATED
> `[{id:0,name:...},...]`

***

###### Ruta_Tasks

Permisos: [Protegido(Usuario)]

```json
// Obtener todos las tareas de un proyecto de id específico
{
 Url: "{HOST_API}/api/v1/projects/{id}/tasks/",
 Method: "GET",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 }
}
```

HTTP Responses:

> Si no existe el proyecto con el `{id}`
> × HTTP_404_NOT_FOUND
> `{"detail":"No Project matches the given query."}`

***

> ✓ HTTP_200_OK
> `[{id:0,name: "Task1",...}, ...]`
> *Si no hay elementos (proyectos)*
> `[]`

***

```json
// Crear una nueva tarea en un proyecto específico
{
 Url: "{HOST_API}/api/v1/projects/{id}/tasks/",
 Method: "POST",
 Headers: {
  "Content-Type": "application/json",
  "Authorization": "Token {token..}"
 },
 Body: {
  "name": "{Nombre}",
  "description": "{Descripción}",
  "assigned_to": "{TeamMembers || null}",
  "start_date": "{FechaDeInicio}",
  "end_date": "{FechaDeFin}",
  "status": "{CHOICE_STATUS}"
 }
}
```

Elementos con valores escogidos:

**[CHOICE_STATUS](#Choice_Status)**

###### Ruta_Task

***

The dev is working here!! 

***

***


###### Ruta_TeamMembers

***

The dev is working here!! 

***

***

###### Ruta_TeamMember

***

The dev is working here!! 

***

***

##### Choices Values

Son un conjunto de (llave, valor) que permiten limitar la cantidad de opciones a la hora de completar un campo.
Para completar un campo solo se utiliza la llave elegida del grupo de selección disponible.

HTTP Responses:

***

> Si selecciona un valor fuera de la lista:
> × HTTP_400_BAD_REQUEST
> {"{NombreDelCampo}":["\"{TuValor}\" is not a valid choice."]}

***

###### Choice_Status

> Son valores que establecen el estado de una tarea en el campo `[status]`

```python
STATUS_CHOICES = [
    ('new', 'Nueva'),
    ('assigned', 'Asignada'),
    ('accepted', 'Aceptada'),
    ('resolved', 'Resuelta'),
    ('closed', 'Cerrada')
]
# DEFAULT=('new', 'Nueva')
```

###### Choice_Role

> Son valores que establecen el rol de un miembro del equipo en el campo `[role]`

```python
ROLE_CHOICES = [
    ('backend', 'Backend Developer'),
    ('frontend', 'Frontend Developer'),
    ('fullstack', 'Fullstack Developer'),
    ('devops', 'DevOps Engineer'),
    ('qa', 'QA Engineer'),
    ('uxui', 'UX/UI Designer'),
    ('project_manager', 'Project Manager')
]
```

###### Choice_Gender

> Son los valores que establecen el género de un miembro de equipo en el campo `[gender]`

```python
GENDER_CHOICES = [
    ('m', 'Male'),
    ('f', 'Female')
]
```