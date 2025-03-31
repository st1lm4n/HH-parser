from unittest.mock import patch

from main import get_valid_input, user_interaction


def test_get_valid_input(monkeypatch):
    # Test valid input
    monkeypatch.setattr('builtins.input', lambda _: "10")
    assert get_valid_input("Test: ") == 10

    # Test invalid input
    inputs = iter(["invalid", "5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_valid_input("Test: ") == 5


@patch('main.HeadHunterAPI')
@patch('main.JSONSaver')
def test_user_interaction(mock_saver, mock_api):
    mock_api_instance = mock_api.return_value
    mock_api_instance.get_vacancies.return_value = [{
        "name": "Python Developer",
        "alternate_url": "http://hh.ru/vacancy/1",
        "salary": {"from": 100000},
        "snippet": {"requirement": "Python experience"}
    }]

    mock_saver_instance = mock_saver.return_value

    inputs = [
        "Python",
        "10",  # per_page
        "5",  # top_n
        "python"  # keyword
    ]

    with patch('builtins.input', side_effect=inputs):
        user_interaction()

    assert mock_api_instance.get_vacancies.called
    assert mock_saver_instance.add_vacancy.called
