import os
from dataclasses import dataclass
from typing import Self


@dataclass
class DatabaseConfiguration:
    user: str
    password: str
    host: str
    port: str
    database: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            database=os.environ['DB_DATABASE'],
        )
