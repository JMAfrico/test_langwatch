"""Utilitários para verificação de dependências do ADK.

Este módulo fornece funções para verificar se o google-adk está
instalado e construir instâncias configuradas do runner ADK.
"""

import sys
from pathlib import Path

# Add tests directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))


def has_adk() -> bool:
    """Verifica se o google-adk está instalado e disponível.
    
    Tenta importar os componentes principais do google-adk para
    verificar se a biblioteca está corretamente instalada.
    
    Returns:
        bool: True se google-adk está disponível, False caso contrário.
    """
    try:
        import google.adk  # noqa: F401  # pyright: ignore[reportMissingImports]
        from google.adk.agents import Agent  # noqa: F401  # pyright: ignore[reportMissingImports]
        from google.adk.runners import InMemoryRunner  # noqa: F401  # pyright: ignore[reportMissingImports]
    except Exception:
        return False
    return True


def build_weather_runner():
    """Constrói e retorna um InMemoryRunner com um agente de clima.
    
    Cria um agente ADK configurado para responder perguntas sobre
    tempo e o envolve em um InMemoryRunner.
    
    Returns:
        InMemoryRunner: Runner configurado com o agente de clima.
        
    Raises:
        Exception: Se o ADK não estiver corretamente configurado
                   ou as dependências estiverem ausentes.
    """
    from google.adk.agents import Agent  # pyright: ignore[reportMissingImports]
    from google.adk.runners import InMemoryRunner  # pyright: ignore[reportMissingImports]
    
    from config import APP_NAME, GEMINI_MODEL, WEATHER_AGENT_NAME

    def get_weather(city: str) -> dict:
        """Obtém um relatório de tempo para uma cidade.
        
        Args:
            city: Nome da cidade para obter o relatório.
            
        Returns:
            dict: Dicionário com status e relatório de tempo.
        """
        return {"status": "ok", "report": f"Sunny in {city}"}

    agent = Agent(
        name=WEATHER_AGENT_NAME,
        model=GEMINI_MODEL,
        description="Replies with a short weather report.",
        instruction="Call get_weather for the city the user asks about and answer briefly.",
        tools=[get_weather],
    )
    return InMemoryRunner(agent=agent, app_name=APP_NAME)
