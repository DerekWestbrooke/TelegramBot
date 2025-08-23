import datetime
import os
from datetime import timedelta

import aiosqlite
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from resources.bot import bot
from resources.bot_keyboards import communal_main_menu_button
from resources.user_logger import create_local_logger
from resources.values import db_name, message_payment_time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, delete
from datetime import datetime, timedelta
from resources.database import Notification
from resources.bot import db

user_logger = create_local_logger()


# Функция мониторинга указанного пользователем периода времени для оповещения
async def notifications_monitoring(async_session_maker):
    datetime_now = datetime.now().replace(microsecond=0)
    async with async_session_maker() as session:
        result = await session.execute(
            select(Notification).where(
                and_(
                    Notification.start_time <= datetime_now,
                    Notification.end_time >= datetime_now,
                )
            )
        )
        notifications = result.scalars().all()

        for notif in notifications:
            chat_id = notif.chat_id
            start_time = notif.start_time
            end_time = notif.end_time
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=message_payment_time,
                    reply_markup=communal_main_menu_button(),
                )
            except Exception as e:
                user_logger.info(
                    f"РАСПИСАНИЕ: Ошибка при отправке напоминании пользователю (chat: {chat_id}): {e}"
                )

            if start_time - end_time == timedelta(minutes=1):
                await session.execute(
                    delete(Notification).where(Notification.id == notif.id)
                )
            else:
                notif.start_time = start_time + timedelta(days=1)
            await session.commit()
            user_logger.info(f"РАСПИСАНИЕ: напоминание отправлено (chat: {chat_id})")


def start_notifications_monitoring():
    scheduler.add_job(
        notifications_monitoring, "interval", minutes=1, args=[db.async_session_maker]
    )
    scheduler.start()


scheduler = AsyncIOScheduler()
