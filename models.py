from datetime import datetime

from sqlmodel import Field, SQLModel


class ShopInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shop_num: int | None = None
    shop_address: str | None = None
    shop_status: bool | None = None
    shop_entity: str | None = None
    shop_kpp: int | None = None
    cigarettes: bool | None


class EntityInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    entity_name: str | None = None
    entity_inn: str | None = None


class ArmInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shop_num: int | None = None
    arm_comp: str | None = None
    arm_os: str | None = None
    arm_shtrih_ver: str | None = None
    arm_pos_num: int | None = None
    arm_permit: bool | None = None


class FiscalInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shop_num: int | None = None
    fiscal_model: str | None = None
    fiscal_fabric_num: str | None = None
    fiscal_reg_num: str | None = None
    fascal_taxcom_name: str | None = None
    fiscal_taxcom_end_date: datetime | None = None
    fiscal_fn_num: str | None = None
    fiscal_fn_period: int | None = None
    fiscal_fn_end_day: datetime | None = None
