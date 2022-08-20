import re
from datetime import datetime
from types import NoneType

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


def alltimetable_parser() -> list:
    alltimetable_book = openpyxl.load_workbook("alltime.xlsx")
    worksheet = alltimetable_book.active
    shops_info_list = []
    for row in range(1, worksheet.max_row):
        shop_info = {}
        shop_info["main_info"] = {}  # словарь с основными данными о ммагазине
        shop_info["fiscal"] = {}  # словарь с данными о фискальном регистраторе
        for col in worksheet.iter_cols(2, worksheet.max_column):
            
            match col[row].column:               
                case 2:  # номер магазина
                    num = col[row].value  # проверяем есть ли данные в ячейке
                    if num:
                        shop_info["main_info"]["num_shop"] = re.search('[\d]+', num).group()
                    else:
                        shop_info["main_info"]["num_shop"] = None
                case 3:  # адрес магазина
                    shop_info["main_info"]["address"] = col[row].value
                case 4:  # статус магазина
                    shop_info["main_info"]["status"] = col[row].value
                case 5:  # юридическое лицо
                    shop_info["main_info"]["entity"] = col[row].value
                case 6:  # почтовый индекс
                    post_index = col[row].value
                    try:
                        shop_info["main_info"]["post_index"] = int(post_index)
                    except TypeError:
                        shop_info["main_info"]["post_index"] = None
                case 7:  # КПП
                    kpp = col[row].value
                    try:
                        shop_info["main_info"]["kpp"] = int(kpp)
                    except TypeError:
                        shop_info["main_info"]["kpp"] = None
                case 9:  # модель фискальника
                    fiscal_model = col[row].value
                    shop_info["fiscal"]["fiscal_model"] = fiscal_model
                case 10:  # имя в Такскоме
                    taxcom_name = col[row].value
                    shop_info["fiscal"]["taxcom_name"] = taxcom_name
                case 11:  # заводской номер ккт
                    fabric_num = col[row].value
                    try:
                        shop_info["fiscal"]["fabric_num"] = int(fabric_num)
                    except TypeError:
                        shop_info["fiscal"]["fabric_num"] = None
                case 12:  # регистрационный номер ккт
                    reg_num = col[row].value
                    try:
                        shop_info["fiscal"]["reg_num"] = int(reg_num)
                    except TypeError:
                        shop_info["fiscal"]["reg_num"] = None
                case 13:  # оплата в такскоме до
                    # taxcom_paid_up_raw = datetime(col[row].value)
                    # # date = re.match('[\d+\/d+\/d+]',taxcom_paid_up_raw).group(0)
                    # # try:
                    # #     str_to_date = datetime.strptime(date, '%m/%d/%Y')
                    # # except TypeError:
                    # #     shop_info["fiscal"]["taxcom_paid_up"] = None
                    # #     continue
                    # try:
                    #     taxcom_paid_up = taxcom_paid_up_raw.strftime('%d.%m.%Y')
                    # except TypeError:
                    #     taxcom_paid_up = None
                    # # taxcom_paid_up = str_to_date.strftime('%d.%m.%Y')
                    # shop_info["fiscal"]["taxcom_paid_up"] = taxcom_paid_up
                    pass

        shops_info_list.append(shop_info)
    return shops_info_list


if __name__ == "__main__":
    for elem in contacts_parser(contacts_file):
        print(elem)
    for e in alltimetable_parser():
        print(e, sep="\n")
