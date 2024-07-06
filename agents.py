from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

load_dotenv()

GPT_MODEL = 'gpt-3.5-turbo'

client = OpenAI()

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print('Unable to generate ChatCompletion response')
        print(f'Exception: {e}')
        return e
    

class Agent:
    def __init__(self, model=GPT_MODEL):
        self.model = model
        self.memory = []
        self.tools = []
        
    def invoke(self, message):
        self.memory.append(
            {'role': 'user', 'content': message}
        )
        chat_response = chat_completion_request(
            messages=self.memory,
            tools=self.tools,
            model=self.model,
        )

        if chat_response.choices[0].finish_reason == 'stop':
            chat_response_message = chat_response.choices[0].message.content
            self.memory.append(
                {'role': 'assistant', 'content': chat_response_message}
            )
            return chat_response_message

        elif chat_response.choices[0].finish_reason == 'tool_calls':
            # tool_calls = chat_response.choices[0].message.tool_calls
            # for tool_call in tool_calls:
            pass