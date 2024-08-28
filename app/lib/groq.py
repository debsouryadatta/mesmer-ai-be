import os
import dotenv
import json
from groq import Groq
import asyncio
dotenv.load_dotenv()

os.environ.get('GROQ_API_KEY')
client = Groq()
MODEL = "llama3-groq-70b-8192-tool-use-preview"
# MODEL = "llama3-groq-8b-8192-tool-use-preview"
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate",
                    }
                },
                "required": ["expression"],
            },
        },
    }
]



def calculate(expression):
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})
    


async def get_response_from_groq(user_input, chat_history):
    if len(chat_history) == 0:
        chat_history = [{"role": "system", "content": "You are a helpful AI assistant capable of performing calculations."}]
    
    chat_history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        temperature=0.5,
        model=MODEL,
        messages=chat_history,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096,
        stream=True
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "calculate": calculate,
        }
        chat_history.append(response_message)
        for tool_call in tool_calls:
            print(tool_call)
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                expression=function_args.get("expression")
            )
            chat_history.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=chat_history,
            stream=True
        )
        # print(second_response.choices[0].message.content)
        for chunk in second_response:
            # print(chunk.choices[0].delta.content, end="")
            print("tools")
            yield chunk.choices[0].delta.content
            await asyncio.sleep(0)
    else:
        for chunk in response:
            print("no tools")
            # print(chunk.choices[0].delta.content, end="")
            yield chunk.choices[0].delta.content
            await asyncio.sleep(0)







async def get_response_from_groq(user_input, chat_history):
    if len(chat_history) == 0:
        chat_history = [{"role": "system", "content": "You are a helpful ai assistant."}]
        
    chat_history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        temperature=0.5,
        # model="llama-3.1-70b-versatile",
        # model="llama3-groq-70b-8192-tool-use-preview",
        model="llama3-8b-8192",
        messages=chat_history,
        stream=True
    )
    for chunk in response:
        # print(chunk.choices[0].delta.content, end="")
        yield chunk.choices[0].delta.content
        await asyncio.sleep(0)
    # return "Done"