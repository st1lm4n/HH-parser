import json
from unittest.mock import patch, MagicMock, call

import pytest

from src.api import HeadHunterAPI
from src.saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def mock_api():
    return MagicMock(spec=HeadHunterAPI)


@pytest.fixture
def mock_saver(tmp_path):
    return JSONSaver(filename=tmp_path / "test_vacancies.json")


def test_full_flow(mock_api, mock_saver, tmp_path):
    test_vacancies = [
        {
            "name": "Python Developer",
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Опыт работы 3 года"},
        }
    ]

    input_values = ["Python", "5", "3", "опыт"]

    with patch("builtins.input", side_effect=input_values), patch(
        "src.api.HeadHunterAPI", return_value=mock_api
    ), patch("src.saver.JSONSaver", return_value=mock_saver), patch("builtins.print") as mock_print:
        # Настройка mock API
        mock_api.get_vacancies.return_value = test_vacancies

        from main import user_interaction

        user_interaction()

    # Проверяем вызовы API
    mock_api.get_vacancies.assert_called_once_with("Python", 5)

    # Проверяем сохранение данных
    assert len(mock_saver.get_vacancies({})) == 1

    # Проверяем вывод
    expected_calls = [
        call("\nТоп вакансий:"),
        call("Python Developer | Зарплата: 100000-150000 RUR"),
        call("\nНайдено 1 вакансий:"),
        call("Python Developer - 100000-150000"),
    ]
    mock_print.assert_has_calls(expected_calls, any_order=False)


def test_error_handling(mock_api):
    input_values = ["C++", "3", "2", "template"]

    with patch("builtins.input", side_effect=input_values), patch(
        "src.api.HeadHunterAPI", return_value=mock_api
    ), patch("src.saver.JSONSaver.add_vacancy", side_effect=Exception("DB Error")), patch(
        "builtins.print"
    ) as mock_print:
        mock_api.get_vacancies.return_value = [{"name": "Test", "alternate_url": "test"}]

        from main import user_interaction

        user_interaction()

    # Проверяем вывод ошибки
    mock_print.assert_any_call("\nОшибка при сохранении вакансии: DB Error")


def test_filtering_logic(tmp_path):
    # Тест фильтрации с реальным сохранением в файл
    saver = JSONSaver(filename=tmp_path / "filter_test.json")
    test_data = [{"title": "A", "description": "Python experience"}, {"title": "B", "description": "Java experience"}]

    with open(saver.filename, "w") as f:
        json.dump(test_data, f)

    result = saver.get_vacancies({"keyword": "python"})
    assert len(result) == 1
    assert result[0]["title"] == "A"


def test_sorting_logic():
    # Тест правильности сортировки вакансий
    vacancies = [Vacancy("High", "url1", {"from": 200000}, ""), Vacancy("Low", "url2", {"from": 100000}, "")]

    sorted_vacancies = sorted(vacancies, key=lambda x: x.salary_from, reverse=True)
    assert sorted_vacancies[0].salary_from == 200000
    assert sorted_vacancies[1].salary_from == 100000
