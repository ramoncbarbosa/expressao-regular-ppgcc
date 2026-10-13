import argparse
from app.validator import list_fields, validator


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="validador de expressões regulares."
    )

    parser.add_argument(
        "field",
        choices=list_fields(),
        help="campo que será validado.",
    )

    parser.add_argument(
        "value",
        help="valor que será validado.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    arguments = parser.parse_args()

    is_valid = validator(
        input_field=arguments.field,
        value=arguments.value,
    )

    result = "ACEITO" if is_valid else "REJEITADO"
    print(result)


if __name__ == "__main__":
    main()