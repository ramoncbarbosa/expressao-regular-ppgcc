# Validador de Expressões Regulares

Atividade sobre expressões regulares, para validar cadeias utilizando expressões regurales.

Os campos implementados são:

- Nome
- E-mail
- Senha
- CPF
- Telefone

## Regras

- **Nome:** nome e sobrenome separados por um espaço, com iniciais maiúsculas.
- **E-mail:** apenas letras minúsculas, exatamente um `@` e final `.br`.
- **Senha:** exatamente oito caracteres, com pelo menos uma letra maiúscula e um número.
- **CPF:** formato `xxx.xxx.xxx-xx`.
- **Telefone:** aceita os formatos `(xx) 9xxxx-xxxx`, `(xx) 9xxxxxxxx` e `xx 9xxxxxxxx`.

## Como Executar

Utilize Python 3.12 ou superior.

```bash
python main.py name "Alan Turing"
```

Outros exemplos:

```bash
python main.py email "divulga@ufpa.br"
python main.py password "ropsSoq0"
python main.py cpf "123.456.789-09"
python main.py phone "(91) 99999-9999"
```

O programa retorna:

```text
ACEITO
```

ou:

```text
REJEITADO
```

## Testes

Para executar todos os testes:

```bash
python -m unittest discover -s tests -v
```

O resultado esperado é:

```text
Ran 10 tests

OK
```