from typing import Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

import app.repository as repos
from app.core.db import async_sessionmaker
from app.models import Professors

router = APIRouter(prefix="/professors")


class StudentScheme(BaseModel):
    last_name: str
    first_name: str
    current_position: str
    experience: int
    patronymic: Optional[str]
    degree: Optional[str]
    academic_title: Optional[str]
    salary: Optional[int]


@router.get("/", response_model=List[Professors])
async def get_all_profs() -> List[Professors] | HTTPException:
    try:
        with async_sessionmaker() as session:
            professors = await repos.ProfessorRepository.all(session)
            await session.commit()

        return list(professors)

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.get("/{prof_id}", response_model=Professors)
async def get_professor(prof_id: int) -> Professors | HTTPException | None:
    try:
        with async_sessionmaker() as session:
            professor = await repos.ProfessorRepository.get_one(session, {"professor_id": prof_id})
            await session.commit()

        return professor

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.post("/", response_model=HTTPException)
async def create_student(student_data: StudentScheme) -> HTTPException:
    new_prof = Professors(**student_data.model_dump())

    try:
        with async_sessionmaker() as session:
            repos.ProfessorRepository.add(session, new_prof)
            await session.commit()

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")

    return HTTPException(201, "Professor has been created")


@router.delete("/", response_model=HTTPException)
async def delete_student(student_data: StudentScheme) -> HTTPException:
    prof_to_delete = Professors(**student_data.model_dump())

    try:
        with async_sessionmaker() as session:
            repos.ProfessorRepository.delete(session, prof_to_delete)
            await session.commit()

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")

    return HTTPException(200, "Professor has been deleted")
