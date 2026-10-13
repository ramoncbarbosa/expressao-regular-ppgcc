import re
from typing import Final

CPF: Final[re.Pattern[str]] = re.compile(
    r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"
)

def validator_cpf(value: str) -> bool:
    return CPF.fullmatch(value) is not None