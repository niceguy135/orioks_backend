import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import app.repository as repos
from app.core.db import async_sessionmaker

router = APIRouter(prefix="/field")


class FieldComprehensionScheme(BaseModel):
    field_id: uuid.UUID
    field_name: str
    field_mark: int


@router.get("/student/{student_id}", response_model=List[FieldComprehensionScheme])
async def get_student_marks(student_id: int) -> List[FieldComprehensionScheme] | HTTPException:
    try:
        async with async_sessionmaker() as session:
            student_fields = await repos.FieldComprehensionRepository.get_by_filter(
                session,
                f"student_id == :student_id",
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


@router.get("/professor/{professor_id}/fields")
async def get_professors_groups(professor_id: int) -> List[str] | HTTPException:

    try:
        session: AsyncSession
        async with async_sessionmaker() as session:
            query = await session.execute(
                text(
                    """
                    with professor_fields as (
                        select * from fields where professor_id = :professor_id
                    ), educated_students as (
                        select * from field_comprehensions where field in (select field_id from professor_fields)
                    )
                    select distinct students_group_number from students where student_id in (select student_id from educated_students)
                    """
                ),
                {"professor_id": professor_id}
            )

            groups = []
            for group_tuple in query:
                groups.append(
                    group_tuple[0]
                )

            return groups

    except SQLAlchemyError as e:
        return HTTPException(400, f"Bad DB request.\nCause:{e}")
