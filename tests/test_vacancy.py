from src.vacancy import Vacancy


def test_vacancy_creation():
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Требуется опыт работы 3 года",
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.currency == "RUR"


def test_vacancy_without_salary():
    vacancy = Vacancy(title="Java Developer", url="https://hh.ru/vacancy/456", salary=None, description="Стажировка")

    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0


def test_vacancy_comparison():
    v1 = Vacancy("A", "url1", {"from": 100000}, "")
    v2 = Vacancy("B", "url2", {"from": 150000}, "")

    assert v2 > v1


def test_cast_to_object_list():
    raw_data = [
        {"name": "Dev", "alternate_url": "url", "salary": None},
        {"name": None, "alternate_url": "url", "salary": {"from": 50000}},
    ]

    vacancies = Vacancy.cast_to_object_list(raw_data)
    assert len(vacancies) == 1
