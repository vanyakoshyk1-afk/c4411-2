result = []


def divider(a, b):
    # Додаємо обробку TypeError, якщо a або b не є числами для порівняння/ділення
    # Хоча порівняння можна робити з різними типами, для ділення потрібні числа.
    # Проте, винятки ValueError та IndexError генеруються всередині,
    # а ZeroDivisionError та TypeError можуть виникнути при a/b або data[kem]

    if a < b:
        # Генерується, якщо a < b
        raise ValueError("Помилка значення: 'a' менше за 'b'")
    if b > 100:
        # Генерується, якщо b > 100
        raise IndexError("Помилка індексу: 'b' більше за 100")

    return a / b  # Може виникнути ZeroDivisionError або TypeError


data = {10: 2, 2: 5, "123": 4, 18: 0, []: 15, 8: 4}

for key in data:
    try:
        # Потенційні винятки:
        # 1. TypeError: якщо data[key] викликає помилку (наприклад, key є [] або "123" і викликається divider)
        # 2. Помилки всередині divider: ValueError, IndexError, ZeroDivisionError

        # Виправлення: в оригінальному коді помилка data[kem]. Правильний ключ - key
        res = divider(key, data[key])
        result.append(res)

    except ValueError as e:
        # Обробка ValueError, згенерованого всередині divider
        print(f"Помилка ValueError для ключа {key}: {e}")
        result.append(None)  # Додаємо None, щоб зберегти кількість ітерацій
    except IndexError as e:
        # Обробка IndexError, згенерованого всередині divider
        print(f"Помилка IndexError для ключа {key}: {e}")
        result.append(None)
    except ZeroDivisionError as e:
        # Обробка ZeroDivisionError, згенерованого при a / b
        print(f"Помилка ZeroDivisionError для ключа {key}: Ділення на нуль")
        result.append(None)
    except TypeError as e:
        # Обробка TypeError, який може виникнути через:
        # - data[key] (якщо key - нехешований об'єкт, але тут ключі хешовані, тому це менш імовірно)
        # - при виклику divider(key, data[key]) - неможливе порівняння або ділення нечислових типів
        # - при key < data[key] або key / data[key]
        print(f"Помилка TypeError для ключа {key}: Неправильні типи для операції - {e}")
        result.append(None)
    except Exception as e:
        # Обробка будь-яких інших непередбачених винятків
        print(f"Невідома помилка для ключа {key}: {e}")
        result.append(None)

print("\nФінальний результат:", result)