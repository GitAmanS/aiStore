import ollama
from typing import Dict, Any, Callable
import json

import mariadb

def get_connection():
    # Connection Configuration
    config = {
        "user": "root",
        "password": "",
        "host": "localhost",  # Change to the server IP if remote
        "port": 3306,
        "database": "archisty"
    }

    try:
        # Establish Connection
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        
        # Example Query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"Connected to MariaDB, Version: {version[0]}")

        # Close cursor
        cursor.close()
        
        return conn

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def run_sql(query):
    """
    Run a SQL query
    """
    if not query or query == "":
        print("No query provided")
        return "No query provided"
    print(f"\nRunning query: {query}\n")
    conn = get_connection()
    if conn is None:
        print("Failed to get connection")
        return "Failed to get connection"
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error running query: {e}")
        result = "Error running query - " + str(e)
    cursor.close()
    conn.close()
    return result

globals()['run_sql'] = run_sql

# Manual tool definition
run_sql_tool = {
    'type': 'function',
    'function': {
        'name': 'run_sql',
        'description': 'Run a MariaDB query',
        'parameters': {
            'type': 'object',
            'required': ['query'],
            'properties': {
                'query': {'type': 'string', 'description': 'The SQL query to run'},
            },
        },
    },
}
context = []




def get_response(prompt: str, use_tools: bool = True) -> Any:
    context.append({'role': 'user', 'content': prompt})

    available_functions: Dict[str, Callable] = {
        'run_sql': run_sql,
    }

    response = ollama.chat(
        'llama3.2',
        messages=context,
        tools=[run_sql_tool] if use_tools else None,
    )

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            try:
                if function_to_call := available_functions.get(tool.function.name):
                    print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = function_to_call(**tool.function.arguments)
                    print('Function output:', output)
                    context.append({'role': 'tool', 'name': tool.function.name, 'content': str(output)})
                else:
                    print('Function', tool.function.name, 'not found')
            except Exception as e:
                print('Error calling function:', e)
                context.append({'role': 'tool', 'name': tool.function.name, 'content': str(e)})
        final_response = ollama.chat(
            'llama3.2',
            messages=context,
        )
        context.append({'role': 'assistant', 'content': final_response.message.content})
        return final_response

    
    return response




