# my_vegetarian_recipe_agent.py
import pytest
import scenario
import litellm
from tests.my_agent_adapter import MyAgentAdapter
 
# Configure the default model for simulations
scenario.configure(default_model="openai/gpt-4.1-mini")
 
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_vegetarian_recipe_agent():
 
    # 2. Run the scenario
    result = await scenario.run(
        name="dinner recipe request",
        description="""
            It's saturday evening, the user is very hungry and tired,
            but have no money to order out, so they are looking for a recipe.
        """,
        agents=[
            MyAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(),
        ],
        script=[
            scenario.user("quick recipe for dinner"),
            scenario.agent(),
            scenario.judge(criteria=[
                "Agent either asks a relevant follow-up question or starts providing a recipe",
            ]),
            scenario.user(),
            scenario.agent(),
            scenario.judge(criteria=[
                "Agent should not ask more than two follow-up questions",
                "Agent should generate a recipe",
                "Recipe should include a list of ingredients",
                "Recipe should include step-by-step cooking instructions",
                "Recipe should be vegetarian and not include any sort of meat",
            ]),
        ],
    )
 
    # 3. Assert the result
    assert result.success
 
# Example agent implementation using litellm
@scenario.cache()
def vegetarian_recipe_agent(messages) -> scenario.AgentReturnTypes:
    response = litellm.completion(
        model="openai/gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a vegetarian recipe agent.
                    Given the user request, ask AT MOST ONE follow-up question,
                    then provide a complete recipe. Keep your responses concise and focused.
                """,
            },
            *messages,
        ],
    )
    return response.choices[0].message