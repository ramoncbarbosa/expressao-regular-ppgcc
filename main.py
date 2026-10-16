import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from app.validator import list_fields, validator


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="validate values with regular expressions."
    )
    parser.add_argument(
        "command",
        choices=(*list_fields(), "batch", "interactive"),
        help="field name, batch, or interactive",
    )
    parser.add_argument(
        "value",
        nargs="?",
        help="value to validate or test-case file for batch mode",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        help="save results to a JSON file",
    )
    return parser


def read_test_cases(file_path: Path) -> list[dict[str, Any]]:
    test_cases: list[dict[str, Any]] = []

    with file_path.open(encoding="utf-8", newline="") as test_file:
        for line_number, line in enumerate(test_file, start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue

            try:
                row = next(csv.reader([line], delimiter=";", strict=True))
            except csv.Error as error:
                raise ValueError(
                    f"line {line_number}: invalid CSV: {error}"
                ) from error

            if len(row) != 3:
                raise ValueError(
                    f"line {line_number}: expected field;value;expected"
                )

            field, value, expected = row
            field = field.strip().lower()
            expected = expected.strip().lower()

            if field not in list_fields():
                raise ValueError(
                    f"line {line_number}: unknown field: {field}"
                )
            if expected not in {"accepted", "rejected"}:
                raise ValueError(
                    f"line {line_number}: expected accepted or rejected"
                )

            test_cases.append(
                {
                    "line": line_number,
                    "field": field,
                    "value": value,
                    "expected": expected,
                }
            )

    return test_cases


def save_json_report(
    file_path: Path,
    mode: str,
    results: list[dict[str, Any]],
) -> None:
    passed = sum(result.get("passed") is True for result in results)
    failed = sum(result.get("passed") is False for result in results)
    accepted = sum(result["actual"] == "accepted" for result in results)
    rejected = sum(result["actual"] == "rejected" for result in results)

    report = {
        "mode": mode,
        "summary": {
            "total": len(results),
            "accepted": accepted,
            "rejected": rejected,
            "passed": passed,
            "failed": failed,
        },
        "results": results,
    }

    with file_path.open("w", encoding="utf-8") as json_file:
        json.dump(report, json_file, ensure_ascii=False, indent=2)
        json_file.write("\n")


def run_batch(file_path: Path, json_path: Path | None) -> int:
    try:
        test_cases = read_test_cases(file_path)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    for test_case in test_cases:
        actual = (
            "accepted"
            if validator(test_case["field"], test_case["value"])
            else "rejected"
        )
        passed = actual == test_case["expected"]
        result = {
            **test_case,
            "actual": actual,
            "passed": passed,
        }
        results.append(result)

        status = "PASS" if passed else "FAIL"
        print(
            f"Line {test_case['line']}: {status} - "
            f"{test_case['field']}: {actual.upper()} "
            f"(expected {test_case['expected'].upper()})"
        )

    passed_count = sum(result["passed"] for result in results)
    failed_count = len(results) - passed_count
    print(
        f"Batch finished: {passed_count}/{len(results)} passed, "
        f"{failed_count} failed."
    )

    if json_path is not None:
        try:
            save_json_report(json_path, "batch", results)
        except OSError as error:
            print(f"Error saving JSON: {error}", file=sys.stderr)
            return 2
        print(f"JSON saved to {json_path}")

    return 1 if failed_count else 0


def run_interactive(json_path: Path | None) -> int:
    fields = list_fields()
    current_field: str | None = None
    results: list[dict[str, Any]] = []

    print(
        "Fields: " + ", ".join(fields) + ". "
        "Type a field name to select it or 'exit' to finish."
    )

    while True:
        prompt = f"{current_field}> " if current_field else "> "
        try:
            entry = input(prompt)
        except EOFError:
            print()
            break

        command = entry.strip().lower()
        if command in {"exit", "quit"}:
            break

        if command in fields:
            current_field = command
            print(f"Selected field: {current_field}")
            continue

        if current_field is None:
            print("Select a field first.")
            continue

        actual = "accepted" if validator(current_field, entry) else "rejected"
        print(actual.upper())
        results.append(
            {
                "field": current_field,
                "value": entry,
                "expected": None,
                "actual": actual,
                "passed": None,
            }
        )

    print(f"Session finished: {len(results)} value(s) checked.")
    if json_path is not None:
        try:
            save_json_report(json_path, "interactive", results)
        except OSError as error:
            print(f"Error saving JSON: {error}", file=sys.stderr)
            return 2
        print(f"JSON saved to {json_path}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    arguments = parser.parse_args(argv)

    if arguments.command == "interactive":
        if arguments.value is not None:
            parser.error("interactive mode does not take a value")
        return run_interactive(arguments.json_path)

    if arguments.command == "batch":
        if arguments.value is None:
            parser.error("batch mode requires a test-case file")
        return run_batch(Path(arguments.value), arguments.json_path)

    if arguments.value is None:
        parser.error("field validation requires a value")

    actual = "accepted" if validator(arguments.command, arguments.value) else "rejected"
    print(actual.upper())

    if arguments.json_path is not None:
        result = {
            "field": arguments.command,
            "value": arguments.value,
            "expected": None,
            "actual": actual,
            "passed": None,
        }
        try:
            save_json_report(arguments.json_path, "single", [result])
        except OSError as error:
            print(f"Error saving JSON: {error}", file=sys.stderr)
            return 2
        print(f"JSON saved to {arguments.json_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
