from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.saver import JSONSaver
import logging


def get_valid_input(prompt: str, max_value: int = 100) -> int:
    """
    Валидация ввода числовых значений
    :param prompt: Текст приглашения
    :param max_value: Максимальное допустимое значение
    :return: Введенное число
    """
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= max_value:
                return value
            print(f"Ошибка: введите число от 1 до {max_value}")
        except ValueError:
            print("Ошибка: введите целое число!")


def display_vacancies(vacancies: list) -> None:
    """Отображение списка вакансий"""
    if not vacancies:
        print("\nНет вакансий для отображения")
        return

    print("\nРезультаты поиска:")
    for i, vac in enumerate(vacancies, 1):
        salary_info = []
        if vac.salary_from > 0:
            salary_info.append(f"от {vac.salary_from}")
        if vac.salary_to > 0:
            salary_info.append(f"до {vac.salary_to}")

        salary_str = " ".join(salary_info) if salary_info else "не указана"
        print(f"{i}. {vac.title} | Зарплата: {salary_str} {vac.currency}")
        print(f"   Описание: {vac.description[:100]}...")
        print(f"   Ссылка: {vac.url}\n")


def user_interaction():
    """Основная функция взаимодействия с пользователем"""
    logging.info("Starting user interaction")

    try:
        hh_api = HeadHunterAPI()
        saver = JSONSaver()

        # Ввод поискового запроса
        while True:
            search_query = input("Введите поисковый запрос: ").strip()
            if search_query:
                break
            print("Ошибка: запрос не может быть пустым!")

        per_page = get_valid_input("Введите количество вакансий для поиска (1-100): ", 100)

        # Получение вакансий
        try:
            hh_data = hh_api.get_vacancies(search_query, per_page)
            vacancies = Vacancy.cast_to_object_list(hh_data)

            if not vacancies:
                print("\nПо вашему запросу вакансий не найдено. Попробуйте:")
                print("- Уточнить запрос (например 'Менеджер по продажам')")
                print("- Использовать английские термины")
                return

            print(f"\nНайдено вакансий: {len(vacancies)}")
            with_salary = sum(1 for v in vacancies if v.salary_from > 0)
            print(f"Из них с указанной зарплатой: {with_salary}")

            # Сохранение вакансий
            for vac in vacancies:
                saver.add_vacancy(vac)

            # Вывод топ N вакансий
            top_n = get_valid_input("\nВведите количество вакансий для топа: ", min(100, len(vacancies)))
            sorted_vacancies = sorted(
                vacancies,
                key=lambda x: (x.salary_from, x.salary_to),
                reverse=True
            )[:top_n]

            display_vacancies(sorted_vacancies)

            # Поиск по ключевому слову
            keyword = input("\nВведите ключевое слово для поиска в описании: ").strip()
            if keyword:
                filtered = saver.get_vacancies({"keyword": keyword})
                print(f"\nНайдено {len(filtered)} вакансий по ключевому слову '{keyword}':")
                for item in filtered:
                    print(f"- {item['title']} (ЗП: {item['salary']['from']}-{item['salary']['to']})")

        except Exception as e:
            print(f"\nОшибка при обработке вакансий: {str(e)}")
            logging.exception("Error processing vacancies")

    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {str(e)}")
        logging.critical(f"Application error: {str(e)}")


if __name__ == "__main__":
    user_interaction()