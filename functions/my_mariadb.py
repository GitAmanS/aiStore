import requests

BASE_URL = "https://dummyjson.com/products"

def get_all_products(limit=10, skip=0, select=None):
    params = {"limit": limit, "skip": skip}
    if select:
        params["select"] = ",".join(select)
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_product_by_id(product_id):
    response = requests.get(f"{BASE_URL}/{product_id}")
    return response.json()

def search_products(query):
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    return response.json()

def get_products_by_category(category):
    response = requests.get(f"{BASE_URL}/category/{category}")
    return response.json()

def add_product(product_data):
    response = requests.post(BASE_URL, json=product_data)
    return response.json()

def update_product(product_id, product_data):
    response = requests.put(f"{BASE_URL}/{product_id}", json=product_data)
    return response.json()

def delete_product(product_id):
    response = requests.delete(f"{BASE_URL}/{product_id}")
    return response.json()

def get_all_categories():
    response = requests.get(f"{BASE_URL}/categories")
    return response.json()

# Example Usage
if __name__ == "__main__":
    print(get_all_products(limit=5))
    print(get_product_by_id(1))
    print(search_products("phone"))
    print(get_products_by_category("smartphones"))
    print(add_product({"title": "New Product", "price": 100}))
    print(update_product(1, {"price": 120}))
    print(delete_product(1))
    print(get_all_categories())

get_all_products_tool = {
    'type': 'function',
    'function': {
        'name': 'get_all_products',
        'description': 'Get all products',
        'parameters': {
            'type': 'object',
            'required': ['limit'],
            'properties': {
                'limit': {'type': 'integer', 'description': 'Number of products to return'},
                'skip': {'type': 'integer', 'description': 'Number of products to skip'},
                'select': {'type': 'array', 'description': 'List of fields to select'},
            },
        },
    },
}

get_product_by_id_tool = {
    'type': 'function',
    'function': {
        'name': 'get_product_by_id',
        'description': 'Get product by ID',
        'parameters': {
            'type': 'object',
            'required': ['product_id'],
            'properties': {
                'product_id': {'type': 'integer', 'description': 'ID of the product to retrieve'},
            },
        },
    },
}

search_products_tool = {
    'type': 'function',
    'function': {
        'name': 'search_products',
        'description': 'Search for products',
        'parameters': {
            'type': 'object',
            'required': ['query'],
            'properties': {
                'query': {'type': 'string', 'description': 'One or more keywords to search for in the products table'},
            },
        },
    },
}

get_products_by_category_tool = {
    'type': 'function',
    'function': {
        'name': 'get_products_by_category',
        'description': 'Get products by category',
        'parameters': {
            'type': 'object',
            'required': ['category'],
            'properties': {
                'category': {'type': 'string', 'description': 'Category of the products to retrieve'},
            },
        }}
}


add_product_tool = {
    'type': 'function',
    'function': {
        'name': 'add_product',
        'description': 'Add a new product',
        'parameters': {
            'type': 'object',
            'required': ['title', 'price'],
            'properties': {
                'title': {'type': 'string', 'description': 'Title of the product'},
                'price': {'type': 'number', 'description': 'Price of the product'},
            },
        },
    },
}


update_product_tool = {
    'type': 'function',
    'function': {
        'name': 'update_product',
        'description': 'Update an existing product',
        'parameters': {
            'type': 'object',
            'required': ['product_id', 'price'],
            'properties': {
                'product_id': {'type': 'integer', 'description': 'ID of the product to update'},
                'price': {'type': 'number', 'description': 'New price of the product'},
            },
            }
    }
}

delete_product_tool = {
    'type': 'function',
    'function': {
        'name': 'delete_product',
        'description': 'Delete a product',
        'parameters': {
            'type': 'object',
            'required': ['product_id'],
            'properties': {
                'product_id': {'type': 'integer', 'description': 'ID of the product to delete'},
            },
        },
    }
}

get_all_categories_tool = {
    'type': 'function',
    'function': {
        'name': 'get_all_categories',
        'description': 'Get all categories',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {},
        },
    },
}
globals()['get_all_products'] = get_all_products
globals()['get_product_by_id'] = get_product_by_id
globals()['search_products'] = search_products
globals()['get_products_by_category'] = get_products_by_category
globals()['add_product'] = add_product
globals()['update_product'] = update_product
globals()['delete_product'] = delete_product
globals()['get_all_categories'] = get_all_categories