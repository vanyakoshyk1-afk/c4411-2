import time
from typing import Callable, Any


# Функція, що визначає час роботи (декоратор)
def timer_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()

        result = func(*args, **kwargs)  # Виклик оригінальної функції

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Функція '{func.__name__}' виконана за {elapsed_time:.4f} секунд.")
        return result

    return wrapper


# Приклад використання
@timer_decorator
def complex_operation(n):
    time.sleep(0.05)  # Імітація роботи
    return n * 2


result = complex_operation(10)