from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    completed: bool


todo_store: List[Task] = []


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return todo_store


@app.post("/tasks", response_model=List[Task], status_code=201)
def create_tasks(todo_payload: List[Task]):
    todo_store.extend(todo_payload)
    return todo_store


@app.get("/tasks/{id}", response_model=Task)
def get_task_by_id(id: int):
    for task in todo_store:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{id}", response_model=Task)
def delete_task_by_id(id: int):
    for task in todo_store:
        if task.id == id:
            todo_store.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks", response_model=List[Task])
def delete_tasks(ids: List[int]):
    global todo_store   # ✅ doit être déclaré avant utilisation
    deleted = []
    remaining = []
    for task in todo_store:
        if task.id in ids:
            deleted.append(task)
        else:
            remaining.append(task)
    todo_store = remaining
    return deleted
