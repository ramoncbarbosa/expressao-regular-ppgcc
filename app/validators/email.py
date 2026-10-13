import re
from typing import Final

EMAIL: Final[re.Pattern[str]] = re.compile(
    r"[a-z]+@[a-z]+\.br"
)

def validator_email(value: str) -> bool:
    return EMAIL.fullmatch(value) is not None