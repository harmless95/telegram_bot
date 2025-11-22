from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: UUID
    name: str
    id_telegram: int

    model_config = ConfigDict(from_attributes=True)


class ReadUser(User):
    created_at: datetime
