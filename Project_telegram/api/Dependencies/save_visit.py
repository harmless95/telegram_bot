from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.model import User


async def save_db_user(user_id: int, session: AsyncSession):
    stmt = select(User).where(User.id_telegram == user_id)
    result = await session.scalars(stmt)
    user = result.first()
    if not user:
        user = User(
            name="not name",
            id_telegram=user_id,
            created_at=datetime.now(tz=timezone.utc),
        )
        session.add(user)
    else:
        user.created_at = datetime.now(tz=timezone.utc)
    await session.commit()
    await session.refresh(user)
