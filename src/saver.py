import json
import logging

logging.basicConfig(level=logging.INFO)


class JSONSaver:
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy) -> None:
        """Добавление вакансии в файл"""
        try:
            data = self._read_file()
            vacancy_data = {
                "title": vacancy.title,
                "url": vacancy.url,
                "salary": {"from": vacancy.salary_from, "to": vacancy.salary_to, "currency": vacancy.currency},
                "description": vacancy.description,
            }
            if vacancy_data not in data:
                data.append(vacancy_data)
                self._write_file(data)
        except Exception as e:
            logging.error(f"Error saving vacancy: {str(e)}")

    def get_vacancies(self, criteria: dict) -> list:
        """Поиск вакансий по критериям"""
        data = self._read_file()
        keyword = criteria.get('keyword', '').lower()
        return [
            v for v in data
            if keyword in (v.get('description', '') or '').lower()  # Исправлено
        ]

    def _read_file(self) -> list:
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: list) -> None:
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
