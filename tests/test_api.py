from src.api import HeadHunterAPI



def test_get_vacancies_success(requests_mock):
    api = HeadHunterAPI()
    mock_data = {"items": [{"id": "1", "name": "Python Developer"}]}
    requests_mock.get(api.BASE_URL, json=mock_data, status_code=200)

    result = api.get_vacancies("Python", 10)
    assert len(result) == 1
    assert result[0]["name"] == "Python Developer"


def test_get_vacancies_empty_response(requests_mock):
    api = HeadHunterAPI()
    requests_mock.get(api.BASE_URL, json={}, status_code=200)

    result = api.get_vacancies("Java", 5)
    assert result == []


def test_get_vacancies_error_handling(requests_mock):
    api = HeadHunterAPI()
    requests_mock.get(api.BASE_URL, status_code=400)

    result = api.get_vacancies("C++", 3)
    assert result == []
