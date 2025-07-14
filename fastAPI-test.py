from fastapi import FastAPI

api = FastAPI()

@api.get('/') #choosing your endpoint, '/' = location
def index():
    return {"message": "Hello World"}
#endpoint types(popular):
#GET - get information from server
#POST - create something new to server
#PUT - change something in server
#DELETE - delete information in server

