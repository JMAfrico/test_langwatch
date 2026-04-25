"""Teste exemplo usando Google Gemini API para conversas.

Este módulo demonstra como usar o GoogleGeminiAdapter para conversar
com o modelo Gemini do Google através do framework scenario.
"""

import pytest
import scenario
from google_gemini_adapter import GoogleGeminiAdapter


@pytest.mark.asyncio
async def test_google_gemini_simple_conversation():
    """Testa uma conversa simples com Google Gemini.
    
    Valida que o agente consegue:
    - Conectar com a API do Google Gemini
    - Processar mensagens de usuário
    - Gerar respostas coerentes
    """
    
    result = await scenario.run(
        name="Google Gemini Conversation",
        description="Testa uma conversa simplificada com o Gemini",
        agents=[
            GoogleGeminiAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should respond to user messages",
                "Response should be coherent and relevant",
                "Response should be non-empty",
            ]),
        ],
        script=[
            scenario.user("O que é Python?"),
            scenario.agent(),
            scenario.proceed(),
        ],
    )
    
    assert result.success


@pytest.mark.asyncio
async def test_google_gemini_with_custom_prompt():
    """Testa Gemini com um prompt customizado.
    
    Valida que o agente respeita instrções do sistema personalizadas.
    """
    
    custom_prompt = """Você é um especialista em programação Python.
Responda perguntas sobre Python de forma didática e com exemplos de código quando apropriado."""
    
    result = await scenario.run(
        name="Python Expert",
        description="Testa Gemini como expert em Python",
        agents=[
            GoogleGeminiAdapter(system_prompt=custom_prompt),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Response should be about Python",
                "Response should be helpful and educational",
                "Response should use appropriate examples",
            ]),
        ],
        script=[
            scenario.user("Como criar uma lista em Python?"),
            scenario.agent(),
            scenario.proceed(),
        ],
    )
    
    assert result.success


@pytest.mark.asyncio
async def test_google_gemini_multi_turn_conversation():
    """Testa uma conversa multi-turno com Gemini.
    
    Valida que o agente mantém histórico e contexto entre mensagens.
    """
    
    result = await scenario.arun(
        name="Multi-turn Conversation",
        description="Testa múltiplas trocas de mensagens com Gemini",
        agents=[
            GoogleGeminiAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should maintain conversation context",
                "Agent should respond to follow-up questions",
                "Responses should be coherent with the conversation history",
            ]),
        ],
        script=[
            scenario.user("Qual é a capital da França?"),
            scenario.agent(),
            scenario.user("Quantos habitantes tem?"),
            scenario.agent(),
            scenario.proceed(),
        ],
    )
    
    assert result.success
