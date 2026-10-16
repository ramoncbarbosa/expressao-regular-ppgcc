import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from main import main


class TestCommandLineModes(unittest.TestCase):
    def test_batch_mode_prints_results_and_saves_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            case_file = directory / "test_cases.txt"
            json_file = directory / "results.json"
            case_file.write_text(
                "# test cases\n"
                "name;Alan Turing;accepted\n"
                "email;T@teste.br;rejected\n",
                encoding="utf-8",
            )
            output = StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    ["batch", str(case_file), "--json", str(json_file)]
                )

            report = json.loads(json_file.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertIn("Batch finished: 2/2 passed", output.getvalue())
        self.assertEqual(report["mode"], "batch")
        self.assertEqual(report["summary"]["passed"], 2)
        self.assertEqual(report["summary"]["failed"], 0)
        self.assertEqual(report["results"][0]["field"], "name")

    def test_batch_mode_returns_failure_for_wrong_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            case_file = Path(temporary_directory) / "test_cases.txt"
            case_file.write_text(
                "email;T@teste.br;accepted\n",
                encoding="utf-8",
            )
            output = StringIO()

            with redirect_stdout(output):
                exit_code = main(["batch", str(case_file)])

        self.assertEqual(exit_code, 1)
        self.assertIn("FAIL", output.getvalue())

    def test_interactive_mode_switches_fields_and_saves_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            json_file = Path(temporary_directory) / "session.json"
            entries = [
                "cpf",
                "000.000.000-00",
                "phone",
                "(91) 99999-9999",
                "exit",
            ]
            output = StringIO()

            with patch("builtins.input", side_effect=entries):
                with redirect_stdout(output):
                    exit_code = main(
                        ["interactive", "--json", str(json_file)]
                    )

            report = json.loads(json_file.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertIn("Session finished: 2 value(s) checked", output.getvalue())
        self.assertEqual(report["mode"], "interactive")
        self.assertEqual(report["summary"]["accepted"], 2)
        self.assertEqual(
            [result["field"] for result in report["results"]],
            ["cpf", "phone"],
        )


if __name__ == "__main__":
    unittest.main()
