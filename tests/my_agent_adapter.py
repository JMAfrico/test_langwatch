import scenario
#from my_agent import MyCustomAgent

class MyAgentAdapter(scenario.AgentAdapter):
    """Adaptador de agente customizado - template para integração de agentes próprios.
    
    Este é um template que mostra como criar um adaptador para
    integrar seu próprio agente com o framework de cenários.
    Descomente e implemente os métodos conforme necessário.
    
    Atributos:
        agent: Instância do agente customizado (a ser implementado).
    """
    
    #def __init__(self):
    #    """Inicializa o adaptador com o agente customizado.
    #    
    #    Descomente este método quando tiver um agente pronto.
    #    """
    #    self.agent = MyCustomAgent()

    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        """Processa a mensagem do usuário através do agente customizado.
        
        Extrai a última mensagem do usuário, processa através do agente
        e retorna a resposta.
        
        Args:
            input: Entrada contendo o histórico de mensagens da conversa.
            
        Returns:
            str | dict | list: A resposta do agente (string, dicionário
                                de mensagem ou lista de mensagens).
        """
        # Obter a mensagem de usuário mais recente
        user_message = input.last_new_user_message_str()

        # Chamar o agente existente
        response = await self.agent.process(
            message=user_message,
            history=input.messages,
            thread_id=input.thread_id
        )

        # Retornar a resposta (pode ser string, dict ou lista de mensagens)
        return response