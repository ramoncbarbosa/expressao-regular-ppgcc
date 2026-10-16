# Regular Expression Validator

Validador de nome, e-mail, senha, CPF e telefone usando expressões regulares.
Requer Python 3.12 ou superior e não usa dependências externas.

## Validar um valor

```bash
python3 main.py name "Alan Turing"
python3 main.py email "divulga@ufpa.br"
python3 main.py password "ropsSoq0"
python3 main.py cpf "123.456.789-09"
python3 main.py phone "(91) 99999-9999"
```

O terminal mostra `ACCEPTED` ou `REJECTED`.
Para salvar o resultado em um JSON:

```bash
python3 main.py cpf "123.456.789-09" --json result.json
```

## Testar vários casos

O arquivo `examples/test_cases.txt` contém 100 casos de teste para os cinco
campos, cada linha usa o formato `field;value;expected`.
Linhas iniciadas com `#` e linhas vazias são ignoradas, o resultado esperado pode ser `accepted` ou `rejected`.

```bash
python3 main.py batch examples/test_cases.txt --json results.json
```

O terminal mostra o resultado de cada linha e o resumo dos testes, o JSON
registra o campo, o valor, o resultado esperado e o resultado obtido.

Para adicionar casos, inclua linhas no arquivo, por exemplos:

```text
name;Alan Turing;accepted
email;T@teste.br;rejected
cpf;123.456.789-09;accepted
```

## Validar valores interativamente

```bash
python3 main.py interactive --json session_results.json
```

Digite o nome do campo para selecioná-lo, depois, digite os valores a serem validados.
Digite outro nome de campo para trocar a seleção e use `exit` para finalizar e
salvar os resultados no arquivo JSON.

```text
> cpf
cpf> 123.456.789-09
ACCEPTED
cpf> phone
phone> (91) 99999-9999
ACCEPTED
phone> exit
```

Campos disponíveis: `name`, `email`, `password`, `cpf` e `phone`.

## Executar os testes automatizados

```bash
python3 -m unittest discover -s tests -v
```
