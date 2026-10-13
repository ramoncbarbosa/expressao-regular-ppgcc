from app.validators.name import validator_name
from app.validators.email import validator_email
from app.validators.password import validator_password
from app.validators.cpf import validator_cpf
from app.validators.phone import validator_phone

__all__ = [
    "validator_name",
    "validator_email",
    "validator_password",
    "validator_cpf",
    "validator_phone",
]