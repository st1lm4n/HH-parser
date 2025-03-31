from abc import ABC, abstractmethod
from urllib.parse import quote
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int) -> list:
        pass

    @abstractmethod
    def _validate_response(self, response: requests.Response) -> None:
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API HeadHunter"""

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__headers = {
            "User-Agent": "MyApp/1.0 (skapincev.15@mail.ru)",
            "HH-User-Agent": "MyApp (skapincev.15@mail.ru)"
        }

    def _connect_to_api(self, params: dict) -> requests.Response:
        """Приватный метод для подключения к API"""
        try:
            return requests.get(
                self.BASE_URL,
                headers=self.__headers,
                params=params,
                timeout=30
            )
        except requests.RequestException as e:
            logging.error(f"Connection error: {str(e)}")
            raise

    def _validate_response(self, response: requests.Response) -> None:
        """Валидация ответа от API"""
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")

    def get_vacancies(self, keyword: str, per_page: int = 100) -> list:
        """
        Получение вакансий по ключевому слову"""
        try:
            params = {
                "text": f"NAME:{keyword}",
                "per_page": per_page,
                "locale": "RU",
                "search_field": "name"
            }

            response = self._connect_to_api(params)
            self._validate_response(response)

            data = response.json()
            logging.info(f"Received {len(data.get('items', []))} vacancies for query: '{keyword}'")

            return data.get("items", [])

        except Exception as e:
            logging.exception(f"Failed to get vacancies: {str(e)}")
            return []