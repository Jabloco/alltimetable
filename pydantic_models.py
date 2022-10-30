from datetime import datetime

from pydantic import BaseModel


class PhoneNum(BaseModel):
    person_num: list[str] | None = None
    corp_num: list[str] | None = None


class MainData(BaseModel):
    shop_num: int | None = None
    shop_shipment_num: list[int] | None = None
    shop_post_index: int | None = None
    shop_address: str | None = None
    shop_phone_num: PhoneNum | None
    shop_kpp: int | None = None
    shop_entity: str | None = None
    shop_entity_inn: str | None = None
    shop_cigarettes: bool | None = None
    shop_status: bool | None = None


class FiscalData(BaseModel):
    fiscal_model: str | None = None
    fiscal_fabric_num: str | None = None
    fiscal_reg_num: str | None = None
    fascal_taxcom_name: str | None = None
    fiscal_taxcom_end_date: datetime | None = None
    fiscal_fn_num: str | None = None
    fiscal_fn_period: int | None = None
    fiscal_fn_end_day: datetime | None = None


class DevicesData(BaseModel):
    arm_comp: str | None = None
    arm_os: str | None = None
    arm_shtrih_ver: str | None = None
    arm_pos_num: int | None = None
    arm_permit: bool | None = None


class EgaisData(BaseModel):
    egais_avaliable: bool | None = None
    egais_fsrar_id: str | None = None
    egais_gost_key_end_date: datetime | None = None
    egais_rsa_key_end_date: datetime | None = None


class ShopData(BaseModel):
    main_info: MainData
    fiscal_info: FiscalData | None = None
    devices_info: DevicesData | None = None
    egais_info: EgaisData | None = None


class AllShopsInfo(BaseModel):
    shops: list[ShopData]
