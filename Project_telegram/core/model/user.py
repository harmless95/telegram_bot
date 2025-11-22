from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, Integer

from core.model.Base import BaseDB
from core.model.id_mixin import IdPrKey


class User(BaseDB, IdPrKey):
    name: Mapped[str] = mapped_column(String(50), default="Not name")
    id_telegram: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        nullable=False,
    )
