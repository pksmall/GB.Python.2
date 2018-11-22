# L02 task #1

import csv
import glob
import re

'''
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. 
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров 
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в 
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, 
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в 
него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных 
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
'''
data_dir = 'data'
main_file = '/main_data_'


def get_data():
    file_list = glob.iglob(data_dir+"/*.txt")
    idx = 1
    for file_name in file_list:
        main_data = []
        s_prod_list = []
        os_name_list = []
        os_code_list = []
        os_type_list = []
        tmp_list = []
        header = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
        with open(file_name, encoding="windows-1251") as fn:
            for line_str in fn:
                # print(str(line_str))
                match = re.search(r"Изготовитель системы:\s+(.+)", line_str, re.IGNORECASE)
                if match:
                    s_prod_list.append(match.group(1))
                match = re.search(r"Название ОС:\s+(.+)", str(line_str), re.IGNORECASE)
                if match:
                    os_name_list.append(match.group(1))
                match = re.search(r"Код продукта:\s+(.+)", str(line_str), re.IGNORECASE)
                if match:
                    os_code_list.append(match.group(1))
                match = re.search(r"Тип системы:\s+(.+)", str(line_str), re.IGNORECASE)
                if match:
                    os_type_list.append(match.group(1))
        tmp_list.append(''.join(s_prod_list))
        tmp_list.append(''.join(os_name_list))
        tmp_list.append(''.join(os_code_list))
        tmp_list.append(''.join(os_type_list))
        main_data.append(header)
        main_data.append(tmp_list)
        print(main_data)
        with open(data_dir+main_file+str(idx)+'.csv', 'w', encoding='utf-8') as f_n:
            f_n_writer = csv.writer(f_n, quoting=csv.QUOTE_ALL)
            f_n_writer.writerows(main_data)
        idx += 1


def write_to_csv():
    file_list = glob.iglob(data_dir + "/*.csv")
    head_flag = True
    for file_name in file_list:
        print(file_name)
        with open(file_name, encoding="utf-8") as fn, open("./"+main_file+"all.csv", "a+") as of:
            fnr = csv.DictReader(fn)
            writer = csv.writer(of, quoting=csv.QUOTE_ALL)
            for row in fnr:
                if head_flag:
                    writer.writerow(row)
                    head_flag = False
                writer.writerow([row['Изготовитель системы'], row['Название ОС'], row['Код продукта'], row['Тип системы']])


if __name__ == '__main__':
    get_data()
    write_to_csv()
    print()
