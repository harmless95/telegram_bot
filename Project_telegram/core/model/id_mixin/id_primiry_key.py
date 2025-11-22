import uuid
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUD

class IdPrKey:
    id: Mapped[UUID] = mapped_column(PG_UUD(as_uuid=True), primary_key=True, default=uuid.uuid4,)