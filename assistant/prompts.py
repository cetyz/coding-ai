def github_cleaner_agent_system_prompt():
    prompt = {
        'role': 'system',
        'content': '''You are an expert at reading code and also developing programs. You will be given some data from a github repo. 
    Primary Objectives: 
    1. Convert any notebook code or other markdown (e.g. .ipynb) into more readable python
    For example: ```{\n   "cell_type": "code",\n   "execution_count": 10,\n   "metadata": {},\n   "outputs": [],\n   "source": [\n    "from dotenv import load_dotenv\\n",\n    "from openai import OpenAI\\n",\n    "from tenacity import retry, wait_random_exponential, stop_after_attempt"\n   ]\n  }```
    Should become: ``` from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt```
    3. Then, give me output in the following format:
    
    
     ## Folder Structure
     (insert folder structure here)

     ## File contents
     file1.py
     ```file1.py contents```

     file2.ipynb
     ```file2.ipynb contents```
    
'''
    }
    return prompt

def github_assistant_agent_system_prompt(github_data):
    prompt = {
        'role': 'system',
        'content': f'''You are an expert at reading code and also developing programs. You will be given the structure of a github repo and also the content of the files.

START OF github data: {github_data}
END github data

Primary Objectives: 
1. Understand the repository and answer any questions the user may have
2. Think step by step how to answer this question
3. Give the final answer

Use the following framework for thinking and answering:

Summary of user question: [summary]
First thoughts and reactions: [possible solutions]
Criticism of first thoughts and reactions: [criticize pros and cons of each thought]
Final answer: [choose solution, followed by reasoning]
Implementation of code: [```insert code or changes```]
Explanation of implementation: [explain written/edited code]
'''
    }

    return prompt


if __name__ == '__main__':
    print(github_cleaner_agent_system_prompt())