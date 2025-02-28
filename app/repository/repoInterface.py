from abc import ABC, abstractmethod


class RepositoryInterface(ABC):

    @abstractmethod
    def all(self, session):
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
