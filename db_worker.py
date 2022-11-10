from sqlmodel import Session, create_engine, select
from settings import db_host, db_user, db_pass, db_name


from models import EntityInfo
from models import ShopInfo
from models import ArmInfo
from models import FiscalInfo
from pydantic_models import ShopData


db_url = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
engine = create_engine(db_url)


def is_data_in_db(model_in_db, **kwarg):
    """
    функция для определения есть ли в БД входящий набор данных

    если данные есть возвращает True
    """
    with Session(engine) as session:
        statement = select(model_in_db).where(**kwarg)
        result = session.exec(statement)
        if result:
            return result, True

    return None, None


def write_to_db(raw_json):
    """
    функция для записи данных в БД

    на вход принимает json из модели pydentic
    """
    shop_info = ShopData.parse_raw(raw_json)
    with Session(engine) as session:
        if shop_info.main_info.shop_entity or shop_info.main_info.shop_entity_inn:
            entity_info = EntityInfo(
                entity_name=shop_info.main_info.shop_entity,
                entity_inn=shop_info.main_info.shop_entity_inn
            )
        else:
            entity_info = None

        shop_main_info = ShopInfo(
            shop_num=shop_info.main_info.shop_num,
            shop_address=str(shop_info.main_info.shop_post_index) + ', ' + shop_info.main_info.shop_address,
            shop_shipment=' '.join(list(map(str, shop_info.main_info.shop_shipment_num))),
            shop_status=shop_info.main_info.shop_status,
            shop_kpp=shop_info.main_info.shop_kpp,
            cigarettes=shop_info.main_info.shop_cigarettes,
            shop_phone_person=' '.join(shop_info.main_info.shop_phone_num.person_num),
            shop_phone_corp=' '.join(shop_info.main_info.shop_phone_num.corp_num),
            egais_avaliable=shop_info.egais_info.egais_avaliable,
            egais_fsrar_id=shop_info.egais_info.egais_fsrar_id,
            egais_gost_key_end_date=shop_info.egais_info.egais_gost_key_end_date,
            egais_rsa_key_end_date=shop_info.egais_info.egais_rsa_key_end_date,
            entity=entity_info
        )


        if (shop_info.devices_info.arm_comp
                or shop_info.devices_info.arm_os
                or shop_info.devices_info.arm_shtrih_ver
                or shop_info.devices_info.arm_pos_num
                or shop_info.devices_info.arm_permit):
            arm_info = ArmInfo(
                arm_comp=shop_info.devices_info.arm_comp,
                arm_os=shop_info.devices_info.arm_os,
                arm_shtrih_ver=shop_info.devices_info.arm_shtrih_ver,
                arm_pos_num=shop_info.devices_info.arm_pos_num,
                arm_permit=shop_info.devices_info.arm_permit,
                shop=shop_main_info
            )
        else:
            arm_info = None

        if (shop_info.fiscal_info.fiscal_model
                or shop_info.fiscal_info.fiscal_fabric_num
                or shop_info.fiscal_info.fiscal_reg_num
                or shop_info.fiscal_info.fascal_taxcom_name
                or shop_info.fiscal_info.fiscal_taxcom_end_date
                or shop_info.fiscal_info.fiscal_fn_num
                or shop_info.fiscal_info.fiscal_fn_period
                or shop_info.fiscal_info.fiscal_fn_end_day):
            fiscal_info = FiscalInfo(
                fiscal_model=shop_info.fiscal_info.fiscal_model,
                fiscal_fabric_num=shop_info.fiscal_info.fiscal_fabric_num,
                fiscal_reg_num=shop_info.fiscal_info.fiscal_reg_num,
                fiscal_taxcom_name=shop_info.fiscal_info.fascal_taxcom_name,
                fiscal_taxcom_end_date=shop_info.fiscal_info.fiscal_taxcom_end_date,
                fiscal_fn_num=shop_info.fiscal_info.fiscal_fn_num,
                fiscal_fn_period=shop_info.fiscal_info.fiscal_fn_period,
                fiscal_fn_end_day=shop_info.fiscal_info.fiscal_fn_end_day,
                shop=shop_main_info
            )
        else:
            fiscal_info = None

        session.add(shop_main_info)
        if entity_info:
            session.add(entity_info)
        if arm_info:
            session.add(arm_info)
        if fiscal_info:
            session.add(fiscal_info)
        session.commit()


def read_from_db():
    pass


if __name__ == "__main__":
    # мокап json для проверки
    input_json = """
    {
        "main_info":
        {
            "shop_num": 2,
            "shop_shipment_num": [11],
            "shop_post_index": 600000,
            "shop_address": "Розы Л ул, дом № 00",
            "shop_phone_num":
                {
                "person_num": [89120000000, 89090000000],
                "corp_num": [89220000000]
                },
            "shop_kpp": 400000000,
            "shop_entity": null,
            "shop_entity_inn": null,
            "shop_cigarettes": false,
            "shop_status": true
        },
        "fiscal_info":
            {
                "fiscal_model": "РИТЕЙЛ",
                "fiscal_fabric_num": "0000000000000995",
                "fiscal_reg_num": "0000000000048029",
                "fascal_taxcom_name": "Магазин №2_ККТ1",
                "fiscal_taxcom_end_date": "2019-01-29T00:00:00",
                "fiscal_fn_num": "0000000000410052",
                "fiscal_fn_period": 13,
                "fiscal_fn_end_day": "2018-11-06T00:00:00"
            },
        "devices_info":
            {
                "arm_comp": null,
                "arm_os": null,
                "arm_shtrih_ver": null,
                "arm_pos_num": 46,
                "arm_permit": false
            },
        "egais_info":
            {
                "egais_avaliable": true,
                "egais_fsrar_id": "0000000000068",
                "egais_gost_key_end_date": "2019-06-22T00:00:00",
                "egais_rsa_key_end_date": null
            }
    }
    """

    write_to_db(input_json)
