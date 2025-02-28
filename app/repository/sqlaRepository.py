from typing import Sequence, Type, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repository.repoInterface import RepositoryInterface


class SqlalchemyRepository[T](RepositoryInterface):

    def __init__(self, scheme_model: T):
        self._scheme_model = scheme_model

    def all(self, session: Session) -> Sequence[T]:
        req = select(self._scheme_model)
        result_rows = session.scalars(req).all()
        return result_rows

    def get_one(self, session: Session, unique_values: Dict) -> Type[T] | None:
        return session.get(self._scheme_model, unique_values)

    def add(self, session: Session, item: T) -> None:
        session.add(item)

    def delete(self, session: Session, item: T):
        session.delete(self._scheme_model)
