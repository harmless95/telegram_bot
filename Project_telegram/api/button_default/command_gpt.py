from datetime import datetime, timezone
import logging

from aiogram.types import Message
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.text_gpt.client_gpt import conn_client
from core.model import User, HistoryMessage


logger = logging.getLogger(__name__)


async def get_user_id_tg(user_id: int, session: AsyncSession):
    stmt = select(User).where(User.id_telegram == user_id)
    result = await session.scalars(stmt)
    user = result.first()
    if not user:
        user = User(
            name="not name",
            created_at=datetime.now(tz=timezone.utc),
            id_telegram=user_id,
            chat_disabled=1,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def command_hand(message: Message, session: AsyncSession):
    """Включает чат с AI"""
    user_id = message.from_user.id
    user = await get_user_id_tg(
        user_id=user_id, session=session
    )  # Правильная транзакция
    if user.chat_disabled == 1:  # Был отключён, теперь включаем
        stmt = update(User).where(User.id_telegram == user_id).values(chat_disabled=0)
        await session.execute(stmt)
        await session.commit()
        await message.answer("✅ AI чат включён!")
    else:  # Уже активен
        await message.answer(
            "🤖 Groq AI готов! Пиши любой вопрос.\n🛑 /stop_ai — остановить чат"
        )


async def command_stop(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    user = await get_user_id_tg(user_id=user_id, session=session)
    if user.chat_disabled == 0:  # Активен — отключаем
        stmt = update(User).where(User.id_telegram == user_id).values(chat_disabled=1)
        await session.execute(stmt)
        await session.commit()
        await message.answer("🛑 AI чат остановлен.\n🔄 /start_ai — включить снова")
    else:
        await message.answer("🤖 Чат уже остановлен.\n🔄 /start_ai — включить чат")


async def message_sent(message: Message, session: AsyncSession):
    """Обработка текстовых сообщений с AI"""
    user_id = message.from_user.id
    client = await conn_client()

    user = await get_user_id_tg(user_id=user_id, session=session)
    if user.chat_disabled == 1:
        return
    stmt = select(HistoryMessage).where(HistoryMessage.id_user == user.id)
    result = await session.scalars(stmt)
    user_hist = result.first()
    if not user_hist:
        user_hist = HistoryMessage(
            id_user=user.id,
            message_text=[
                {
                    "role": "system",
                    "content": "Ты полезный ассистент. Отвечай кратко и по делу на русском.",
                },
            ],
        )

        session.add(user_hist)
        await session.commit()

    user_hist.message_text.append({"role": "user", "content": message.text})
    await session.flush()
    await session.commit()
    await message.answer("🤔 Думаю...")
    await ai_message(
        client=client, user_hist=user_hist, session=session, message=message
    )


async def ai_message(
    client, user_hist: HistoryMessage, session: AsyncSession, message: Message
):
    try:
        if not client:
            raise Exception("Groq клиент не инициализирован")
        last_messages = user_hist.message_text[-10:]
        chat_completion = client.chat.completions.create(
            messages=last_messages,  # Последние 10 сообщений
            model="llama-3.1-8b-instant",  # ✅ АКТУАЛЬНАЯ модель
            max_tokens=500,
            temperature=0.7,
        )

        response = chat_completion.choices[0].message.content
        user_hist.message_text.append({"role": "assistant", "content": response})

        session.add(user_hist)  # Обновляем объект
        await session.commit()

        await message.answer(response)

    except Exception as e:
        logger.error(f"Groq ошибка: {e}", exc_info=True)
        await message.answer(f"❌ Ошибка AI: {str(e)[:100]}...")
