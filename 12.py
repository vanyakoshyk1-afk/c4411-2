import colorama
from colorama import Fore, Back, Style, init

# Обов'язково викликаємо init() для ініціалізації Colorama,
# особливо на Windows. Вона автоматично конвертує коди ANSI в команди WinAPI.
init(autoreset=True) # Встановлюємо autoreset=True, щоб стиль скидався автоматично після кожного print()

# 1. Fore.RED - Колір тексту: Червоний
print(Fore.RED + 'Цей текст буде червоним.')

# 2. Back.GREEN - Колір фону: Зелений
print(Back.GREEN + 'Цей текст має зелений фон.')

# 3. Style.BRIGHT - Стиль тексту: Яскравий
# + Fore.YELLOW - Колір тексту: Жовтий
print(Style.BRIGHT + Fore.YELLOW + 'Цей текст буде яскраво-жовтим.')

# 4. Style.RESET_ALL - Скидання всіх стилів
print(Fore.CYAN + 'Це бірюзовий текст. ' + Style.RESET_ALL + 'Це звичайний текст.')
# При autoreset=True Style.RESET_ALL можна і не викликати в кінці,
# але він важливий, коли autoreset=False або для скидання в середині рядка.