import re
from datetime import datetime

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

def find_yes(cell_data) -> bool:
    """
    Функция для нахождения ДА в ячейке.

    Возвращает True или False.
    """
    try:
        if re.match('(да)', cell_data, re.IGNORECASE).group(0):
            is_yes = True
    except AttributeError:
        is_yes = False
    except TypeError:
        is_yes = False
    return is_yes

def is_date(cell_data) -> datetime:
    """
    Функция для определения что данные в ячейке есть дата

    Возвращает datetime
    """
    if isinstance(cell_data, datetime):
        return cell_data
    else:
        return None


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
        shop_info["devices"] = {}  # словарь с данными об оборудованиии на кассе
        shop_info["egais"] = {}
        for col in worksheet.iter_cols(2, worksheet.max_column):    
            match col[row].column:               
                case 2:  # номер магазина
                    num = col[row].value
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
                    if fabric_num:
                        shop_info["fiscal"]["fabric_num"] = fabric_num
                    else:
                        shop_info["fiscal"]["fabric_num"] = None
                case 12:  # регистрационный номер ккт
                    reg_num = col[row].value
                    if reg_num:
                        shop_info["fiscal"]["reg_num"] = reg_num
                    else:
                        shop_info["fiscal"]["reg_num"] = None
                case 13:  # оплата в такскоме до
                    taxcom_date = col[row].value
                    shop_info["fiscal"]["taxcom_end_date"] = is_date(taxcom_date)
                case 14:  # номер фн
                    fn_num = col[row].value
                    if fn_num:
                        shop_info["fiscal"]["fn_num"] = fn_num
                    else:
                        shop_info["fiscal"]["fn_num"] = None
                case 15:  # дата окончания фн
                    fn_end_date = col[row].value
                    shop_info["fiscal"]["fn_end_date"] = is_date(fn_end_date)
                case 16:  # срок фн
                    fn_period_raw = col[row].value
                    if fn_period_raw:
                        fn_period = re.search('(13|15|36) месяцев', fn_period_raw).group(0)
                    else:
                        fn_period = None
                    shop_info["fiscal"]["fn_period"] = fn_period
                case 17:  # тип компьютера на кассе
                    kkt_hardware = col[row].value
                    if kkt_hardware:
                        shop_info["devices"]["kkt_comp"] = kkt_hardware
                    else:
                        shop_info["devices"]["kkt_comp"] = None
                case 18:   # наличие ЕГАИС
                    is_egais = col[row].value
                    shop_info["egais"]["avaliable"] = find_yes(is_egais)
                case 19:  # срок ГОСТ ключа
                    gost_key_date = col[row].value
                    shop_info["egais"]["gost_key_date"] = is_date(gost_key_date)
                case 20:  #  срок RSA ключа
                    rsa_key_date = col[row].value
                    shop_info["egais"]["rsa_key_date"] = is_date(rsa_key_date)
                case 21:  # fsrar id
                    fsrar_id = col[row].value
                    if fsrar_id:
                        shop_info["egais"]["fsrar_id"] = fsrar_id
                    else:
                        shop_info["egais"]["fsrar_id"] = None
                case 22:  # ОС на кассе
                    kkt_os = col[row].value
                    shop_info["devices"]["kkt_os"] = kkt_os
                case 23:  # логический номер терминала
                    logic_pos_num = col[row].value
                    try:
                        shop_info["devices"]["logic_pos_num"] = int(logic_pos_num)
                    except TypeError:
                        shop_info["devices"]["logic_pos_num"] = None
                case 24:
                    pass
                case 25:  # версия кассира
                    shtrih_ver_raw = col[row].value
                    try:
                        shtrih_ver = re.search('(\d.\d.\d.\d)', shtrih_ver_raw).group(0)
                    except AttributeError:
                        shtrih_ver = None
                    except TypeError:
                        shtrih_ver = None
                    shop_info["devices"]["shtrih_ver"] = shtrih_ver
                case 26:  # сигареты
                    cigarettes_raw = col[row].value
                    cigarettes = find_yes(cigarettes_raw)
                    shop_info["main_info"]["cigarettes"] = cigarettes
                case 27:  # считыватель пропусков
                    permit_raw = col[row].value
                    permit = find_yes(permit_raw)
                    shop_info["devices"]["permit"] = permit
        shops_info_list.append(shop_info)
    return shops_info_list


if __name__ == "__main__":
    for elem in contacts_parser(contacts_file):
        print(elem)
    for e in alltimetable_parser():
        print(e, sep="\n")
