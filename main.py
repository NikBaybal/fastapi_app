from typing import Optional, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict

from contextlib import asynccontextmanager
from database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

app = FastAPI(lifespan=lifespan)

class STaskAdd(BaseModel):
    name:str
    description: Optional[str]=None

class STask(STaskAdd):
    id:int
    model_config = ConfigDict(from_attributes=True)

tasks=[]

@app.post('/tasks')
async def add_task(
        task: Annotated[STaskAdd, Depends()]
):
    tasks.append(task)
    return{'ok':True}


# @app.get('/tasks')
# def get_tasks():
#     task = Task(name='Запиши это видео')
#     return {"data": task}
