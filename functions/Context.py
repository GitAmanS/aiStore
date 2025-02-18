import json
import os

class Context:
    TOOL_STRING = 'tool'
    ASSISTANT_STRING = 'assistant'
    USER_STRING = 'user'

    def __init__(self, name, role, content):
        self.name = name
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            'name': self.name,
            'role': self.role,
            'content': self.content
        }
    
    def get(self, key):
        return self.__dict__.get(key)


class Context_Chain:
    def __init__(self, contexts=None):
        self.contexts = contexts if contexts is not None else []

    def __iter__(self):
        return iter(self.contexts)

    def append(self, context):
        self.contexts.append(context)

    def to_dict_list(self):
        return [context.to_dict() for context in self.contexts]


class Context_Handler:
    TOOL_STRING = 'tool_context'
    CONVERSATION_STRING = 'conversation_context'
    BASE_PATH = 'user_context_env'

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.tool_context_chain = Context_Chain()
        self.conversation_context_chain = Context_Chain()
        if not os.path.exists(self.BASE_PATH):
            os.makedirs(self.BASE_PATH)

    def get_context(self, type: str = None):
        try:
            with open(f'{self.BASE_PATH}/{self.TOOL_STRING}_{self.user_id}.json', 'r') as f:
                self.tool_context_chain = Context_Chain([Context(item.get('name'), item.get('role'), item.get('content')) for item in json.load(f)])
        except FileNotFoundError:
            self.tool_context_chain = Context_Chain()
        try:
            with open(f'{self.BASE_PATH}/{self.CONVERSATION_STRING}_{self.user_id}.json', 'r') as f:
                self.conversation_context_chain = Context_Chain([Context(item.get('name'), item.get('role'), item.get('content')) for item in json.load(f)])
        except FileNotFoundError:
            self.conversation_context_chain = Context_Chain()
        
        if type == self.TOOL_STRING:
            return self.tool_context_chain.to_dict_list()
        elif type == self.CONVERSATION_STRING:
            return self.conversation_context_chain.to_dict_list()
        else:
            return (self.tool_context_chain.to_dict_list(), 
                    self.conversation_context_chain.to_dict_list())

    def update_context(self, type: str = None):
        if type == self.TOOL_STRING:
            with open(f'{self.BASE_PATH}/{self.TOOL_STRING}_{self.user_id}.json', 'w') as f:
                json.dump(self.tool_context_chain.to_dict_list(), f, indent=4)
        elif type == self.CONVERSATION_STRING:
            with open(f'{self.BASE_PATH}/{self.CONVERSATION_STRING}_{self.user_id}.json', 'w') as f:
                json.dump(self.conversation_context_chain.to_dict_list(), f, indent=4)
        else:
            with open(f'{self.BASE_PATH}/{self.TOOL_STRING}_{self.user_id}.json', 'w') as f:
                json.dump(self.tool_context_chain.to_dict_list(), f, indent=4)
            with open(f'{self.BASE_PATH}/{self.CONVERSATION_STRING}_{self.user_id}.json', 'w') as f:
                json.dump(self.conversation_context_chain.to_dict_list(), f, indent=4)
    
    def update(self, type: str = None):
        return self.update_context(type)

    def set_context(self, new_context, type: str):
        if type == self.TOOL_STRING:
            self.tool_context_chain = Context_Chain([Context(item.get('name'), item.get('role'), item.get('content')) for item in new_context])
            self.update_context(type)
        elif type == self.CONVERSATION_STRING:
            self.conversation_context_chain = Context_Chain([Context(item.get('name'), item.get('role'), item.get('content')) for item in new_context])
            self.update_context(type)
        
    def append(self, new_context, type: str):
        if type == self.TOOL_STRING:
            self.tool_context_chain.append(Context(new_context.get('name'), new_context.get('role'), new_context.get('content')))
            self.update_context(type)
        elif type == self.CONVERSATION_STRING:
            self.conversation_context_chain.append(Context(new_context.get('name'), new_context.get('role'), new_context.get('content')))
            self.update_context(type)
        else:
            self.tool_context_chain.append(Context(new_context.get('name'), new_context.get('role'), new_context.get('content')))
            self.conversation_context_chain.append(Context(new_context.get('name'), new_context.get('role'), new_context.get('content')))
            self.update_context(type)
            print("Warning: Appended to both contexts")
        return self.get_context(type)

    def clear_context(self):
        self.tool_context_chain = Context_Chain()
        self.conversation_context_chain = Context_Chain()
        self.update_context(self.TOOL_STRING)
        self.update_context(self.CONVERSATION_STRING)
        os.remove(f'{self.BASE_PATH}/{self.TOOL_STRING}_{self.user_id}.json')
        os.remove(f'{self.BASE_PATH}/{self.CONVERSATION_STRING}_{self.user_id}.json')
        return self.get_context()