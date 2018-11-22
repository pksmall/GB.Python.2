# L02 task #2

import json

'''
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), 
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл 
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''
data_dir = 'data'
orders_file = 'orders.json'


def write_order_to_json(item, qty, price, buyer, date):
    with open(data_dir+"/"+orders_file) as f_n:
        f_n_content = f_n.read()
        obj = json.loads(f_n_content)

    for section, commands in obj.items():
        print(section)
        print(commands)

    order = {
        "item": item,
        "quantity": qty,
        "price": price,
        "buyer": buyer,
        "date": date
    }

    obj['orders'].append(order)

    with open(data_dir+"/"+orders_file, 'w') as f_n:
        json.dump(obj, f_n, indent=4)


if __name__ == '__main__':
    write_order_to_json('Лактоцин №5', 5, 15, 'Мухин В.Н.', '2018-11-22 15:12:32')
    print()
