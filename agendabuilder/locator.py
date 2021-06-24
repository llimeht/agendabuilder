from pathlib import Path
from typing import (
    Union,
)


class FileLocator:
    def __init__(self, config_filename: Union[str, Path]) -> None:
        self.base = Path(config_filename).parent

    def find(self, filename: Union[str, Path]) -> Path:
        loc = Path(filename)

        if loc.is_absolute():
            return loc

        return self.base / loc

    def __call__(self, filename: Union[str, Path]) -> Path:
        return self.find(filename)
