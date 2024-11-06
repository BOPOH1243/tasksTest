from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models import Task  # Импортируйте вашу модель Task
from typing import List
from schemas import TaskCreate, TaskUpdate
from models import User
from typing import Optional

class CRUDTask:
    async def create_task(self, db: AsyncSession, task: TaskCreate) -> Task:
        db_task = Task(**task.dict())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    async def get_task(self, db: AsyncSession, task_id: int) -> Task:
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_tasks(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Task]:
        result = await db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_task(self, db: AsyncSession, task_id: int, task: TaskUpdate) -> Task:
        stmt = update(Task).where(Task.id == task_id).values(**task.dict()).execution_options(synchronize_session="fetch")
        await db.execute(stmt)
        await db.commit()
        return await self.get_task(db, task_id)

    async def delete_task(self, db: AsyncSession, task_id: int) -> None:
        stmt = delete(Task).where(Task.id == task_id)
        await db.execute(stmt)
        await db.commit()
class CRUDUser:
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create_user(self, db: AsyncSession, username: str, password_hash: str) -> User:
        db_user = User(username=username, password_hash=password_hash)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def get_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update_user(self, db: AsyncSession, user_id: int, new_data: dict) -> Optional[User]:
        stmt = update(User).where(User.id == user_id).values(**new_data).execution_options(synchronize_session="fetch")
        await db.execute(stmt)
        await db.commit()
        return await self.get_user(db, user_id)

    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        stmt = delete(User).where(User.id == user_id)
        await db.execute(stmt)
        await db.commit()

crud_user = CRUDUser()
crud_task = CRUDTask()
