from typing import Optional

from pydantic import Field

from libs.tm_lib.models.base_model import BaseConfigModel

class Driver(BaseConfigModel):
    id:Optional[int] = Field(None,alias="driver_id")
    name:Optional[str] = Field(None,alias="name")
    balance:Optional[float] = Field(None,alias="balance")