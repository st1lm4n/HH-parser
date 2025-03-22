from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.saver import JSONSaver


def user_interaction():
    hh_api = HeadHunterAPI()

    # Ввод параметров
    search_query = input("Введите поисковый запрос: ")
    per_page = int(input("Введите количество вакансий (макс. 100): "))
    per_page = min(per_page, 100)

    # Получение данных
    hh_data = hh_api.get_vacancies(search_query, per_page)
    vacancies = Vacancy.cast_to_object_list(hh_data)

    # Сохранение
    saver = JSONSaver()
    for vac in vacancies:
        try:
            saver.add_vacancy(vac)
        except Exception as e:
            print(f"\nОшибка при сохранении вакансии: {str(e)}")

    # Топ N по зарплате
    top_n = int(input("\nВведите количество вакансий для топа: "))
    filtered_vacancies = [v for v in vacancies if v.salary_from > 0]
    sorted_vacancies = sorted(filtered_vacancies, key=lambda x: x.salary_from, reverse=True)[:top_n]

    if sorted_vacancies:
        print("\nТоп вакансий:")
        for vac in sorted_vacancies:
            salary_to = vac.salary_to if vac.salary_to > 0 else "не указано"
            print(f"{vac.title} | Зарплата: {vac.salary_from}-{salary_to} {vac.currency}")
    else:
        print("\nНет вакансий для отображения в топе")

    # Фильтр по описанию
    keyword = input("\nВведите ключевое слово для поиска: ")
    filtered = saver.get_vacancies({"keyword": keyword})
    print(f"\nНайдено {len(filtered)} вакансий:")
    for item in filtered:
        salary_from = item["salary"]["from"]
        salary_to = item["salary"]["to"] if item["salary"]["to"] > 0 else "не указано"
        print(f"{item['title']} - {salary_from}-{salary_to}")


if __name__ == "__main__":
    user_interaction()
