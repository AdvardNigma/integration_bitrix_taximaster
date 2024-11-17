from typing import Optional

from pydantic import Field

from libs.bx_lib.models.base_model import BaseConfigModel


class Contact(BaseConfigModel):
    id:Optional[int] = Field(None,alias="ID")
    tm_id:Optional[int] = Field(None,alias="UF_CRM_1727700536348")
    balance:Optional[float] = Field(None,alias="UF_CRM_1729781383")