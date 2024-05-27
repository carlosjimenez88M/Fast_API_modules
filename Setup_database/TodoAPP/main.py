#================================================#
#     Design  Database Server with FastAPI       #
#              FastAPI Practices                 #
#================================================#


# libraries ---------------


from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from database import engine, SessionLocal
import models
from models import Todos
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI(title='V1')

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,
                             max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool



@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(Todos).all()

@app.get('/todo/{todo_id}',status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int = Path(gt=0),
                    db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,
                            detail="Todo not found")
    return todo_model


@app.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: Session = Depends(get_db)):
    todo_model = Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)  # Ensure the new object is updated with its new ID
    return todo_model



## Create Update method -------

@app.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)

async def update_todo(todo_id: int,
                      todo_request=TodoRequest,
                      db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,
                            detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


## Add method delete ------


@app.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)


async def delete_todo(todo_id: int = Path(gt=0),
                      db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id== todo_id).first()
    if todo_model is None :
        raise HTTPException(status_code=404,
                            detail='Todo not found')
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()