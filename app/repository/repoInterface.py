from abc import ABC, abstractmethod


class RepositoryInterface(ABC):

    @abstractmethod
    def all(self, session):
        raise NotImplemented

    @abstractmethod
    def get_by_filter(self, session, unique_where, where_column_values):
        raise NotImplemented

    @abstractmethod
    def get_one(self, session, unique_values):
        raise NotImplemented

    @abstractmethod
    def add(self, session, item):
        raise NotImplemented

    @abstractmethod
    def delete(self, session, item):
        raise NotImplemented
