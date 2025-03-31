from abc import ABC, abstractmethod
import json
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)


class Saver(ABC):
    """Абстрактный класс для работы с хранилищами данных"""

    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy') -> None:
        pass


class JSONSaver(Saver):
    """Класс для сохранения вакансий в JSON файл"""

    def __init__(self, filename: str = "vacancies.json"):
        self.__filename = filename
        logging.info(f"Initialized JSONSaver with file: {filename}")

    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        """Добавление вакансии в файл"""
        try:
            data = self._read_file()
            vacancy_data = self._create_vacancy_dict(vacancy)

            if not any(v['url'] == vacancy_data['url'] for v in data):
                data.append(vacancy_data)
                self._write_file(data)
                logging.info(f"Vacancy '{vacancy.title}' added to {self.__filename}")
            else:
                logging.debug(f"Vacancy '{vacancy.title}' already exists, skipping")

        except Exception as e:
            logging.error(f"Error saving vacancy: {str(e)}")
            raise

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict]:
        """Поиск вакансий по критериям"""
        try:
            data = self._read_file()
            keyword = criteria.get('keyword', '').lower()

            return [
                v for v in data
                if keyword in (v.get('description', '') or '').lower()
                   or keyword in (v.get('title', '') or '').lower()
            ]
        except Exception as e:
            logging.error(f"Error getting vacancies: {str(e)}")
            return []

    def delete_vacancy(self, vacancy: 'Vacancy') -> None:
        """Удаление вакансии из файла"""
        try:
            data = self._read_file()
            vacancy_data = self._create_vacancy_dict(vacancy)

            initial_count = len(data)
            data = [v for v in data if v['url'] != vacancy_data['url']]

            if len(data) < initial_count:
                self._write_file(data)
                logging.info(f"Vacancy '{vacancy.title}' removed from {self.__filename}")
            else:
                logging.warning(f"Vacancy '{vacancy.title}' not found in file")

        except Exception as e:
            logging.error(f"Error deleting vacancy: {str(e)}")
            raise

    def _create_vacancy_dict(self, vacancy: 'Vacancy') -> Dict[str, Any]:
        """Создание словаря с данными вакансии"""
        return {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": {
                "from": vacancy.salary_from,
                "to": vacancy.salary_to,
                "currency": vacancy.currency
            },
            "description": vacancy.description
        }

    def _read_file(self) -> List[Dict]:
        """Чтение данных из файла"""
        try:
            with open(self.__filename, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[Dict]) -> None:
        """Запись данных в файл"""
        with open(self.__filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)