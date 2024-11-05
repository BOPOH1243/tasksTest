from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_async_session, init_db  # Импортируйте вашу функцию для получения сессии
from schemas import TaskCreate, TaskUpdate, Task  # Импортируйте Pydantic схемы
from crud import crud_task  # Импортируйте ваши CRUD операции
from typing import List
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print('первый запуск')
    print('инициализация БД')
    await init_db()
    print('инициализация бд прошла')

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud_task.create_task(db=db, task=task)

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    task = await crud_task.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    tasks = await crud_task.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_async_session)):
    db_task = await crud_task.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    await crud_task.delete_task(db=db, task_id=task_id)
    return {"detail": "Task deleted successfully"}
