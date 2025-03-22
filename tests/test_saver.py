import pytest
import json
from src.saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def saver(tmp_path):
    return JSONSaver(filename=tmp_path / "test_vacancies.json")


def test_add_vacancy(saver):
    vacancy = Vacancy(
        title="Python Dev",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000},
        description="Python experience required",
    )

    saver.add_vacancy(vacancy)
    with open(saver.filename, "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["title"] == "Python Dev"


def test_get_vacancies(saver):
    test_data = [{"title": "A", "description": "Python and Django"}, {"title": "B", "description": "Java Spring"}]

    with open(saver.filename, "w") as f:
        json.dump(test_data, f)

    result = saver.get_vacancies({"keyword": "python"})
    assert len(result) == 1
    assert result[0]["title"] == "A"


def test_duplicate_handling(saver):
    vacancy = Vacancy("Test", "url", None, "")
    saver.add_vacancy(vacancy)
    saver.add_vacancy(vacancy)

    with open(saver.filename, "r") as f:
        data = json.load(f)

    assert len(data) == 1


def test_search_with_missing_description(saver):
    test_data = [
        {'title': 'A', 'description': None},
        {'title': 'B', 'description': 'Опыт работы'}
    ]

    with open(saver.filename, 'w') as f:
        json.dump(test_data, f)

    result = saver.get_vacancies({'keyword': 'опыт'})
    assert len(result) == 1
    assert result[0]['title'] == 'B'
