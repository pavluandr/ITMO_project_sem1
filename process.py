import pandas as pd
import numpy as np

def load_sales_data(file_path):
    REQUIRED_COLS = [
    "ID операции",
    "Дата",
    "Адрес магазина",
    "Район магазина",
    "Артикул",
    "Название товара",
    "Отдел товара",
    "Количество упаковок, шт.",
    "Операция",
    "Цена руб./шт."
    ]
    # Перехватываем любую ошибку чтения файла, чтобы пользователь не видел огромный трейсбек.
    # Вместо этого выводим одно понятное сообщение и завершаем функцию.
    try:
        data = pd.read_csv(file_path, sep=";", encoding="utf-8")
    except Exception:
        try:
            data = pd.read_csv(file_path, sep=";", encoding="cp1251")
        except Exception:
            print(f"Не удалось прочесть файл, проверьте кодировку и разделитель: {file_path}")
            return None

    # После чтения файла проверяем структуру таблицы, если столбцы не совпадают с ожидаемыми,
    # то это значит, что файл не подходит.
    missing = [col for col in REQUIRED_COLS if col not in data.columns]
    if missing:
        print(f"Не удалось прочесть файл: {file_path}. Отсутстуют обязательные столбцы: {', '.join(missing)}")
        return None

    return data



def preprocess_data(data):
    # Если на вход пришёл None, то ничего не делаем, чтобы программа не падала
    if data is None:
        return None

    # Работаем с копией, чтобы не менять исходные данные
    data_clean = data.copy()

    # Приводим дату к формату datetime,
    # ошибки превращаются в NaN и будут удалены позже
    data_clean["Дата"] = pd.to_datetime(
        data_clean["Дата"], errors="coerce", dayfirst=True
    )

    # Количество упаковок делаем числом
    data_clean["Количество упаковок, шт."] = pd.to_numeric(
        data_clean["Количество упаковок, шт."], errors="coerce"
    )

    # Цена иногда может быть записана через запятую,
    # поэтому сначала заменяем её на точку
    data_clean["Цена руб./шт."] = (
        data_clean["Цена руб./шт."].astype(str).str.replace(",", ".", regex=False)
    )
    data_clean["Цена руб./шт."] = pd.to_numeric(
        data_clean["Цена руб./шт."], errors="coerce"
    )

    # Удаляем строки с пропусками
    before = len(data_clean)
    data_clean = data_clean.dropna()
    removed = before - len(data_clean)

    if removed > 0:
        print(f"Удалено строк с пустыми значениями: {removed}")

    # Считаем сумму операции
    data_clean["Сумма операции"] = (
        data_clean["Количество упаковок, шт."] * data_clean["Цена руб./шт."]
    )

    return data_clean

# функция 3


# функция 4


# функция 5


# функция 6


def get_top_n_products(data_clean, n=5, metric='quantity', date='all'):
    # заменить строчку с использованием функции 3. Отсекаем от датасета товары категории "Поступление"
    sales_data = data_clean[data_clean['Операция'] == "Продажа"]

    # Если указана конкретная дата, фильтруем датасет по этой дате
    if date != 'all':
        sales_data = sales_data[sales_data["Дата"] == date]

    # В соответствие с метрикой (количество или выручка) присваиваем колонку, по которой будет фильтровать
    if metric == 'quantity':
        sort_column = 'Количество упаковок, шт.'
    elif metric == 'revenue':
        sort_column = 'Сумма операции'
    else:
        return None

    # Фильтрации датасета по колонке фильтрации по убыванию
    data_sorted = sales_data.sort_values(by=sort_column, ascending=False)
    # Возвращаем n верхних строчек фильтрованного сортированного датасета
    return data_sorted.head(n)

def get_top_n_products(data_clean, n=5, metric='quantity'):

    return

