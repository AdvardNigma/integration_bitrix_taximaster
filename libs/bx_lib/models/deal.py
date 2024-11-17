from typing import Optional

from pydantic import Field
from libs.bx_lib.models.base_model import BaseConfigModel


class Deal(BaseConfigModel):
    id:Optional[int] = Field(None,alias="ID")
    contact_id:Optional[int] = Field(None,alias="CONTACT_ID")