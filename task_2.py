from typing import Callable
from collections.abc import Generator
import re

Numbers_Generator = Generator[float]

def generator_numbers(text: str) -> Numbers_Generator:
    numbers = re.findall(r'\d+\.\d+', text)
    for num in numbers:
        yield float(num)
    
def sum_profit(text: str, func: Callable[[str], Numbers_Generator]):
    numbers_generator = func(text)
    return sum(numbers_generator)

text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")

