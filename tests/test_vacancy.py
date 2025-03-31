import pytest
from src.vacancy import Vacancy
import logging


def test_vacancy_creation():
    vac = Vacancy("Test Title", "http://test.com", {"from": 100000, "to": 200000}, "Test description")
    assert vac.title == "Test Title"
    assert vac.url == "http://test.com"
    assert vac.salary_from == 100000
    assert vac.salary_to == 200000
    assert vac.currency == "RUR"
    assert vac.description == "Test description"


def test_vacancy_without_salary():
    vac = Vacancy("Test", "http://test.com", None, "")
    assert vac.salary_from == 0
    assert vac.salary_to == 0
    assert vac.currency == "RUR"


def test_vacancy_comparison():
    vac1 = Vacancy("Junior", "http://test.com", {"from": 50000}, "")
    vac2 = Vacancy("Senior", "http://test.com", {"from": 150000}, "")
    assert vac1 < vac2


def test_invalid_vacancy():
    with pytest.raises(ValueError):
        Vacancy("", "http://test.com", {}, "")

    with pytest.raises(ValueError):
        Vacancy("Test", "invalid_url", {}, "")


def test_cast_to_object_list():
    api_data = [{
        "name": "Python Developer",
        "alternate_url": "http://hh.ru/vacancy/1",
        "salary": {"from": 100000, "currency": "RUR"},
        "snippet": {"requirement": "Python experience"}
    }]

    vacancies = Vacancy.cast_to_object_list(api_data)
    assert len(vacancies) == 1
    assert vacancies[0].title == "Python Developer"