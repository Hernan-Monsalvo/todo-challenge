# # Invera ToDo-List Challenge

## Descripcion de la app

esta es una aplicacion desarollada en Django Rest Framework, la misma le permite al usuario crear tareas, modificarlas y eliminarlas. cuenta con un sistema de registro/login que le entrega al usuario un token para authenticarse en las llamadas a la API.

## Levantar aplicacion
para levantar la aplicacion hay dos opciones:

### Docker
`docker run -p 8000:8000 hernanmonsalvo/django-todo:v1.0.0`

### Python
`./start.sh`

## Endpoints

- ### Register (post)
 url: "localhost:8000/auth/register"  
 Crea un usuario.  
 recibe: "username" y "password"  

- ### Login  (post)
 url: "localhost:8000/auth/register"
 Authentica un usuario.
 recibe: "username" y "password"
 devuelve: "token"

- ### Create Task  (post)
 url: "localhost:8000/todo/tasks"
 Auth header: "Authorization: Token {{userToken}}"
 Crea una tarea.
 recibe: "title" y "description"
 devuelve: tarea creada

- ### Task List  (get)
 url: "localhost:8000/todo/tasks"
 Auth header: "Authorization: Token {{userToken}}"
 Lista de tareas.

- ### Task Detail  (get)
 url: "localhost:8000/todo/tasks/{{task_id}}"
 Auth header: "Authorization: Token {{userToken}}"
 Detalle de tarea.

- ### Delete Task  (delete)
 url: "localhost:8000/todo/tasks/{{task_id}}"
 Auth header: "Authorization: Token {{userToken}}"
 Elimina una tarea.

- ### Update Task  (patch)
 url: "localhost:8000/todo/tasks/{{task_id}}"
 Auth header: "Authorization: Token {{userToken}}"
 Modifica una tarea.
 campos modificables: "title", "description", "completed"


**documentacion mas detallada** con ejemplos se encuentra en el archivo doc.html (generado por postman).
