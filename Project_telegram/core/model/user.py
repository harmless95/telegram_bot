from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, BigInteger, Integer

from core.model import BaseDB
from core.model.id_mixin import IdPrKey

if TYPE_CHECKING:
    from core.model import MessageGPT
    from core.model import HistoryMessage


class User(BaseDB, IdPrKey):
    name: Mapped[str] = mapped_column(String(50), default="Not name")
    id_telegram: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        nullable=False,
    )

    chat_disabled: Mapped[int] = mapped_column(Integer, default=1)

    message_gpt: Mapped["MessageGPT"] = relationship(
        "MessageGPT", back_populates="user_message"
    )
    message_history: Mapped["HistoryMessage"] = relationship(
        "HistoryMessage", back_populates="user_history"
    )
