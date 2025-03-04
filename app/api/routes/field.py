import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import repository as repos
from app.core.db import async_sessionmaker
from app.models import Fields

router = APIRouter(prefix="/field")


class FieldComprehensionScheme(BaseModel):
    field_id: uuid.UUID
    field_name: str
    field_mark: int


class StudentComprehension(BaseModel):
    student_id: int
    name: str
    mark: int


@router.get("/student/{student_id}", response_model=List[FieldComprehensionScheme])
async def get_student_marks(student_id: int) -> List[FieldComprehensionScheme] | HTTPException:
    try:
        async with async_sessionmaker() as session:
            student_fields = await repos.FieldComprehensionRepository.get_by_filter(
                session,
                f"student_id = :student_id",
                {"student_id": student_id}
            )

            fields_sequence = await repos.FieldRepository.all(session)
            fields_dict = {field.field_id: field for field in fields_sequence}

        response_data = []
        for field_com_model in student_fields:
            response_data.append(
                FieldComprehensionScheme(
                    field_id=field_com_model.field,
                    field_name=fields_dict[field_com_model.field].field_name,
                    field_mark=field_com_model.mark
                )
            )

        return response_data

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.get("/professor/{professor_id}/fields", response_model=List[Fields])
async def get_professors_fields(professor_id: int) -> List[str] | HTTPException:
    try:
        session: AsyncSession
        async with async_sessionmaker() as session:
            fields = await repos.FieldRepository.get_by_filter(
                session,
                f"professor_id = :professor_id",
                {"professor_id": professor_id}
            )

            return fields

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.get("/professor/{field_id}/groups", response_model=List[Fields])
async def get_professors_field_groups(field_id: int) -> List[str] | HTTPException:
    try:
        session: AsyncSession
        async with async_sessionmaker() as session:
            res = await session.execute(
                text(
                    """
                    with educated_students as (
                        select * from field_comprehensions where field = :field_id
                    )
                    select distinct students_group_number from students where student_id in (select student_id from educated_students)
                    """,

                ),
                {"field_id": field_id}
            )

            groups = []
            for group_tuple in res:
                groups.append(
                    group_tuple[0]
                )

            return groups

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")


@router.get("/professor/get_group_comprehension")
async def get_group_comprehension(group_name: str, field_id: str) -> List[StudentComprehension] | HTTPException:
    try:
        session: AsyncSession
        async with async_sessionmaker() as session:
            query = await session.execute(
                text(
                    """
                    select f.student_id, last_name, first_name, patronymic, mark from students s join field_comprehensions f on s.student_id = f.student_id where students_group_number = :group_name and field_id = :field_id
                    """
                ),
                {
                    "group_name": group_name,
                    "field_id": field_id
                }
            )

            groups = []
            for group_tuple in query:
                groups.append(
                    StudentComprehension(
                        student_id=int(group_tuple[0]),
                        name=" ".join(group_tuple[1:4]),
                        mark=int(group_tuple[4]) if group_tuple[4] not in ["", " "] else 0
                    )
                )

            return groups

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")
