"""Configuração e constantes para testes de integração ADK.

Este módulo centraliza todas as constantes, variáveis de ambiente e
valores padrão usados nos testes de integração com Google ADK.

Atributos:
    SCENARIO_HEADLESS: Define se os cenários rodam em modo headless.
    GOOGLE_API_KEY: Chave da API do Google para autenticação.
    GEMINI_MODEL: Nome do modelo Gemini a usar.
    APP_NAME: Nome da aplicação para o runner ADK.
    WEATHER_AGENT_NAME: Nome do agente de clima.
    TEST_CITIES: Lista de cidades para testes.
    DEFAULT_GREETING: Saudação padrão do sistema.
    DEFAULT_REPLY: Resposta padrão quando não há resposta.
    NO_REPLY_MESSAGE: Mensagem de raciocínio para falta de resposta.
    PASSED_CRITERIA: Critérios passados na avaliação.
    SESSION_USER_ID: ID do usuário padrão para sessões.
"""

import os

# Environment setup
SCENARIO_HEADLESS = os.environ.get("SCENARIO_HEADLESS", "true")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")

# Application settings
APP_NAME = os.environ.get("APP_NAME", "scenario-arun-adk-integration")
WEATHER_AGENT_NAME = os.environ.get("WEATHER_AGENT_NAME", "weather_agent")

# Test data
TEST_CITIES = ["Amsterdam", "Berlin", "Cairo", "Delhi"]
DEFAULT_GREETING = "Hello"
DEFAULT_REPLY = "(no reply)"
NO_REPLY_MESSAGE = "adk reply received"
PASSED_CRITERIA = ["adk responded"]

# Session configuration
SESSION_USER_ID = "user"
