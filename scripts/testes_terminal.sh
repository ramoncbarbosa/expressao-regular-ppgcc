#!/usr/bin/env bash

cd "$(dirname "$0")/.." || exit 1

echo "=== Testes automatizados ==="
python3 -m unittest discover -s tests -v

echo
echo "=== Lote com 100 casos ==="
python3 main.py batch examples/test_cases.txt --json results.json
