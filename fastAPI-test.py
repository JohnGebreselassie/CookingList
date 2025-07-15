from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()

#----------------------------------------------------CLASS DEFINITIONS-----------------------------------------------------------------
#The point of these classes is to simplify data modeling and checking later
#For example, if the API gets a request, these classes ensure what kind of data will be recieved and what will be returned
#defining these models is very important to ensure the API works very cleanly

class Priority(IntEnum): #priority for the todo, used in other classes
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class ToDoBase(BaseModel): #This is the base class that all others are using, but is never used itself
    todo_name: str = Field(..., min_length=1, max_length=512, description = "Name of todo")
    todo_description: str = Field(..., description = "description of todo")
    priority: Priority = Field(default = Priority.LOW, description = "priority of the todo")

class ToDo(ToDoBase): #Responses need their id as well, so you can return the id
    todo_id: int = Field(..., description = "unique id for todo instance")

class ToDoCreate(ToDoBase): #You need the exact same information as the base to post something new, so nothing new
    pass

class ToDoUpdate(BaseModel): #when updating, the difference is that everything is optional, you don't need to update anything specifically
    todo_name: Optional[str] = Field(None, min_length=1, max_length=512, description = "Name of todo")
    todo_description: Optional[str] = Field(None, description = "description of todo")
    priority: Priority = Field(None, description = "priority of the todo") 



#----------------------------------------------------MOCK SERVER-----------------------------------------------------------------

todos = [ #mock server to do list because this example video doesn't have a server(sqlAlchemy)
    ToDo(todo_id = 1,  todo_name = "do homework", todo_description = "do 120 homework", priority = Priority.HIGH),
    ToDo(todo_id = 2,  todo_name = "go work out", todo_description = "hit full exercise day", priority = Priority.MEDIUM),
    ToDo(todo_id = 3,  todo_name = "party hard", todo_description = "party harder then ever", priority = Priority.LOW)
]



#endpoint types(popular):
#GET - get information from server
#POST - create something new to server
#PUT - change something in server
#DELETE - delete information in server

@api.get('/') #choosing your endpoint, '/' = location in url
def index():
    return {"message": "Hello World"}


#----------------------------------------------------GET REQUESTS-----------------------------------------------------------------
@api.get('/to_do/',response_model = List[ToDo]) #to run this, add /to_do to the end of local host url - discord has example
def get_todos(firstn:int = None): #returns everything in to_do, uses query parameter if you want specifics - end is ?firstn=__, check discord
    if firstn:
        if firstn > len(todos) or firstn < 1:
            raise HTTPException(status_code = 400, detail = 'todo outside scope of data') #have to raise HTTP exceptions because the response model is expecting something specific, so it wont work if you return a string
        return todos[:firstn]
    else:
        return todos

@api.get('/to_do/{id}', response_model = ToDo) #response model - what you are returning
def get_specific_todos(id:int): #specify id type, gets all ids of type
    for i in todos:
        if i.todo_id == id:
            return i
    raise HTTPException(status_code = 404, dettail = 'id not found')

#----------------------------------------------------POST REQUESTS-----------------------------------------------------------------
@api.post('/to_do', response_model = ToDo)
def create_todo(new_todo: ToDoCreate): #uses create this time
    new_id = max(i.todo_id for i in todos) + 1
    new = ToDo(todo_id = new_id,  todo_name = new_todo.todo_name, todo_description = new_todo.todo_description, priority = new_todo.priority)
    todos.append(new)
    return new

#----------------------------------------------------PUT REQUESTS-----------------------------------------------------------------
@api.put('/to_do/{id}', response_model = ToDo)
def edit_todo(id:int, updated_todo: ToDoUpdate):
    if 0 < id < len(todos):
        for todo in todos:
            if todo.todo_id == id:
                if updated_todo.todo_name is not None:
                    todo.todo_name = updated_todo.todo_name
                if updated_todo.todo_description is not None:
                    todo.todo_description = updated_todo.todo_description
                if updated_todo.priority is not None:
                    todo.priority = updated_todo.priority
                return todo
            raise HTTPException(status_code = 404, dettail = 'id not found')
    else:
        raise HTTPException(status_code = 400, detail = 'todo outside scope of data')

#----------------------------------------------------PUT REQUESTS-----------------------------------------------------------------
@api.delete('/to_do/{id}', response_model = List)
def delete_todo(id:int):
    if 0 < id < len(todos):
        for todo in todos:
            if todo.todo_id == id:
                todos.remove(todo)
                return todos
            raise HTTPException(status_code = 404, dettail = 'id not found')
    else:
        raise HTTPException(status_code = 400, detail = 'todo outside scope of data')
