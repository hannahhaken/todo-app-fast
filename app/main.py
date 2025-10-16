from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import engine, get_db

import os

if os.getenv("TESTING") != "true":
    models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A simple todo list API built with FastAPI",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Todo API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post("/todos", response_model=schemas.TodoResponse, status_code=201)
def create_todo(
        todo: schemas.TodoCreate,
        db: Session = Depends(get_db)
):
    return crud.create_todo(db=db, todo=todo)


@app.get("/todos", response_model=List[schemas.TodoResponse])
def get_todos(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_todos(db=db, skip=skip, limit=limit)


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
        todo_id: int,
        db: Session = Depends(get_db)
):
    db_todo = crud.get_todo(db=db, todo_id=todo_id)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.patch("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
        todo_id: int,
        todo: schemas.TodoUpdate,
        db: Session = Depends(get_db)
):
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo=todo)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schemas.TodoResponse)
def delete_todo(
        todo_id: int,
        db: Session = Depends(get_db)
):
    db_todo = crud.delete_todo(db=db, todo_id=todo_id)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return db_todo
