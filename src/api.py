from urllib.parse import quote
import requests
import logging


class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.headers = {
            "User-Agent": "MyApp/1.0 (skapincev.15@mail.ru)",
            "HH-User-Agent": "MyApp (skapincev.15@mail.ru)",
        }

    def get_vacancies(self, keyword: str, per_page: int = 100) -> list:
        try:
            # Кодируем только один раз и выводим для проверки
            original_text = keyword
            encoded_text = quote(original_text)

            params = {
                "text": original_text,  # Пробуем без кодирования
                "area": 113,
                "per_page": per_page,
                "locale": "RU",
                "enable_snippets": "true",
            }

            response = requests.get(self.BASE_URL, headers=self.headers, params=params, timeout=10)

            response.raise_for_status()

            data = response.json()

            return data.get("items", [])

        except Exception as e:
            logging.error(f"API Error: {str(e)}")
            return []
