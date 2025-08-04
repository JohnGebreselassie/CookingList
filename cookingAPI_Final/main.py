from fastapi import FastAPI
import database
from api_endpoints import user


app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
