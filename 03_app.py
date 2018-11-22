# L02 task #3

import yaml

'''
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, 
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке 
ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с 
помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''

data_dir = 'data'
main_file = '/file.yaml'

if __name__ == '__main__':
    first_list = ['l1', 'l2', 'l3']

    dict_list = {374: 'Ŷ', 1269: 'ӵ', 1176: 'Ҙ'}

    data_to_yaml = {'list': first_list, 'number': 182619, 'dist': dict_list}

    with open(data_dir+"/"+main_file, 'w') as f_n:
        yaml.dump(data_to_yaml, f_n, default_flow_style=False, allow_unicode=True)

    with open(data_dir+"/"+main_file) as f_n:
        print(f_n.read())

    print()
