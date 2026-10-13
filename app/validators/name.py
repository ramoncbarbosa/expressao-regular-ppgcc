import re
from typing import Final

NAME: Final[re.Pattern[str]] = re.compile(
    r"[A-Z][a-z]* [A-Z][a-z]*"
)

def validator_name(value: str) -> bool:
    return NAME.fullmatch(value) is not None