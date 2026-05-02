from tools.tools import *

TOOLS = {
    "random_numbers": random_numbers,
    "find_max": find_max,
    "reverse_string": reverse_string,
}

TOOL_DESCRIPTIONS = {
    "random_numbers": "Generate random numbers. args: count:int, min_val:int, max_val:int",
    "find_max": "Find the largest number. args: numbers:list[int]",
    "reverse_string": "Reverse a string. args: s:str",
}