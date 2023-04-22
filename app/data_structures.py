from dataclasses import dataclass
from pathlib import Path


@dataclass
class AptPreference:
    """Represent preference entry. """

    package: str
    pin: str
    pin_priority: int
    file_path: Path
