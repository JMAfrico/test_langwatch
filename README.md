CONFIGURAÇÕES DO PYTHON
gerenciador de pacotes padrão - pip testes unitarios - pytest

Criar ambiente virtual
criar : python -m venv .venv ativar: ..venv\Scripts\activate.bat

Criar o requirements.
pip freeze para listar os modulos, copiar e colar no requirements ou pip freeze > requirements.txt , ja pega os módulos e coloca no arquivo

Istalação do langwatch
https://langwatch.ai/scenario/basics/concepts https://langwatch.ai/scenario/reference/python/scenario/index.html

PARA INSTALAR COM O PIP, É NECESSÁRIO CONFIGURAR MANUALMENTE O .ENV pip install langwatch-scenario pytest

PARA INSTALAR COM O UV , ja adiciona o .env e ativa automaticamente uv add langwatch-scenario pytest

primeiro cenario langwatch
https://langwatch.ai/scenario/introduction/getting-started

Criar a pasta tests, colocar o arquivo lá criar um arquivo de agentAdapter para usar , tem que escolher um modelo de interface de agente
