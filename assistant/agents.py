from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

from prompts import *

load_dotenv()

GPT_MODEL = 'gpt-3.5-turbo'

client = OpenAI()

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        if tools:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response
    except Exception as e:
        print('Unable to generate ChatCompletion response')
        print(f'Exception: {e}')
        return e
    

class Agent:
    def __init__(self, model=GPT_MODEL, system_prompt=None, tools=None):
        self.model = model
        self.memory = []
        if system_prompt:
            self.append_to_memory(system_prompt)
        if tools:
            self.tools = tools
        else:
            self.tools = []

    def append_to_memory(self, memory_content: Dict) -> None:
        """Takes in a Dict that will be appended to memory.
        Memory will be updated.

        Args:
            memory_content (Dict): {'role': {role}, 'content', {content}}

        Returns:
            None
        """

        if 'role' not in memory_content.keys():
            raise Exception('\'role\' key not found in memory to be added')
        
        if 'content' not in memory_content.keys():
            raise Exception('\'content\' key not found in memory to be added')

        self.memory.append(memory_content)

    def invoke(self, message):

        self.append_to_memory({'role': 'user', 'content': message})

        if len(self.tools):

            chat_response = chat_completion_request(
                messages=self.memory,
                tools=self.tools,
                model=self.model,
            )
        
        else:

            chat_response = chat_completion_request(
                messages=self.memory,
                model=self.model,
            )

        if chat_response.choices[0].finish_reason == 'stop':
            chat_response_message = chat_response.choices[0].message.content
            self.append_to_memory({'role': 'assistant', 'content': chat_response_message})
            return chat_response_message

        elif chat_response.choices[0].finish_reason == 'tool_calls':
            # tool_calls = chat_response.choices[0].message.tool_calls
            # for tool_call in tool_calls:
            pass


class GithubCleanerAgent(Agent):
    def __init__(self, model=GPT_MODEL):
        super().__init__(model=model, system_prompt=github_cleaner_agent_system_prompt())

class GithubAssistantAgent(Agent):
    def __init__(self, model=GPT_MODEL, github_data=None):
        if not github_data:
            raise Exception('Please ensure to provide data to the Github Assistant at initialization')
        super().__init__(model=model, system_prompt=github_assistant_agent_system_prompt(github_data))

if __name__ == '__main__':
    from tools import fetch_github_repo
    repo_data = fetch_github_repo('https://github.com/cetyz/coding-ai')

    github_cleaner_agent = GithubCleanerAgent()
    github_data = github_cleaner_agent.invoke(repo_data)
    
    print(github_data)

    # github_assistant_agent = GithubAssistantAgent(github_data=github_data)


    # while True:
    #     user_input = input('User Message: ')
    #     if user_input == 'exit':
    #         break
    #     response = github_assistant_agent.invoke(user_input)
    #     print('Assistant:', response)
    #     print()