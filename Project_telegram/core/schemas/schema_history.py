from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel

from .schemas_user import User


class HistorySchema(BaseModel):
    id_user: UUID
    user_history: Optional["User"]
    message_text: List[dict]
