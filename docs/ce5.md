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

