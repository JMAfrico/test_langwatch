"""Adaptador para agente que usa Google Gemini API.

Este módulo fornece um adaptador que integra o modelo Gemini do Google
com o framework scenario para conversas e processamento de texto.
"""

import os

import google.generativeai as genai
import scenario


class GoogleGeminiAdapter(scenario.AgentAdapter):
    """Adaptador para agente que usa a API Google Gemini.
    
    Este adaptador integra o modelo Gemini do Google com o framework
    scenario, permitindo conversas e processamento de texto.
    
    Atributos:
        model: Modelo Gemini a ser utilizado.
        chat: Sessão de conversa com o modelo.
        api_key: Chave da API do Google.
    """
    
    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        system_prompt: str = None
    ):
        """Inicializa o adaptador do Google Gemini.
        
        Args:
            model: Modelo Gemini a usar. Se None, lê de GEMINI_MODEL do .env
            api_key: Chave da API do Google. Se None, lê de GOOGLE_API_KEY do .env
            system_prompt: Instrução do sistema para o modelo.
                           Se None, usa prompt genérico.
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model_name = model or os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
        
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY não configurada. "
                "Configure no .env ou passe como argumento."
            )
        
        # Configurar a API do Google
        genai.configure(api_key=self.api_key)
        
        # Criar modelo Gemini
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_prompt or self._get_default_prompt()
        )
        
        # Iniciar conversa
        self.chat = self.model.start_chat()

    def _get_default_prompt(self) -> str:
        """Retorna o prompt padrão do sistema.
        
        Returns:
            str: Instruções padrão para o modelo.
        """
        return """Você é um assistente inteligente e prestativo.
Responda às perguntas do usuário de forma clara, concisa e útil.
Se não souber a resposta, seja honesto sobre isso."""

    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        """Processa a mensagem do usuário com Google Gemini.
        
        Extrai a última mensagem do usuário, envia para o Gemini
        e retorna a resposta gerada.
        
        Args:
            input: Entrada contendo o histórico de mensagens da conversa.
            
        Returns:
            Dict: Resposta do modelo em formato de mensagem.
        """
        # Obter a mensagem de usuário mais recente
        user_message = input.last_new_user_message_str()

        # Enviar para o Gemini e obter resposta
        response = self.chat.send_message(user_message)
        
        # Retornar a resposta
        return {
            "role": "assistant",
            "content": response.text
        }

    def reset_conversation(self):
        """Reseta o histórico de conversa.
        
        Útil para iniciar um novo tópico ou teste.
        """
        self.chat = self.model.start_chat()
