from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class EntityInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    entity_name: str | None = None
    entity_inn: str | None = None
    """отношение с таблицей магазинов"""
    """
    комментарий для себя.
    нижеследующая конструкция ссылается на таблицу ShopInfo и поле entity в ней
    """
    shops: list["ShopInfo"] = Relationship(back_populates="entity")


class ShopInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shop_num: int | None = None
    shop_address: str | None = None
    shop_shipment: str | None = None
    shop_status: bool | None = None
    shop_kpp: int | None = None
    cigarettes: bool | None
    shop_phone_person: str | None = None
    shop_phone_corp: str | None = None
    egais_avaliable: bool | None = None
    egais_fsrar_id: str | None = None
    egais_gost_key_end_date: datetime | None = None
    egais_rsa_key_end_date: datetime | None = None
    """отношение с таблицей юрлиц"""
    entity_id: int = Field(default=None, foreign_key="entityinfo.id")
    """
    комментарий для себя.
    нижеследующая конструкция ссылается на таблицу EntityInfo и поле shops в ней
    """
    entity: EntityInfo = Relationship(back_populates="shops")
    """отношение с таблицей АРМ"""
    arm: list["ArmInfo"] = Relationship(back_populates="shop")
    """отношение с таблицей фискальников"""
    fiscal: list["FiscalInfo"] = Relationship(back_populates="shop")


class ArmInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    arm_comp: str | None = None
    arm_os: str | None = None
    arm_shtrih_ver: str | None = None
    arm_pos_num: int | None = None
    arm_permit: bool | None = None
    """отношение с таблицей магазинов"""
    shop_id: int = Field(default=None, foreign_key="shopinfo.id")
    shop: ShopInfo = Relationship(back_populates="arm")


class FiscalInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    fiscal_model: str | None = None
    fiscal_fabric_num: str | None = None
    fiscal_reg_num: str | None = None
    fiscal_taxcom_name: str | None = None
    fiscal_taxcom_end_date: datetime | None = None
    fiscal_fn_num: str | None = None
    fiscal_fn_period: int | None = None
    fiscal_fn_end_day: datetime | None = None
    """отнощение с таблицей магазинов"""
    shop_id: int = Field(default=None, foreign_key="shopinfo.id")
    shop: ShopInfo = Relationship(back_populates="fiscal")
