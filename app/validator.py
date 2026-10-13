from collections.abc import Callable
from typing import Final

from app.validators import (
    validator_name,
    validator_email,
    validator_password,
    validator_cpf,
    validator_phone,
)

Validator = Callable[[str], bool]

VALIDATORS: Final[dict[str, Validator]] = {
    "name": validator_name,
    "email": validator_email,
    "password": validator_password,
    "cpf": validator_cpf,
    "phone": validator_phone,
}

def validator(input_field: str, value: str) -> bool:
    try:
        selected_validator = VALIDATORS[input_field]
    except KeyError as error:
        raise ValueError(
            f"campo desconhecido: {input_field}"
        ) from error

    return selected_validator(value)


def list_fields() -> tuple[str, ...]:
    return tuple(VALIDATORS)