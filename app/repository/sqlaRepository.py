from typing import Sequence, Type, Dict

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.repository.repoInterface import RepositoryInterface


class SqlalchemyRepository[T](RepositoryInterface):

    def __init__(self, scheme_model: T):
        self._scheme_model = scheme_model

    async def all(self, session: AsyncSession) -> Sequence[T]:
        req = select(self._scheme_model)
        rows_future = await session.scalars(req)
        result_rows = rows_future.all()
        return result_rows

    async def get_by_filter(self, session: AsyncSession, unique_where: str) -> Sequence[T] | None:
        req = (
            select(self._scheme_model)
            .where(text(unique_where))
        )
        rows_future = await session.scalars(req)
        result_rows = rows_future.all()
        return result_rows

    async def get_one(self, session: AsyncSession, unique_values: Dict) -> Type[T] | None:
        student = await session.get(self._scheme_model, unique_values)
        return student

    async def add(self, session: AsyncSession, item: T) -> None:
        session.add(item)

    def delete(self, session: AsyncSession, item: T):
        session.delete(self._scheme_model)
