import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

import app.repository as repos
from app.core.db import async_sessionmaker
from app.models import Students

router = APIRouter(prefix="/student")


class StudentScheme(BaseModel):
    last_name: str
    first_name: str
    students_group_number: str
    birthday: datetime.date
    patronymic: Optional[str]
    email: Optional[str]


@router.get("/", response_model=List[Students])
async def get_all_students() -> List[Students] | HTTPException:
    try:
        with async_sessionmaker() as session:
            students = await repos.StudentRepository.all(session)
            await session.commit()

        return list(students)

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.get("/{student_id}", response_model=Students)
async def get_student(student_id: int) -> Students | HTTPException | None:
    try:
        with async_sessionmaker() as session:
            student = await repos.StudentRepository.get_one(session, {"student_id": student_id})
            await session.commit()

        return student

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.post("/", response_model=HTTPException)
async def create_student(student_data: StudentScheme) -> HTTPException:
    new_student = Students(**student_data.model_dump())

    try:
        with async_sessionmaker() as session:
            repos.StudentRepository.add(session, new_student)
            await session.commit()

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")

    return HTTPException(201, "Student has been created")


@router.delete("/", response_model=HTTPException)
async def delete_student(student_data: StudentScheme) -> HTTPException:
    student_to_delete = Students(**student_data.model_dump())

    try:
        with async_sessionmaker() as session:
            repos.StudentRepository.delete(session, student_to_delete)
            await session.commit()

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")

    return HTTPException(200, "Student has been deleted")
