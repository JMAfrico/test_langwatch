"""Teste de integração: um runner ADK compartilhado funciona em invocações concorrentes.

Este teste valida que um runner ADK ``InMemoryRunner`` instanciado em uma
fixture pytest, que mantém um canal gRPC / serviço de sessão vinculado ao
loop de eventos do chamador, funciona corretamente quando múltiplos cenários
são executados concorrentemente com ``scenario.arun``.

A razão é que com ``scenario.arun`` o adaptador é executado no loop do
chamador, mantendo o runner singleton reutilizável em todos os cenários.

Requer ``GOOGLE_API_KEY`` e ``google-adk``. Ignorado caso contrário.
"""

from __future__ import annotations

import asyncio
import sys
import uuid
from pathlib import Path
from typing import List

import pytest

import scenario
from scenario.types import ScenarioResult

# Add tests directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from agents import ADKAgent, StubUser, InstantJudge
from config import TEST_CITIES


@pytest.mark.asyncio
async def test_shared_adk_runner_survives_concurrent_arun(shared_runner):
    """Testa que chamadas concorrentes de scenario.arun funcionam com um runner ADK compartilhado.
    
    Este teste valida que:
    1. Todos os cenários concorrentes podem reutilizar o mesmo runner ADK
    2. Não ocorrem erros de afinidade de event loop
    3. Todas as invocações de adaptador executam no mesmo event loop
    
    Args:
        shared_runner: Fixture de pytest que fornece o runner ADK compartilhado.
    """
    observed: List[dict] = []
    cities = TEST_CITIES
    suffix = uuid.uuid4().hex[:6]

    async def one(city: str, idx: int) -> ScenarioResult:
        """Executa um único cenário para uma cidade.
        
        Cria e executa um cenário simples onde o usuário pergunta
        sobre o clima em uma cidade específica.
        
        Args:
            city: A cidade para obter o clima.
            idx: O índice do cenário.
            
        Returns:
            ScenarioResult: O resultado de executar o cenário.
        """
        return await scenario.arun(
            name=f"adk-weather-{city.lower()}",
            description=f"User asks about {city} weather",
            agents=[
                ADKAgent(shared_runner, f"arun-{suffix}-{idx}", observed),
                StubUser(f"What is the weather in {city}?"),
                InstantJudge(),
            ],
            script=[
                scenario.user(f"What is the weather in {city}?"),
                scenario.agent(),
                scenario.judge(),
            ],
        )

    results = await asyncio.gather(
        *(one(city, i) for i, city in enumerate(cities)),
        return_exceptions=True,
    )

    # Any loop-affinity breakage would surface as one of these turning
    # into a RuntimeError with "different loop" in its repr.
    for idx, result in enumerate(results):
        assert not isinstance(result, Exception), (
            f"scenario {idx} raised: {result!r}\n"
            "This likely means the ADK runner was awaited on a loop "
            "it was not created on (i.e. arun regressed to scenario.run's "
            "threaded behaviour)."
        )

    assert all(isinstance(r, ScenarioResult) and r.success for r in results)

    # All adapter invocations must have run on a single event loop — the
    # one this test function itself is running on.
    loop_ids = {o["loop_id"] for o in observed}
    assert loop_ids == {id(asyncio.get_running_loop())}