import logging


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ['title', 'url', 'salary', 'description', 'currency']

    def __init__(self, title: str, url: str, salary: dict, description: str):
        """
        Инициализация вакансии
        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary: Зарплата
        :param description: Описание
        """
        try:
            self.title = self._validate_title(title)
            self.url = self._validate_url(url)
            self.salary = salary or {}
            self.description = description or ''
            self.currency = self._validate_currency()

            logging.debug(f"Created vacancy: {self.__repr__()}")

        except ValueError as e:
            logging.error(f"Invalid vacancy data: {str(e)}")
            raise

    def _validate_title(self, title: str) -> str:
        """Проверка названия вакансии"""
        if not title.strip():
            raise ValueError("Title cannot be empty")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Проверка URL вакансии"""
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format")
        return url

    def _validate_currency(self) -> str:
        """Определение валюты зарплаты"""
        return self.salary.get("currency", "RUR") if self.salary else "RUR"

    @property
    def salary_from(self) -> int:
        """Нижняя граница зарплаты"""
        try:
            return int(self.salary.get('from') or 0)
        except (TypeError, ValueError) as e:
            logging.warning(f"Invalid salary.from: {str(e)}")
            return 0

    @property
    def salary_to(self) -> int:
        """Верхняя граница зарплаты"""
        try:
            return int(self.salary.get('to') or 0)
        except (TypeError, ValueError) as e:
            logging.warning(f"Invalid salary.to: {str(e)}")
            return 0

    def __lt__(self, other) -> bool:
        """Сравнение вакансий по зарплате"""
        return self.salary_from < other.salary_from

    def __repr__(self) -> str:
        """Строковое представление вакансии"""
        return f"Vacancy({self.title}, {self.salary_from}-{self.salary_to} {self.currency})"

    @classmethod
    def cast_to_object_list(cls, data: list) -> list:
        """
        Создание списка объектов Vacancy из данных API
        :param data: Список вакансий из API
        :return: Список объектов Vacancy
        """
        return [
            cls(
                title=item.get("name"),
                url=item.get("alternate_url"),
                salary=item.get("salary") or {},
                description=item.get("snippet", {}).get("requirement", "")
            )
            for item in data
            if item.get("name") and item.get("alternate_url")
        ]