# Standard imports
import ollama
from typing import Dict, Any, Callable
import json

# internal imports
from functions.my_mariadb import get_products_table, get_products_table_tool, get_products_count_tool, get_products_count

context = []
tools = [get_products_table_tool, get_products_count_tool]

def tool_call_to_dict(tool_call):
    """
    Convert a ToolCall object to a dictionary.
    """
    return {
        "function": {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments
        }
    }

def get_response(prompt: str, use_tools: bool = True) -> Any:
    global context
    global tools
    context.append({'role': 'user', 'content': prompt})

    available_functions: Dict[str, Callable] = {
        'get_products_table': get_products_table,
        'get_products_count': get_products_count,

    }

    response = ollama.chat(
        'llama3.2',
        messages=context,
        tools=tools if use_tools else None,
    )

    returner = {
        "message": {
            "content": response.message.content,
        },
        "function": []
    }

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            try:
                if function_to_call := available_functions.get(tool.function.name):
                    print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = function_to_call(**tool.function.arguments)
                    print('Function output:', output)
                    context.append({'role': 'tool', 'name': tool.function.name, 'content': str(output)})

                    returner["function"].append({
                        "name": tool.function.name,
                        "arguments": tool.function.arguments,
                        "output": output
                    })
                else:
                    print('Function', tool.function.name, 'not found')
            except Exception as e:
                print('Error calling function:', e)
                context.append({'role': 'tool', 'name': tool.function.name, 'content': str(e)})
    else:
        context.append({'role': 'assistant', 'content': response.message.content})

    returner["context"] = context

    return returner
