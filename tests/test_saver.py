import pytest
import os
import json
from src.saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def temp_saver(tmp_path):
    return JSONSaver(tmp_path / "test.json")


def test_add_vacancy(temp_saver):
    vac = Vacancy("Test", "http://test.com", {}, "")
    temp_saver.add_vacancy(vac)

    with open(temp_saver._JSONSaver__filename, "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["title"] == "Test"


def test_duplicate_vacancy(temp_saver):
    vac = Vacancy("Test", "http://test.com", {}, "")
    temp_saver.add_vacancy(vac)
    temp_saver.add_vacancy(vac)

    with open(temp_saver._JSONSaver__filename, "r") as f:
        data = json.load(f)

    assert len(data) == 1


def test_delete_vacancy(temp_saver):
    vac = Vacancy("Test", "http://test.com", {}, "")
    temp_saver.add_vacancy(vac)
    temp_saver.delete_vacancy(vac)

    with open(temp_saver._JSONSaver__filename, "r") as f:
        data = json.load(f)

    assert len(data) == 0


def test_get_vacancies(temp_saver):
    vac1 = Vacancy("Python", "http://test.com", {}, "Django experience")
    vac2 = Vacancy("Java", "http://test.com", {}, "Spring framework")

    temp_saver.add_vacancy(vac1)
    temp_saver.add_vacancy(vac2)

    result = temp_saver.get_vacancies({"keyword": "django"})
    assert len(result) == 1
    assert result[0]["title"] == "Python"