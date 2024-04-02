import os
from dataclasses import dataclass
from typing import Self


@dataclass
class ApplicationConfiguration:
    host: str
    port: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            host=os.environ.get('APPLICATION_HOST', '0.0.0.0'),
            port=os.environ.get('APPLICATION_PORT', '50501'),
        )
