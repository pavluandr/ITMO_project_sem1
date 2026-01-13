import pandas as pd

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



def get_top_n_products(data_clean, n=5, metric='quantity', date='all'):
    # Оставляем только операции продажи
    sales_data = data_clean[data_clean['Операция'] == "Продажа"]

    # Если указана конкретная дата, переназначаем ее
    if date != 'all':
        sales_data = sales_data[sales_data["Дата"] == date]

    # Обозначаем переменные для фильтрации в зависимости от указанной метрики
    if metric == 'quantity':
        agg_column = 'Количество упаковок, шт.'  # По чему составляется топ
        result_column = f'Сумма_{agg_column}'   # Название нового столбца в датафрейме
        agg_func = 'sum'  # Параметр агрегирования - сумма
    elif metric == 'revenue':
        agg_column = 'Сумма операции'
        result_column = f'Сумма_{agg_column}'
        agg_func = 'sum'
    else:
        return None
        
    # Группируем все записи для одинаковых названия товаров в одну строчку - сумма по товару, считаю сумму всех операций
    grouped_data = sales_data.groupby('Название товара', as_index=False).agg({agg_column: agg_func}).rename(columns={agg_column: result_column})

    # Сортировка по колонке по убыванию
    data_sorted = grouped_data.sort_values(by=result_column, ascending=False)
    return data_sorted.head(n)

