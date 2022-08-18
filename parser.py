import re

import openpyxl

from files_names import contacts_file


def separate_num(words_list: list) -> tuple[dict, dict]:
    """
    Функция для разделения корпоративных и личных номеров телефона.

    Принимае список.

    Возвращает два списка person_phone и corp_phone. Именно в этом порядке
    """
    person_phone = []
    corp_phone = []
    # проходим по списку, ищем номера, отделяем корпоративный от личных
    for word in words_list:
        if not re.match('[\d]+', word):
            continue
        if (re.search('[личн]', word)
                and len(re.match('[\d]+', word).group(0)) == 11):
            person_phone.append(int(re.match('[\d]+', word).group(0)))
        elif (len(re.match('[\d]+', word).group(0)) == 4
                or len(re.match('[\d]+', word).group(0)) == 11):
            corp_phone.append(int(word))
    return person_phone, corp_phone


def contacts_parser(file_link: str) -> list:
    """
    Из файла парсим номер магазина, номер партии, телефоны
    Возвращает список словарей
    """
    contacts_book = openpyxl.load_workbook(file_link)
    worksheet = contacts_book.active
    shops_info_list = []
    for row in range(1, worksheet.max_row):
        shop_info = {}
        for col in worksheet.iter_cols(2, worksheet.max_column):
            match col[row].column:
                case 2:  # номер маршрута
                    num_shipment = re.findall('[0-9]+', str(col[row].value))
                    # преобразуем список строк в список int
                    num_shipment = [int(item) for item in num_shipment]
                    shop_info["num_shipment"] = num_shipment
                case 3:  # номер магазина
                    shop_info["num_shop"] = int(col[row].value)
                case 6:  # номера телефонов
                    if col[row].value:  # если ячейка не пустая
                        # разбираем ячейку на "слова", формируем список
                        words_list = re.findall('[\w]+', col[row].value)
                    person_phone, corp_phone = separate_num(words_list)
                    shop_info["phone_num"] = {}
                    shop_info["phone_num"]["person_num"] = person_phone
                    shop_info["phone_num"]["corp_num"] = corp_phone
        shops_info_list.append(shop_info)
    return shops_info_list


if __name__ == "__main__":
    for elem in contacts_parser(contacts_file):
        print(elem)
