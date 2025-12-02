from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, TIMESTAMP

from core.model import BaseDB
from core.model.id_mixin import IdPrKey

if TYPE_CHECKING:
    from core.model import User


class MessageGPT(BaseDB, IdPrKey):
    message_user: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(column="users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user_message: Mapped["User"] = relationship("User", back_populates="message_gpt")
