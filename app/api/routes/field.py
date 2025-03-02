import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

import app.repository as repos
from app.core.db import async_sessionmaker

router = APIRouter(prefix="/field")


class FieldComprehensionScheme(BaseModel):
    field_id: uuid.UUID
    field_name: str
    field_mark: int


@router.get("/{student_id}", response_model=List[FieldComprehensionScheme])
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
