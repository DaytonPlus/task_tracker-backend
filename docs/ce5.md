## Caso de estudio 5: Empresa de software

**Descripción**: *Una empresa de software busca una solución informática para gestionar sus proyectos de desarrollo de software. La empresa necesita un sistema que permita la asignación y seguimiento de tareas, la colaboración entre equipos y la generación de informes de progreso.*

### Sobre el sistema:

* `Dispondrá de varios espacios para la gestión y visualización de la información que se requiere.`
* `Debe brindar la posibilidad de conocer en todo momento la fecha y la hora en que la información fue almacenada o modificada, así como el usuario que realiza la acción.`


[`Frontend: Angular`]

Empleando una estructura basada en módulos que agrupen componentes para gestionar la información que se determine.

***

[`Backend: Django Rest Framework`]

Mediante una API REST que facilitar la persistencia de la información de la base de datos `PostgreSQL`.

***

### Información recepcionada:

**Proyectos**: `[nombre del proyecto, descripción, objetivos, fecha de inicio, fecha de fin]`

**Tareas**: `[nombre, descripción, responsable de la tarea, fecha de inicio, fecha de fin, estado de la tarea]`

**Miembros del equipo**: `[nombres y apellidos, número de identidad, correo electrónico, número de contacto, sexo, proyecto, rol en el proyecto]`

#### Valores escogidos:

**Estados de una tarea**: `[Nueva, Asignada, Aceptada, Resuelta, Cerrada]`

**Rol en el Proyecto**: `[probador, analista, jefe de proyecto, arquitecto, programador, ...]`


### Funcionalidades:

* `Autenticación y registro de usuarios.`
* `Gestión de proyectos en el sistema (CRUD).`
* `Gestión de miembros del equipo en el sistema (CRUD).`
* `Gestión de tareas en el sistema (CRUD).`
* `Realizar búsquedas y filtrar tareas por nombre, responsable, fecha de inicio o fecha de fin.`
* `Exportar listado de tareas [PDF, EXCEL]`



### Información agregada:

Gestión de los proyectos y las tareas en el sistema:
* Cada Usuario solo puede estar en un unico proyecto, pero ser asignada a más de una tarea de ese proyecto

?? El problema es que si un Usuario cualquiera con rol basico quiere, puede elimnar el proyecto completo, las tareas, usuarios..
* ?? Que Usuario puede acutualizar, elimnar o crear Proyectos (admin, rol de jefe)
* ?? Que Usuario puede acutualizar, elimnar o crear Tareas (admin, creador, rol superior al creador)

* Por relación cada tarea está vinculada a un proyecto específico `(No hay tareas que no esten vinculadas a un proyecto)`, al crear una tarea, esta debe tener relación directa con un proyecto `(En un proyecto específico se crea la tarea)`.
* Si se elimina un proyecto por ende también las tareas de ese proyecto, en el caso de los miembros del equipo vinculados a ese proyecto se mantienen pero se eliminan sus relaciones con ese proyecto y sus tareas (auto, no es necesario implementar).
* Si se elimina un miembro de equipo las tareas vinculadas quedan en el estado [`Nueva`] (auto, Es necesario implementar para que se establezca en `Nueva`)
* Si se elimina una tarea se desvincula el miembro del equipo asignado (No es necesario ya que la tarea es quien tiene a quien fue asignado)


Gestión de Usuarios del Sistema:
* Al crear un Usuario por defecto no debe tener un proyecto asignado

? ?? El jefe de proyecto o creador tiene que aceptar al Usuario que quiere entrar al proyecto? Esto implicaría crear un panel de solicitudes y informar al Usuario cuando llege la solicitud o al que solicita cuando es aceptado o rechazado

* Los Usuarios solo pueden estar o no en un proyecto a la vez

? ?? Boton al ver un proyecto de (abandonar si está o unir si no está en ninguno)
? ?? Los Usuarios solo pueden [ver |o| no] las tareas de los [demas |o| solo el propio si esta], y solo pueden ser asignados, eliminar, actualizar si estan en ese proyecto (admin, segun el rol)
? ?? Los Usuarios tienen la opcion de abandonar si esta en un proyecto o integrar un proyecto si no esta vinculado a ningún otro

* CRUD del Usuario `/login, /register, /profile`

? ?? Panel para acutualizar los datos de un usuario
? ?? Los Usuarios pueden obtener o acutualizar solo sus propios datos

? ?? Panel de adminstración de Usuarios para admins o superusers
? ?? Solo admin puede acceder al CRUD completo en profile de otros usuarios no admins
? ?? Solo superuser puede acceder al CRUD completo en profile de todos los usuarios no superuser


Busqueda y Exportación
* Filtros de busqueda [GET] `/projects/find?{key}={value}/ , /projects/{id}/tasks/find?{key}={value}/`
* Crear EXCEL, Cear PDF desde el EXCEL `/projects/{id}/export-excel/ , /projects/{id}/export-pdf/`
? ?? No crear PDF sino convertir de excel a pdf, al final va a exportar pdf, o a excel