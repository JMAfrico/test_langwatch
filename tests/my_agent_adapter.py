import scenario
#from my_agent import MyCustomAgent

class MyAgentAdapter(scenario.AgentAdapter):
    #def __init__(self):
        #self.agent = MyCustomAgent()

    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        # Get the latest user message
        user_message = input.last_new_user_message_str()

        # Call your existing agent
        response = await self.agent.process(
            message=user_message,
            history=input.messages,
            thread_id=input.thread_id
        )

        # Return the response (can be string, message dict, or list of messages)
        return response