import unittest
from collections.abc import Callable
from app.validator import list_fields, validator
from app.validators import (
    validator_cpf,
    validator_email,
    validator_name,
    validator_password,
    validator_phone,
)


Validator = Callable[[str], bool]


class TestValidators(unittest.TestCase):

    def assert_validation_cases(
        self,
        selected_validator: Validator,
        accepted: list[str],
        rejected: list[str],
    ) -> None:
        for value in accepted:
            with self.subTest(
                value=value,
                expected="accepted",
            ):
                self.assertTrue(
                    selected_validator(value),
                    msg=f"o valor deveria ser aceito: {value!r}",
                )

        for value in rejected:
            with self.subTest(
                value=value,
                expected="rejected",
            ):
                self.assertFalse(
                    selected_validator(value),
                    msg=f"o valor deveria ser rejeitado: {value!r}",
                )

    def test_name_validator(self) -> None:
        accepted = [
            "Alan Turing",
            "Noam Chomsky",
            "Ada Lovelace",
        ]

        rejected = [
            "",
            "1Alan",
            "Alan",
            "A1an",
            "A1an Turing",
            "alan Turing",
            "Alan turing",
            "Alan  Turing",
            "Alan Turing Silva",
            "João Silva",
            "Alan-Turing",
        ]

        self.assert_validation_cases(
            validator_name,
            accepted,
            rejected,
        )

    def test_email_validator(self) -> None:
        accepted = [
            "a@a.br",
            "divulga@ufpa.br",
        ]

        rejected = [
            "",
            "@",
            "a@.br",
            "T@teste.br",
            "a@@teste.br",
            "@teste.br",
            "a@Teste.br",
            "a.silva@teste.br",
            "a@sub.teste.br",
            "teste@dominio.com",
            "usuario@servidor.com.br",
            "a@teste.net",
            "a@teste.br.com",
        ]

        self.assert_validation_cases(
            validator_email,
            accepted,
            rejected,
        )

    def test_password_validator(self) -> None:
        accepted = [
            "518R2r5e",
            "F123456A",
            "1234567T",
            "ropsSoq0",
        ]

        rejected = [
            "",
            "F1234567A",
            "abcdefgH",
            "1234567HI",
            "12345678",
            "abcdefgh",
            "ABCDEFGH",
            "Abc!1234",
            "Abc123",
        ]

        self.assert_validation_cases(
            validator_password,
            accepted,
            rejected,
        )

    def test_cpf_validator(self) -> None:
        accepted = [
            "123.456.789-09",
            "000.000.000-00",
        ]

        rejected = [
            "",
            "123.456.789-0",
            "111.111.11-11",
            "12345678909",
            "123-456-789.09",
            "123.456.789.09",
            "abc.def.ghi-jk",
        ]

        self.assert_validation_cases(
            validator_cpf,
            accepted,
            rejected,
        )

    def test_phone_validator(self) -> None:
        accepted = [
            "(91) 99999-9999",
            "(91) 999999999",
            "91 999999999",
        ]

        rejected = [
            "",
            "(91) 59999-9999",
            "99 99999-9999",
            "(94)95555-5555",
            "(91) 9999-9999",
            "(091) 99999-9999",
            "91 99999-9999",
            "91999999999",
        ]

        self.assert_validation_cases(
            validator_phone,
            accepted,
            rejected,
        )

    def test_generic_validator_accepts_valid_value(self) -> None:
        self.assertTrue(
            validator("name", "Alan Turing")
        )

    def test_generic_validator_rejects_invalid_value(self) -> None:
        self.assertFalse(
            validator("email", "T@teste.br")
        )

    def test_generic_validator_selects_all_fields(self) -> None:
        cases = {
            "name": "Ada Lovelace",
            "email": "a@a.br",
            "password": "1234567T",
            "cpf": "000.000.000-00",
            "phone": "91 999999999",
        }

        for field, value in cases.items():
            with self.subTest(field=field, value=value):
                self.assertTrue(
                    validator(field, value)
                )

    def test_unknown_field_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "campo desconhecido: rg",
        ):
            validator("rg", "1234567")

    def test_list_fields(self) -> None:
        self.assertEqual(
            list_fields(),
            (
                "name",
                "email",
                "password",
                "cpf",
                "phone",
            ),
        )


if __name__ == "__main__":
    unittest.main()