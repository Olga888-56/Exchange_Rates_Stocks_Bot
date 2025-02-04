def save_to_csv(rates):
    if not rates:
        print("Нет данных для сохранения")
        return
           

    data_to_save = [
        ["Валюта", "Курс"],
        ["USD", rates["USD"]],
        ["EUR", rates["EUR"]],
        ["GPB", rates["GPB"]],
        ["JPY", rates["JPY"]],
        ["CNY", rates["CNY"]],
    ]

    with open('currency.csv', 'w', encoding='utf-8', newline='') as cur_csv:
        writer = csv.writer(cur_csv)
        writer.writerows(data_to_save)
    print("Данные успешно сохранены в currency.csv")