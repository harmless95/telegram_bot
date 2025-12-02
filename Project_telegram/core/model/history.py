from typing import TYPE_CHECKING, List
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, JSON

from core.model import BaseDB
from core.model.id_mixin import IdPrKey

if TYPE_CHECKING:
    from core.model import User


class HistoryMessage(BaseDB, IdPrKey):
    id_user: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    user_history: Mapped["User"] = relationship(
        "User", back_populates="message_history"
    )
    message_text: Mapped[List[dict]] = mapped_column(JSON)
