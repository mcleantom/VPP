from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class Backends:
    backends = {}

    @classmethod
    def register(cls, backend: BackendHandler):
        cls.backends[backend] = backend


class BackendHandler(ABC):
    operations = {}

    @classmethod
    def handle(self, fn):
        self.__class__.operations[fn] = fn
        return fn

    @abstractmethod
    @classmethod
    def __module(cls):
        ...
