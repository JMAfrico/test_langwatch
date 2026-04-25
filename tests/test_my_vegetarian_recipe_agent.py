# my_vegetarian_recipe_agent.py
"""Testes para um agente que gera receitas vegetarianas.

Este módulo contém um teste que simula um agente capaz de recomendar
receitas vegetarianas de acordo com as preferências do usuário.
Usa um adaptador customizado para integração com o framework scenario.
"""

import pytest
import scenario
from vegetarian_recipe_adapter import VegetarianRecipeAdapter
 
# Configure the default model for simulations
scenario.configure(default_model="openai/gpt-4.1-mini")
 
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_vegetarian_recipe_agent():
    """Testa um agente que gera receitas vegetarianas.
    
    Simula um cenário onde um usuário cansado e com fome pede uma
    receita rápida para jantar. Valida que o agente:
    - Faz perguntas relevantes sobre preferências do usuário
    - Fornece uma receita completa com ingredientes e modo de preparo
    - Garante que a receita é vegetariana (sem carnes)
    """
 
    # 2. Run the scenario
    result = await scenario.run(
        name="dinner recipe request",
        description="""
            It's saturday evening, the user is very hungry and tired,
            but have no money to order out, so they are looking for a recipe.
        """,
        agents=[
            VegetarianRecipeAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should ask relevant follow-up questions to clarify the user's preferences and constraints (e.g., dietary restrictions, available ingredients, time constraints).",
                "Agent should provide a complete recipe that includes a list of ingredients and step-by-step cooking instructions.",
                "Recipe should be vegetarian and not include any sort of meat.",
            ]),
        ],
        script=[
            scenario.user("quick recipe for dinner"),
            scenario.agent(),
            scenario.proceed(),
        ],
    )
 
    # 3. Assert the result
    assert result.success