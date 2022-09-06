import re
from datetime import datetime

import openpyxl
from pydantic import BaseModel
from pydantic import ValidationError

from files_names import contacts_file
from files_names import monitoring_file
from files_names import alltime_file


class PhoneNum(BaseModel):
    person_num: list[int] | None = None
    corp_num: list[int] | None = None


class ShopInfo(BaseModel):
    shop_num: int | None = None
    num_shipment: list[int] | None = None
    phone_num: PhoneNum | None


class AllShopInfo(BaseModel):
    all_shop_info: list[ShopInfo]


def separate_num(words_list: list) -> tuple[list, list]:
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


def is_date(cell_data) -> datetime | None:
    """
    Функция для определения что данные в ячейке есть дата

    Возвращает datetime
    """
    if isinstance(cell_data, datetime):
        return cell_data
    else:
        return None


def shop_num(cell_data) -> int | None:
    try:
        if re.match('(маг[ ]+№|магазин[ ]+№)[\d]+', cell_data, re.IGNORECASE).group(0):
            return int(re.search('[\d]+', cell_data).group())
    except TypeError:
        return None
    except AttributeError:
        return None


def is_kkt_num(cell_data) -> str | None:
    """
    Функция для определения являются ли данные в ячейке каким либо номером кассы
    
    Заводской номер и рег.номер ККТ имеют одинаковую длину.

    Что это будет за номер зависит только от столбца
    """
    try:
        return re.match('[\d]{16}', cell_data).group(0)
    except TypeError:
        return None
    except AttributeError:
        return None


def contacts_parser(file_link: str) -> AllShopInfo:
    """
    Из файла парсим номер магазина, номер партии, телефоны
    Возвращает список словарей
    """
    contacts_book = openpyxl.load_workbook(file_link)
    worksheet = contacts_book.active
    all_shop = []
    for row in range(1, worksheet.max_row):
        for col in worksheet.iter_cols(2, worksheet.max_column):
            match col[row].column:
                case 2:  # номер маршрута
                    num_shipment_raw = re.findall('[0-9]+', str(col[row].value))
                case 3:  # номер магазина
                    shop_num_raw = col[row].value
                case 6:  # номера телефонов
                    if col[row].value:  # если ячейка не пустая
                        # разбираем ячейку на "слова", формируем список
                        words_list = re.findall('[\w]+', col[row].value)
                    person_phone, corp_phone = separate_num(words_list)
                    try:
                        phones = PhoneNum(person_num=person_phone, corp_num=corp_phone)
                    except ValidationError as e:
                        print(e.json())
        try:
            shop = ShopInfo(
                num_shipment=num_shipment_raw,
                shop_num=shop_num_raw,
                phone_num=phones
            )
        except ValidationError as e:
            print(e.json())
        all_shop.append(shop)
    return AllShopInfo(all_shop_info=all_shop)


def alltimetable_parser(file_link) -> list:
    alltimetable_book = openpyxl.load_workbook(file_link)
    worksheet = alltimetable_book.active
    shops_info_list = []
    for row in range(1, worksheet.max_row):
        shop_info = {}
        shop_info["main_info"] = {}  # словарь с основными данными о магазине
        shop_info["fiscal"] = {}  # словарь с данными о фискальном регистраторе
        shop_info["devices"] = {}  # словарь с данными об оборудованиии на кассе
        shop_info["egais"] = {}
        for col in worksheet.iter_cols(2, worksheet.max_column):
            match col[row].column:
                case 2:  # номер магазина
                    num = col[row].value
                    shop_info["main_info"]["num_shop"] = shop_num(num)
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
                    shop_info["fiscal"]["fabric_num"] = is_kkt_num(col[row].value)
                case 12:  # регистрационный номер ккт
                    shop_info["fiscal"]["reg_num"] = is_kkt_num(col[row].value)
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
                case 20:  # срок RSA ключа
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


def monitoring_parser(file_link: str) -> list:
    monitoring_book = openpyxl.load_workbook(file_link)
    worksheet = monitoring_book.active
    monitoring_shop_info_list = []
    for row in range(18, worksheet.max_row):
        shop_info = {}
        shop_info["main_info"] = {}  # словарь с основными данными о магазине
        shop_info["fiscal"] = {}  # словарь с данными о фискальном регистраторе
        for col in worksheet.iter_cols(3, 16):
            match col[row].column:
                case 3:
                    shop_info["main_info"]["shop_num"] = shop_num(col[row].value)
                case 5:
                    shop_info["main_info"]["shop_address"] = col[row].value
                case 6:
                    shop_info["main_info"]["ofd_kkt_name"] = col[row].value
                case 7:
                    shop_info["fiscal"]["kkt_reg_num"] = is_kkt_num(col[row].value)
                case 8:
                    shop_info["fiscal"]["kkt_fabric_num"] = is_kkt_num(col[row].value)
        monitoring_shop_info_list.append(shop_info)
    return monitoring_shop_info_list


if __name__ == "__main__":
    print(contacts_parser(contacts_file).json())
    # for elem in contacts_parser(contacts_file):
    #     print(elem)
    # for e in alltimetable_parser(alltime_file):
    #     print(e, sep="\n")
    # for el in monitoring_parser(monitoring_file):
    #     print(el, sep="\n")
