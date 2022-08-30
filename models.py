import typing

from typing import Optional

from sqlmodel import Field, SQLModel


class MainInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shop_num: int
    shop_address: Optional[str] = None
    shop_status: Optional[bool] = None
    shop_entity: Optional[str] = None
    shop_kpp: Optional[int] = None
    cigarettes: bool