import re
from typing import Final

PHONE: Final[re.Pattern[str]] = re.compile(
    r"(?:"
        r"\([0-9]{2}\) 9[0-9]{4}-[0-9]{4}"
        r"|"
        r"\([0-9]{2}\) 9[0-9]{8}"
        r"|"
        r"[0-9]{2} 9[0-9]{8}"
    r")"
)

def validator_phone(value: str) -> bool:
    return PHONE.fullmatch(value) is not None