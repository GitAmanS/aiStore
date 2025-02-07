# Standard imports
import ollama
from typing import Dict, Any, Callable
import json

# internal imports
from functions.my_mariadb import get_all_products, get_product_by_id, search_products, get_products_by_category, add_product, update_product, delete_product, get_all_categories
from functions.my_mariadb import get_all_products_tool, get_product_by_id_tool, search_products_tool, get_products_by_category_tool, add_product_tool, update_product_tool, delete_product_tool, get_all_categories_tool
context = []
tools = [get_all_products_tool, get_product_by_id_tool, search_products_tool, get_products_by_category_tool, add_product_tool, update_product_tool, delete_product_tool, get_all_categories_tool]

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
        'get_all_products': get_all_products,
        'get_product_by_id': get_product_by_id,
        'search_products': search_products,
        'get_products_by_category': get_products_by_category,
        'add_product': add_product,
        'update_product': update_product,
        'delete_product': delete_product,
        'get_all_categories': get_all_categories
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

    update_context()
    # returner["context"] = context

    return returner

def update_context():
    global context
    with open('context.json', 'w') as f:
        json.dump(context, f, indent=4)

def set_context(new_context):
    global context
    context = new_context