from typing import Callable, Dict

'''
Implementing a Singleton Design Pattern for keeping track of all the functions we have and map those in dictionary,
by using this we can add new functions seemlessly without touching the main workflow or engine code.

This method is better than the simple dictionary method specified in docs as its better in long term.

This exposes a single instance to be used everywhere and will update the registry easily with the register method.
'''

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str):
        #Usage: @registry.register("my_tool")
        def decorator(func: Callable):
            self._tools[name] = func
            return func
        return decorator

    def get_tool(self, name: str):
        return self._tools.get(name)


registry = ToolRegistry()
