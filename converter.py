import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Конвертер RUB/USD"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # Получаем курс доллара
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = response.json()
    usd_rate = data['Valute']['USD']['Value']

    # Поле для ввода рублей
    rub_input = ft.TextField(label="Рубли", width=200)

    # Поле для вывода долларов
    usd_output = ft.TextField(label="Доллары", width=200, read_only=True)

    # Функция конвертации
    def convert(e):
        try:
            rub = float(rub_input.value)
            usd = rub / usd_rate
            usd_output.value = f"{usd:.2f}"
        except ValueError:
            usd_output.value = "Ошибка"
        page.update()

    # Кнопка конвертации
    convert_button = ft.ElevatedButton("Конвертировать", on_click=convert)

    # Добавляем элементы на страницу
    page.add(
        ft.Text(f"Курс USD: {usd_rate:.2f} RUB"),
        rub_input,
        usd_output,
        convert_button
    )

ft.app(target=main)
