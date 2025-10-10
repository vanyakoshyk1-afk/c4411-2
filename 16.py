import requests
from bs4 import BeautifulSoup


# --- Клас Конвертера Валют ---
class CurrencyConverter:
    """
    Клас для конвертації національної валюти (грн) у долари США (USD)
    на основі курсу, отриманого з сайту НБУ.
    """
    # Приклад URL сторінки НБУ з курсами (може змінитися!)
    NBU_URL = "https://bank.gov.ua/ua/markets/exchangerates"

    def __init__(self):
        """Ініціалізує конвертер і намагається отримати курс USD."""
        self.usd_rate = self._get_usd_rate()

    def _get_usd_rate(self):
        """
        Здійснює парсинг сторінки НБУ для отримання курсу долара США.
        Повертає курс (float) або None у разі помилки.
        """
        print(f"Отримання курсу з: {self.NBU_URL}...")
        try:
            # 1. Завантаження HTML-вмісту сторінки
            response = requests.get(self.NBU_URL)
            response.raise_for_status()  # Перевірка на помилки HTTP

            # 2. Парсинг за допомогою BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # 3. Пошук елемента з курсом USD
            # Увага: цей селектор є прикладом і може потребувати оновлення!
            # Наприклад, знаходимо рядок, де є "Долар США"
            usd_row = soup.find('td', text='Долар США')

            if usd_row:
                # Курс зазвичай знаходиться в наступному стовпці (наступний sibling)
                # Часто це 4-й <td> після назви валюти в рядку
                # Для цього прикладу, припустимо, курс знаходиться у наступному <td>
                # У реальності може знадобитися більш складний пошук, наприклад, по id таблиці та номеру колонки

                # Припустимо, шукаємо у рядку, який містить назву валюти
                parent_row = usd_row.find_parent('tr')
                if parent_row:
                    # Курс (офіційне значення) зазвичай знаходиться у 5-й колонці (індекс 4)
                    rate_element = parent_row.find_all('td')[4]
                    rate_text = rate_element.text.replace(',', '.').strip()
                    rate = float(rate_text)
                    print(f"✅ Успішно отримано курс USD: {rate}")
                    return rate

            print("❌ Не вдалося знайти курс USD на сторінці. Перевірте селектор.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Помилка під час підключення або завантаження сторінки: {e}")
            return None
        except Exception as e:
            print(f"❌ Помилка парсингу: {e}")
            return None

    def convert_to_usd(self, amount_uah: float) -> float:
        """
        Конвертує суму з UAH у USD.

        :param amount_uah: Сума у національній валюті (грн).
        :return: Сума у доларах США (USD).
        """
        if self.usd_rate is None:
            print("Конвертація неможлива: не вдалося отримати актуальний курс.")
            return 0.0

        # Конвертація: сума в грн / курс грн до 1 USD
        amount_usd = amount_uah / self.usd_rate
        return amount_usd


# --- Основна логіка програми ---
def main():
    """Основна функція для взаємодії з користувачем."""

    # 1. Ініціалізація конвертера та отримання курсу
    converter = CurrencyConverter()

    if converter.usd_rate is None:
        print("\nПрограма завершує роботу через неможливість отримати курс.")
        return

    # 2. Отримання вводу від користувача
    while True:
        try:
            print("\n---------------------------------------------------")
            user_input = input("Введіть суму у валюті своєї країни (UAH) для конвертації або 'вихід': ")

            if user_input.lower() in ('вихід', 'exit'):
                print("👋 Дякуємо за використання! До побачення.")
                break

            amount_uah = float(user_input)

            if amount_uah < 0:
                print("Будь ласка, введіть невід'ємне число.")
                continue

            # 3. Конвертація та виведення результату
            amount_usd = converter.convert_to_usd(amount_uah)

            print(f"\n📊 Курс USD: {converter.usd_rate} грн за 1 $")
            print(f"💰 {amount_uah:,.2f} грн = **{amount_usd:,.2f} $ США**")

        except ValueError:
            print("❗ Помилка: Введено некоректне число. Будь ласка, спробуйте ще.")
        except Exception as e:
            print(f"Сталася непередбачена помилка: {e}")


if __name__ == "__main__":
    main()