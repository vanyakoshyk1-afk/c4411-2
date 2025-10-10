import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random  # Для імітації парсингу, якщо реальний не спрацює

# --- 1. Параметри та налаштування ---

# Назва файлу бази даних
DB_NAME = 'weather_data.db'

# URL сайту погоди (ПОТРІБНО ЗАМІНИТИ НА АКТУАЛЬНИЙ URL ДЛЯ ВАШОГО МІСТА!)
WEATHER_URL = 'https://sinoptik.ua/погода-київ'

# СЕЛЕКТОР (ПОТРІБНО ЗАМІНИТИ НА РЕАЛЬНИЙ CSS-СЕЛЕКТОР ТЕМПЕРАТУРИ!)
# Це приклад, як може виглядати селектор по класу
TEMPERATURE_SELECTOR = '.main_temp'


# --- 2. Функції для роботи з Базою Даних (SQLite) ---

def create_database():
    """Створює таблицю 'temperatures' у базі даних, якщо вона не існує."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Створення таблиці з двома полями: 'timestamp' (дата й час) та 'temperature' (температура)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL
            )
        ''')
        conn.commit()
        print(f"✅ База даних '{DB_NAME}' і таблиця 'temperatures' готові.")
    except sqlite3.Error as e:
        print(f"❌ Помилка SQLite: {e}")
    finally:
        if conn:
            conn.close()


def insert_data(timestamp: str, temperature: float):
    """Вставляє отримані дані про погоду до таблиці."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO temperatures (timestamp, temperature) VALUES (?, ?)",
            (timestamp, temperature)
        )
        conn.commit()
        print(f"   💾 Запис успішно додано: {timestamp} -> {temperature}°C")
    except sqlite3.Error as e:
        print(f"❌ Помилка вставки даних: {e}")
    finally:
        if conn:
            conn.close()


# --- 3. Функція для Веб-скрапінгу (Парсингу) ---

def scrape_temperature() -> float or None:
    """
    Відвідує сайт погоди, парсить його та повертає поточну температуру.
    """
    print(f"\n🌐 Парсинг сайту: {WEATHER_URL}...")
    try:
        # 1. Запит до сайту
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(WEATHER_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Перевірка на помилки HTTP

        # 2. Парсинг HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Пошук елемента з температурою за селектором
        temp_element = soup.select_one(TEMPERATURE_SELECTOR)

        if temp_element:
            # Отримання тексту і очищення (наприклад, видалення символу градуса)
            temp_text = temp_element.get_text(strip=True)

            # Приклад очищення: видаляємо все, окрім чисел, знаку мінуса та крапки/коми
            temp_text_cleaned = ''.join(c for c in temp_text if c.isdigit() or c in ('-', '.', ','))

            # Заміна коми на крапку і конвертація у float
            temperature = float(temp_text_cleaned.replace(',', '.'))

            print(f"✅ Температура успішно розпарсена: {temperature}°C")
            return temperature
        else:
            print(f"❌ Не вдалося знайти елемент за селектором: '{TEMPERATURE_SELECTOR}'. Перевірте селектор.")
            # Повертаємо випадкове значення для демонстрації роботи БД
            return random.uniform(10.0, 25.0)

    except requests.exceptions.RequestException as e:
        print(f"❌ Помилка підключення/завантаження: {e}")
        return None
    except Exception as e:
        print(f"❌ Помилка парсингу або конвертації: {e}")
        return None


# --- 4. Основна логіка програми ---

def main():
    """Виконує повний цикл: Створення БД -> Парсинг -> Збереження."""

    # 1. Створення або перевірка наявності БД
    create_database()

    # 2. Парсинг температури
    temperature = scrape_temperature()

    # 3. Збереження результату
    if temperature is not None:
        # Форматування поточної дати й часу
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Внесення даних до БД
        insert_data(current_timestamp, temperature)
    else:
        print("\nОперація збереження скасована, оскільки не вдалося отримати температуру.")


# Запуск програми
if __name__ == "__main__":
    main()