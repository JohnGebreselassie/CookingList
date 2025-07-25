from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import database

api = FastAPI()
database.Base.metadata.create_all(bind=database.engine)