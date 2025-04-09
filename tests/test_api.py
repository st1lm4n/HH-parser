import pytest
from unittest.mock import Mock, patch
from src.api import HeadHunterAPI
import requests


@patch('src.api.requests.get')
def test_get_vacancies_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"name": "Test"}]}
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    result = api.get_vacancies("python")

    assert len(result) == 1
    assert result[0]["name"] == "Test"


@patch('src.api.requests.get')
def test_get_vacancies_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Server Error"
    mock_get.return_value = mock_response

    api = HeadHunterAPI()

    # Изменяем тест для обработки возвращаемого значения
    result = api.get_vacancies("python")
    assert result == []  # Проверяем, что возвращается пустой список при ошибке


def test_api_validation():
    api = HeadHunterAPI()
    response = Mock()
    response.status_code = 404
    response.text = "Not Found"

    with pytest.raises(Exception) as e:
        api._validate_response(response)
    assert "404" in str(e.value)