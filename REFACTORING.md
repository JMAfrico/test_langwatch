# Refatoração do Teste ADK

## Resumo das Mudanças

A refatoração foi feita para separar responsabilidades, melhorar a manutenibilidade e mover configurações para variáveis de ambiente.

### Estrutura de Arquivos

```
tests/
├── conftest.py              # Fixtures e configuração de pytest
├── config.py                # Configurações e constantes
├── check_dependencies.py    # Verificação de dependências
├── agents.py                # Classes de agentes/adapters
└── test_adk.py             # Testes apenas
```

### Mudanças Realizadas

#### 1. **Novo arquivo: `config.py`**
   - Centraliza todas as configurações e constantes
   - Lê variáveis do `.env`
   - Define valores padrão
   - Facilita manutenção e testes

#### 2. **Novo arquivo: `check_dependencies.py`**
   - Remove lógica de verificação de dependências do arquivo de teste
   - Função `has_adk()`: verifica se google-adk está instalado
   - Função `build_weather_runner()`: constrói o runner (antes era `_build_runner`)

#### 3. **Novo arquivo: `agents.py`**
   - Contém todas as classes de agentes reutilizáveis
   - Classes públicas (sem prefixo `_`):
     - `ADKAgent`: (era `_ADKAgent`)
     - `StubUser`: (era `_StubUser`)
     - `InstantJudge`: (era `_InstantJudge`)
   - Cada classe tem documentação clara

#### 4. **Novo arquivo: `conftest.py`**
   - Configuração centralizada do pytest
   - Define `pytestmark` para marcas de teste
   - Fixture `shared_runner()`: cria runner compartilhado
   - Verifica requisitos de variáveis de ambiente

#### 5. **Atualizado: `test_adk.py`**
   - Agora APENAS contém o teste
   - Importa agentes, configuração e fixtures
   - Código mais limpo e focado
   - Docstrings melhoradas

#### 6. **Atualizado: `.env`**
   - Adicionadas novas variáveis:
     - `GOOGLE_API_KEY`
     - `GEMINI_MODEL`
     - `SCENARIO_HEADLESS`
     - `APP_NAME`
     - `WEATHER_AGENT_NAME`

### Benefícios

✅ **Separação de Responsabilidades**
- Fixtures em `conftest.py`
- Configurações em `config.py`
- Agentes em `agents.py`
- Verificação de deps em `check_dependencies.py`
- Testes em `test_adk.py`

✅ **Reutilização**
- Classes de agentes podem ser usadas em outros testes
- Fixtures são descobertas automaticamente pelo pytest

✅ **Manutenibilidade**
- Fácil encontrar e alterar configurações
- Cada arquivo tem responsabilidade clara

✅ **Testabilidade**
- Melhor isolamento de componentes
- Mais fácil mockar dependências

### Como Usar

1. Configure o `.env` com suas variáveis
2. Execute os testes normalmente:
   ```bash
   pytest tests/test_adk.py
   ```

3. Para executar com mais verbosidade:
   ```bash
   pytest tests/test_adk.py -v
   ```
