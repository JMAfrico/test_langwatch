"""Adaptador para agente que gera receitas vegetarianas.

Este módulo fornece um adaptador que integra um agente specializado
em gerar receitas vegetarianas com o framework scenario.
"""

import litellm
import scenario


class VegetarianRecipeAdapter(scenario.AgentAdapter):
    """Adaptador para o agente de receitas vegetarianas.
    
    Este adaptador integra um agente LLM especializado em receitas
    vegetarianas com o framework scenario.
    
    Atributos:
        model: Modelo da IA a ser utilizado para gerar respostas.
    """
    
    def __init__(self, model: str = "openai/gpt-4.1-mini"):
        """Inicializa o adaptador do agente vegetariano.
        
        Args:
            model: Modelo LLM a utilizar. Padrão: openai/gpt-4.1-mini
        """
        self.model = model

    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        """Processa a mensagem do usuário e gera uma receita vegetariana.
        
        Extrai a última mensagem do usuário e faz uma chamada à API do LLM
        para gerar uma resposta no contexto de receitas vegetarianas.
        O agente é instruído a fazer no máximo uma pergunta de
        acompanhamento antes de fornecer uma receita completa.
        
        Args:
            input: Entrada contendo o histórico de mensagens da conversa.
            
        Returns:
            Dict: Resposta do modelo em formato de mensagem.
        """
        # Obter a mensagem de usuário mais recente
        user_message = input.last_new_user_message_str()

        # Chamar o agente LLM para gerar a receita
        response = self._generate_recipe(input.messages)

        # Retornar a resposta
        return response

    def _generate_recipe(self, messages: list) -> dict:
        """Gera uma receita vegetariana usando LLM.
        
        Processa mensagens do usuário e faz uma chamada à API do LLM
        para gerar respostas no contexto de receitas vegetarianas.
        O agente faz no máximo uma pergunta de acompanhamento e depois
        fornece uma receita completa.
        
        Args:
            messages: Lista de mensagens do histórico da conversa.
            
        Returns:
            Dict: Resposta do modelo LLM em formato de mensagem.
        """
        response = litellm.completion(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """
                        Você é um agente especializado em receitas vegetarianas.
                        Dado o pedido do usuário, faça NO MÁXIMO UMA pergunta de acompanhamento
                        para esclarecer preferências, e então forneça uma receita completa.
                        Mantenha suas respostas concisas e focadas.
                        
                        A receita deve incluir:
                        - Lista de ingredientes com quantidades
                        - Modo de preparo passo a passo
                        - Tempo de preparo estimado
                        - Dificuldade (fácil, médio, difícil)
                    """,
                },
                *messages,
            ],
        )
        return response.choices[0].message
