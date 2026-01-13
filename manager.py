import matplotlib.pyplot as plt
import seaborn as sns
from process import load_sales_data, preprocess_data, get_top_n_products

# Вывести топ продуктов
def present_top_n_products(data, n, metric, date):
    # Создание датафрейма из функции в другом модуле
    df = get_top_n_products(data, n, metric, date)

    # Палитра цветов из сиборна
    colors = sns.color_palette("husl", n)
    # Для каждой метрики строим горизонтальный барчарт
    if metric == 'revenue':
        plt.barh(df["Название товара"], df["Сумма_Сумма операции"], edgecolor='black', color=colors)
        plt.title("Топ самых продаваемых товаров по выручке")
        plt.ylabel("Рублей")
    else:
        plt.barh(df["Название товара"], df["Сумма_Количество упаковок, шт."], edgecolor='black', color=colors)
        plt.title("Топ самых продаваемых товаров по количеству")
        plt.ylabel("Упаковок")
    plt.show()
    


def get_user_request():
    data = load_sales_data("Data 1.csv")
    clean_data = preprocess_data(data)

    while True:
        print("Выберите функцию из списка ниже: ")
        print("1. Посчитать выручку за период.")
        print("2. Посчитать прибыль за период.")
        print("3. Сгруппировать данные по отделам.")
        print("4. Получить топ самых продаваемых товаров.")
        print("5. Проанализировать движение товаров.")
        user_request = input("Введите число, соответствующее выбранной функции: ")
        if user_request in [str(x) for x in range(1, 6)]:
            print()
            break
        else:
            print("Функция введена неверно, попробуйте еще раз.")
    
    if user_request == '1':
        pass

    if user_request == '2':
        pass

    if user_request == '3':
        pass

    if user_request == '4':
        while True:
            try:
                n = int(input("Сколько самых продаваемых товаров вы хотите увидеть? --- "))
                if n <= 0:
                    raise ValueError
                break
            except:
                print("Пожалуйста, введите целое положительное число")
        
        while True:
            available_metrics = {
                '1' : 'quantity',
                '2' : 'revenue'
            }
            s = input("По какому параметру составить топ (введите число): количество (1) или выручка (2)? --- ")
            if s in available_metrics.keys():
                metric = available_metrics[s]
                break
            else:
                print("Что-то пошло не так, попробуйте еще раз.")
        
        while True:
            s = input("По какой дате составить топ? Введите дату в формате 'ГГГГ-ММ-ДД' или '0' если хотите получить информацию за весь период. --- ")
            if s == "0":
                date = 'all'
                break
            elif s in clean_data["Дата"].unique():
                date = s
                break
            else:
                print("Дата введена некорректно, попробуйте еще раз.")
        present_top_n_products(clean_data, n, metric, date)
    
    if user_request == '5':
        pass

if __name__ == "__main__":
    get_user_request()

