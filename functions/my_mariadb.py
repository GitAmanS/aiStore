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




def get_products_table(query):
    # comma and space separated keywords
    query = query.replace(',', ' ').replace('  ', ' ').strip()
    columns_to_check = ['title', 'description']
    queries = []
    for word in query.split(' '):
        for column in columns_to_check:
            queries.append(f"{column} LIKE '%{word}%'")
    query = f"SELECT * FROM products WHERE {' OR '.join(queries)}"
    return run_sql(query)
    

def get_products_count(query):
    # comma and space separated keywords
    query = query.replace(',', ' ').replace('  ', ' ').strip()
    columns_to_check = ['title', 'description']
    queries = []
    for word in query.split(' '):
        for column in columns_to_check:
            queries.append(f"{column} LIKE '%{word}%'")
    query = f"SELECT * FROM products WHERE {' OR '.join(queries)}"
    return len(run_sql(query))



















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

get_products_table_tool = {
    'type': 'function',
    'function': {
        'name': 'get_products_table',
        'description': 'Get products table',
        'parameters': {
            'type': 'object',
            'required': ['query'],
            'properties': {
                'query': {'type': 'string', 'description': 'One or more keywords to search for in the products table. Comma separated.'},
            },
        },
    },
}


get_products_count_tool = {
    'type': 'function',
    'function': {
        'name': 'get_products_count',
        'description': 'Get products count',
        'parameters': {
            'type': 'object',
            'required': ['query'],
            'properties': {
                'query': {'type': 'string', 'description': 'One or more keywords to search for in the products table'},
            },
        },
    },
}

globals()['run_sql'] = run_sql
globals()['get_products_table'] = get_products_table
globals()['get_products_count'] = get_products_count
