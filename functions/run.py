# Standard imports
import ollama
from typing import Dict, Any, Callable

# internal imports 
from functions.Context import Context, Context_Handler, Context_Chain

# internal imports
from functions.my_mariadb import get_all_products, get_product_by_id, search_products, get_products_by_category, add_product, update_product, delete_product, get_all_categories
from functions.my_mariadb import get_all_products_tool, get_product_by_id_tool, search_products_tool, get_products_by_category_tool, add_product_tool, update_product_tool, delete_product_tool, get_all_categories_tool

class LLM:
    def __init__(self):
        self.tools = [
            get_all_products_tool, get_product_by_id_tool, search_products_tool, 
            get_products_by_category_tool, add_product_tool, update_product_tool, 
            delete_product_tool, get_all_categories_tool
        ]

    def tool_call_to_dict(self, tool_call):
        """
        Convert a ToolCall object to a dictionary.
        """
        return {
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }
        }

    def get_response(self, prompt: str, use_tools: bool = True, user_id: int = 1) -> Any:
        context_handler = self.initialize_context_handler(user_id, prompt)
        response = self.get_chat_response(context_handler, use_tools)
        return self.process_response(response, context_handler)

    def initialize_context_handler(self, user_id: int, prompt: str) -> Context_Handler:
        context_handler = Context_Handler(user_id)
        context_handler.tool_context_chain.append(
            Context(
                Context.USER_STRING, 
                Context.USER_STRING, 
                prompt
            )
        )
        return context_handler

    def get_chat_response(self, context_handler: Context_Handler, use_tools: bool) -> Any:
        return ollama.chat(
            'llama3.2',
            messages=Context_Chain(context_handler.get_context(Context_Handler.TOOL_STRING)),
            tools=self.tools if use_tools else None,
        )

    def process_response(self, response: Any, context_handler: Context_Handler) -> Dict[str, Any]:
        available_functions = self.get_available_functions()
        returner = {
            "message": {
                "content": response.message.content,
            },
            "function": []
        }

        if response.message.tool_calls:
            self.handle_tool_calls(response, context_handler, available_functions, returner)
        else:
            context_handler.tool_context_chain.append(
                Context(Context.ASSISTANT_STRING, Context.ASSISTANT_STRING, response.message.content)
            )

        context_handler.update_context()
        return returner

    def get_available_functions(self) -> Dict[str, Callable]:
        return {
            'get_all_products': get_all_products,
            'get_product_by_id': get_product_by_id,
            'search_products': search_products,
            'get_products_by_category': get_products_by_category,
            'add_product': add_product,
            'update_product': update_product,
            'delete_product': delete_product,
            'get_all_categories': get_all_categories
        }

    def handle_tool_calls(self, response: Any, context_handler: Context_Handler, available_functions: Dict[str, Callable], returner: Dict[str, Any]) -> None:
        for tool in response.message.tool_calls:
            try:
                if function_to_call := available_functions.get(tool.function.name):
                    print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = function_to_call(**tool.function.arguments)
                    print('Function output:', output)
                    context_handler.tool_context_chain.append(
                        Context(tool.function.name, Context.TOOL_STRING, str(output))
                    )

                    returner["function"].append({
                        "name": tool.function.name,
                        "arguments": tool.function.arguments,
                        "output": output
                    })
                else:
                    print('Function', tool.function.name, 'not found')
            except Exception as e:
                print('Error calling function:', e)
                context_handler.tool_context_chain.append(
                    Context(tool.function.name, Context.TOOL_STRING, str(e))
                )