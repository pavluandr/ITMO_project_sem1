import matplotlib.pyplot as plt
import seaborn as sns
from process import load_sales_data, preprocess_data, get_top_n_products, calculate_revenue_by_period

def present_revenue_by_period(data, period='D'):
    revenue_data = calculate_revenue_by_period(data, period)# Получаем данные из функции calculate_revenue_by_period
    
    if period == 'D':
        labels = revenue_data['Дата'].dt.strftime('%Y-%m-%d')# Получаем названия периодов
        title_period = "дням"
    elif period == 'W':
        labels = ["Неделя " + str(i+1) for i in range(len(revenue_data))]# Формируем всё по дням, неделям, месяцам
        title_period = "неделям"
    else:
        labels = revenue_data['Дата'].dt.strftime('%Y-%m')
        title_period = "месяцам"
    
    values = revenue_data['Выручка по периоду']  # Данные для диаграммы
    
    plt.figure(figsize=(10, 8))
    
    colors = sns.color_palette("husl", len(values))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    
    plt.title(f'Распределение выручки по {title_period}', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout() # Делаем диаграмму круглой и оторбажаем
    plt.show()



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
        while True:
            print("\nВыберите период для анализа выручки:")
            print("1. По дням")
            print("2. По неделям") 
            print("3. По месяцам")
            period_choice = input("Введите число (1-3): ")
            
            if period_choice == '1':
                period = 'D'
                period_name = "дням"
                break
            elif period_choice == '2':
                period = 'W'
                period_name = "неделям"
                break
            elif period_choice == '3':
                period = 'M'
                period_name = "месяцам"
                break
            else:
                print("Некорректный выбор. Пожалуйста, введите число от 1 до 3.")
        
        print(f"\nСтрою круговую диаграмму распределения выручки по {period_name}...")
        present_revenue_by_period(clean_data, period)

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
