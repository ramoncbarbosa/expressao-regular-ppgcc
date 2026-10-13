import re
from typing import Final

PASSWORD: Final[re.Pattern[str]] = re.compile(
    r"(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{8}"
)

def validator_password(value: str) -> bool:
    return PASSWORD.fullmatch(value) is not None