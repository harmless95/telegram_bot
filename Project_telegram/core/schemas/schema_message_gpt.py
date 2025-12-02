from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Message(BaseModel):
    message_user: str
    user_id: UUID
    created_at: datetime
