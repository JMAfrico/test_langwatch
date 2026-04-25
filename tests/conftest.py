"""Configuração de pytest e fixtures para testes de integração ADK.

Este módulo define a configuração centralizada do pytest, verificações
de dependências (pytestmark) e fixtures compartilhadas para testes ADK.
"""

import os
import sys
from pathlib import Path

import pytest

# Add tests directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

os.environ.setdefault("SCENARIO_HEADLESS", "true")

from check_dependencies import has_adk, build_weather_runner

pytestmark = [
    pytest.mark.skipif(not has_adk(), reason="google-adk not installed"),
    pytest.mark.skipif(
        not os.environ.get("GOOGLE_API_KEY"), reason="GOOGLE_API_KEY not set"
    ),
]


@pytest.fixture(scope="module")
def shared_runner():
    """Cria um runner ADK compartilhado para o módulo de testes.
    
    É criado uma única vez por módulo no loop de eventos que
    pytest-asyncio está usando — este é o loop que todos os
    cenários concorrentes devem reutilizar.
    
    Yields:
        InMemoryRunner: Uma instância do runner ADK configurado.
        
    Raises:
        pytest.skip: Se o runner não puder ser construído devido
                     a problemas de ambiente.
    """
    try:
        yield build_weather_runner()
    except Exception as exc:  # pragma: no cover - env-dependent
        pytest.skip(f"Failed to build ADK runner: {exc}")
