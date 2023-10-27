"""This a serverice that shows birthdays for the week"""
from datetime import datetime, timedelta
from collections import defaultdict


class WrongDataFormat(Exception):
    """ Specify custom exception."""
    def __init__(self, message):
        super().__init__(message)


NAME_KEY = 'name'
BIRTHDAY_KEY = 'birthday'


def get_birthdays_per_week(users: list[dict[str,datetime]]):
    """
    The function returns the next birthdays for a week from since.
    It grouping it by weekday. Days off are excluded for result.
    """
    print('------------------------------------------')
    week_length = 7
    birthday_users = defaultdict(list)
    today = datetime.today().date()

    if not is_valide(users):
        return

    for user in users:
        name = user[NAME_KEY]
        birthday = user[BIRTHDAY_KEY].date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year+1)

        delta_days = (birthday_this_year - today).days
        if delta_days < week_length:
            if birthday_this_year.weekday() ==  5:
                birthday_this_year = birthday_this_year + timedelta(days=2)
            elif birthday_this_year.weekday() == 6:
                birthday_this_year = birthday_this_year + timedelta(days=1)
            birthday_users[birthday_this_year.strftime("%A")].append(name)

    for name, user in birthday_users.items():
        result = ", ".join(user)
        print(f"{name}: {result}")


def is_valide(users: list[dict[str,datetime]]) -> bool:
    """ Validation function."""
    if not isinstance(users, list):
        raise WrongDataFormat('data must match the format: list[dict[str,datetime]]')

    for user in users:
        if not isinstance(user, dict):
            raise WrongDataFormat('Each user object shout be a dictionary')
        if NAME_KEY not in user.keys() or BIRTHDAY_KEY not in user.keys():
            raise WrongDataFormat(f'Each user object muht have key: {NAME_KEY} and {BIRTHDAY_KEY}')
        if not isinstance(user[NAME_KEY], str) or not isinstance(user[BIRTHDAY_KEY], datetime):
            raise WrongDataFormat(
                f'Key {NAME_KEY} should be "str" and key {BIRTHDAY_KEY} should be "datetime"'
                )

    return True


if __name__ == "__main__":
    example = [
        {'name': 'Кіану Рівз', 'birthday': datetime(1964, 9, 2)},
        {'name': 'Сальма Хайєк', 'birthday': datetime(1966, 9, 2)},
        {'name': 'Бейонсе', 'birthday': datetime(1981, 9, 4)},
        {'name': 'Зак Ефрон', 'birthday': datetime(1987, 9, 4)},
        {'name': 'Ідріс Ельба', 'birthday': datetime(1972, 9, 6)},
        {'name': 'Гвінет Пелтроу', 'birthday': datetime(1972, 9, 27)},
        {'name': 'Том Фелтон', 'birthday': datetime(1987, 9, 22)},
        {'name': 'Олівія Н\'ютон-Джон', 'birthday': datetime(1948, 9, 26)},
        {'name': 'Вінсент Ван Гог', 'birthday': datetime(1853, 9, 30)},
        {'name': 'Магнус Карлсен', 'birthday': datetime(1990, 9, 30)},
        {'name': 'Бріттек Робертсон', 'birthday': datetime(1990, 10, 1)},
        {'name': 'Стінґ', 'birthday': datetime(1951, 10, 2)},
        {'name': 'Гвен Стефані', 'birthday': datetime(1969, 10, 3)},
        {'name': 'Рей Манзарек', 'birthday': datetime(1939, 10, 4)},
        {'name': 'Кейт Винслет', 'birthday': datetime(1975, 10, 5)},
        {'name': 'Джеремі Самптер', 'birthday': datetime(1987, 10, 6)},
        {'name': 'Тоні Брікстон', 'birthday': datetime(1967, 10, 7)},
        {'name': 'Сігур Рос', 'birthday': datetime(1975, 10, 8)},
        {'name': 'Беянсе', 'birthday': datetime(1981, 10, 9)},
        {'name': 'Мішель Трете', 'birthday': datetime(1971, 10, 10)},
        {'name': 'Емір Кустуріца', 'birthday': datetime(1954, 10, 11)},
        {'name': 'Генрік Ібсен', 'birthday': datetime(1828, 10, 12)},
        {'name': 'Саша Барон-Коен', 'birthday': datetime(1971, 10, 13)},
        {'name': 'Ушер', 'birthday': datetime(1978, 10, 14)},
        {'name': 'Сара Фергюсон', 'birthday': datetime(1959, 10, 15)},
        {'name': 'Оскар Уайльд', 'birthday': datetime(1854, 10, 16)},
        {'name': 'Зігмунд Фрейд', 'birthday': datetime(1856, 10, 17)},
        {'name': 'Зак Ефрон', 'birthday': datetime(1987, 10, 18)},
        {'name': 'Джон Леннон', 'birthday': datetime(1940, 10, 19)},
        {'name': 'Сьюзан Сарандон', 'birthday': datetime(1946, 10, 20)},
        {'name': 'Кен Ватанабе', 'birthday': datetime(1959, 10, 21)},
        {'name': 'Дерек Джекобі', 'birthday': datetime(1938, 10, 22)},
        {'name': 'Райан Рейнольдс', 'birthday': datetime(1976, 10, 23)},
        {'name': 'Унікаль Дженнінґс', 'birthday': datetime(1973, 10, 24)},
        {'name': 'Кетрін Ленгфорд', 'birthday': datetime(1996, 10, 25)},
        {'name': 'Хіларі Клінтон', 'birthday': datetime(1947, 10, 26)},
        {'name': 'Тедді Рузвельт', 'birthday': datetime(1858, 10, 27)},
        {'name': 'Джоан Керрі', 'birthday': datetime(1979, 10, 28)},
        {'name': 'Уілльям Гершель', 'birthday': datetime(1738, 10, 29)},
        {'name': 'Генрі Вінклер', 'birthday': datetime(1945, 10, 30)},
        {'name': 'Пітер Джексон', 'birthday': datetime(1961, 10, 31)},
    ]

    try:
        get_birthdays_per_week(example)
    except WrongDataFormat as e:
        print(f"Caught the exception: {e} ")
