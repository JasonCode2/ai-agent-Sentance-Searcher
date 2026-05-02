import random

def random_numbers(count: int, min_val: int, max_val: int):
    return [random.randint(min_val, max_val) for _ in range(count)]

def find_max(numbers: list):
    return max(numbers)

def reverse_string(s: str):
    return s[::-1]