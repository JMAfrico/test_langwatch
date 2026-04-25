"""Implementações de adaptadores de agentes para testes de integração ADK.

Este módulo fornece três classes de adaptadores reutilizáveis:
- ADKAgent: Integra com o runner ADK do Google
- StubUser: Simula um usuário para testes
- InstantJudge: Avalia automaticamente os cenários
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import List

from scenario.agent_adapter import AgentAdapter
from scenario.types import AgentInput, AgentReturnTypes, AgentRole, ScenarioResult

# Add tests directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from config import APP_NAME, DEFAULT_GREETING, DEFAULT_REPLY, NO_REPLY_MESSAGE, PASSED_CRITERIA, SESSION_USER_ID


class ADKAgent(AgentAdapter):
    """Encaminha a mensagem do usuário através de um runner ADK compartilhado.

    O ``InMemoryRunner`` é construído fora do adaptador e passado
    para este - ``arun`` deve aguardar usando o mesmo loop em que foi criado.
    
    Atributos:
        _runner: Instância do runner ADK do Google.
        _session_prefix: Prefixo para identificar sessões do adaptador.
        _observed: Lista para rastrear o loop de execução.
        _session_idx: Índice da sessão atual.
    """

    def __init__(self, runner, session_prefix: str, observed: List[dict]):
        """Inicializa o adaptador ADK.
        
        Args:
            runner: Instância do InMemoryRunner do Google ADK.
            session_prefix: Prefixo para nomear as sessões.
            observed: Lista para rastrear informações de execução.
        """
        self._runner = runner
        self._session_prefix = session_prefix
        self._observed = observed
        self._session_idx = 0

    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """Processa a mensagem do usuário através do runner ADK.
        
        Extrai a última mensagem do usuário do histórico, cria uma sessão
        no runner ADK e processa a mensagem através do agente de clima.
        
        Args:
            input: Entrada contendo o histórico de mensagens da conversa.
            
        Returns:
            dict: Dicionário com 'role' e 'content' da resposta do agente.
        """
        from google.genai import types  # pyright: ignore[reportMissingImports]

        last_user = next(
            (m for m in reversed(input.messages) if m.get("role") == "user"),
            None,
        )
        raw = (last_user or {}).get("content") or DEFAULT_GREETING
        text = raw if isinstance(raw, str) else DEFAULT_GREETING

        session_id = f"{self._session_prefix}-{self._session_idx}"
        self._session_idx += 1
        await self._runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=SESSION_USER_ID,
            session_id=session_id,
        )

        reply = DEFAULT_REPLY
        # Drain the full event stream before returning — early-returning
        # leaves the async generator for the event loop to GC in a
        # different context, which tripped ADK's OTel context-detach
        # assertion on langwatch's experiment path.
        async for event in self._runner.run_async(
            user_id=SESSION_USER_ID,
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=text)]),
        ):
            if not event.is_final_response():
                continue
            content = getattr(event, "content", None)
            parts = getattr(content, "parts", None) or []
            txt = getattr(parts[0], "text", None) if parts else None
            if txt:
                reply = txt.strip()

        self._observed.append({"loop_id": id(asyncio.get_running_loop())})
        return {"role": "assistant", "content": reply}


class StubUser(AgentAdapter):
    """Agente simulador de usuário que retorna um prompt predefinido.
    
    Este adaptador simula um usuário real retornando uma mensagem
    pré-configurada, útil para testes automatizados.
    
    Atributos:
        role: O papel deste agente na conversa (USER).
        _prompt: A mensagem do usuário a ser retornada.
    """

    role = AgentRole.USER

    def __init__(self, prompt: str):
        """Inicializa o agente simulador de usuário.
        
        Args:
            prompt: A mensagem que o usuário simulado irá enviar.
        """
        self._prompt = prompt

    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """Retorna a mensagem pré-configurada do usuário simulado.
        
        Args:
            input: Entrada do cenário (não utilizada).
            
        Returns:
            str: A mensagem do prompt pré-configurado.
        """
        return self._prompt


class InstantJudge(AgentAdapter):
    """Agente juiz que marca todos os cenários como bem-sucedidos.
    
    Este adaptador simula um juiz que avalia automaticamente os
    cenários como sucesso, usado para testes de integração.
    
    Atributos:
        role: O papel deste agente na conversa (JUDGE).
    """

    role = AgentRole.JUDGE

    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """Avalia o cenário e retorna sucesso automaticamente.
        
        Args:
            input: Entrada do cenário (não utilizada).
            
        Returns:
            ScenarioResult: Resultado indicando sucesso do cenário.
        """
        return ScenarioResult(
            success=True,
            messages=[],
            reasoning=NO_REPLY_MESSAGE,
            passed_criteria=PASSED_CRITERIA,
        )
    """Instant judge agent that always marks scenarios as successful."""

    role = AgentRole.JUDGE

    async def call(self, input: AgentInput) -> AgentReturnTypes:
        return ScenarioResult(
            success=True,
            messages=[],
            reasoning=NO_REPLY_MESSAGE,
            passed_criteria=PASSED_CRITERIA,
        )
