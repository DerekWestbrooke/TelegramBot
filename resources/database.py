import os
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    func,
    Float,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from resources.user_logger import create_local_logger
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from handlers.bot_functions_common import get_user_id_hash
from sqlalchemy.ext.asyncio import create_async_engine
from resources.values import POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD

user_logger = create_local_logger()

base = declarative_base()


class User(base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    user_name = Column(String, unique=True)
    chat_id = Column(Integer, unique=True)
    registered_time = Column(
        TIMESTAMP,
        server_default=func.now(),
    )
    notifications = relationship("Notification", back_populates="user")
    counters = relationship("Counter", back_populates="user")


class Notification(base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey("users.chat_id"), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    user = relationship("User", back_populates="notifications")


class Counter(base):
    __tablename__ = "counters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    electricity = Column(Float, nullable=True)
    warm_water = Column(Float, nullable=True)
    cold_water = Column(Float, nullable=True)
    registered_time = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="counters")


class KufarLocation(base):
    __tablename__ = "kufar_locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String, unique=True, nullable=False)


class Metadata(base):
    __tablename__ = "metadata"

    parameter = Column(String, primary_key=True)
    value = Column(String)


class DataBase:
    def __init__(self, db_name):
        self.table_list = {
            "users",
            "notifications",
            "counters",
            "kufar_locations",
            "metadata",
        }

        sync_connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
        async_connection_string = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"

        self.engine = create_engine(sync_connection_string, future=True)
        self.async_engine = create_async_engine(async_connection_string, future=True)

        self.session_maker = sessionmaker(bind=self.engine, future=True)
        self.async_session_maker = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            future=True,
        )

        base.metadata.create_all(self.engine)
        user_logger.info("БАЗА ДАННЫХ: таблицы созданы успешно")

    def insert_user(self, user_data):
        user_id_str, user_name, chat_id = user_data
        user_id_hash = get_user_id_hash(user_id_str)
        current_session = self.session_maker()
        try:
            does_exist = (
                current_session.query(User).filter_by(user_id=user_id_hash).first()
            )
            if not does_exist:
                user = User(user_id=user_id_hash, user_name=user_name, chat_id=chat_id)
                current_session.add(user)
                current_session.commit()
                user_logger.info(
                    "БАЗА ДАННЫХ: новый пользователь зарегистрирован успешно"
                )
            else:
                user_logger.info("БАЗА ДАННЫХ: пользователь уже существует")
        except SQLAlchemyError as e:
            current_session.rollback()
            user_logger.warning(
                f"БАЗА ДАННЫХ: ошибка при регистрации нового пользователя ({e})"
            )
        finally:
            current_session.close()

    def insert_notify(self, user_data):
        chat_id, start_time, end_time = user_data
        current_session = self.session_maker()
        try:
            notification = Notification(
                chat_id=chat_id, start_time=start_time, end_time=end_time
            )
            current_session.add(notification)
            current_session.commit()
            user_logger.info("БАЗА ДАННЫХ: данные для оповещения сохранены успешно")
        except SQLAlchemyError as e:
            current_session.rollback()
            user_logger.warning(
                f"БАЗА ДАННЫХ: ошибка сохранения данных для оповещения ({e})"
            )
        finally:
            current_session.close()

    def insert_kufar_values(self, data):
        current_session = self.session_maker()
        try:
            for location_name in data:
                location = (
                    current_session.query(KufarLocation)
                    .filter_by(location_name=location_name)
                    .first()
                )
                if not location:
                    current_session.add(KufarLocation(location_name=location_name))
                current_session.commit()
                self.insert_metadata()
                user_logger.info("БАЗА ДАННЫХ: метаданные сохранены успешно")

        except SQLAlchemyError as e:
            current_session.rollback()
            user_logger.warning(f"БАЗА ДАННЫХ: ошибка вставки метаданных ({e})")

        finally:
            current_session.close()

    def insert_metadata(self):
        session = self.session_maker()
        try:
            param = "kufar_last_location_update"
            value = datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

            metadata = session.query(Metadata).filter_by(parameter=param).first()
            if metadata:
                metadata.value = value
            else:
                metadata = Metadata(parameter=param, value=value)
                session.add(metadata)
            session.commit()
            user_logger.info("БАЗА ДАННЫХ: метаданные сохранены успешно")
        except SQLAlchemyError as e:
            session.rollback()
            user_logger.warning(f"БАЗА ДАННЫХ: ошибка вставки метаданных ({e})")
        finally:
            session.close()

    def delete_values(self, table_name):
        if not self.does_table_name_exist(table_name):
            user_logger.warning(f"БАЗА ДАННЫХ: {table_name} не существует")
            return
        session = self.session_maker()
        try:
            table_map = {
                "users": User,
                "notifications": Notification,
                "counters": Counter,
                "kufar_locations": KufarLocation,
                "metadata": Metadata,
            }
            model = table_map[table_name]
            session.query(model).delete()
            session.commit()
            user_logger.info(f"БАЗА ДАННЫХ: данные удалены из {table_name} успешно")
        except SQLAlchemyError as e:
            session.rollback()
            user_logger.warning(
                f"БАЗА ДАННЫХ: ошибка удаления данных из {table_name} ({e})"
            )
        finally:
            session.close()

    def select_data_from_table(self, table_name):
        if not self.does_table_name_exist(table_name):
            user_logger.warning(f"БАЗА ДАННЫХ: {table_name} не существует")
            return []

        session = self.session_maker()
        try:
            table_map = {
                "users": User,
                "notifications": Notification,
                "counters": Counter,
                "kufar_locations": KufarLocation,
                "metadata": Metadata,
            }
            model = table_map[table_name]
            results = session.query(model).all()
            user_logger.info(f"БАЗА ДАННЫХ: данные из {table_name} выгружены успешно")
            return results
        except SQLAlchemyError as e:
            user_logger.warning(
                f"БАЗА ДАННЫХ: ошибка выгрузки данных из {table_name} ({e})"
            )
            return []
        finally:
            session.close()

    def is_table_empty(self, table_name):
        if not self.does_table_name_exist(table_name):
            user_logger.warning(f"БАЗА ДАННЫХ: {table_name} не существует")
            return True
        session = self.session_maker()
        try:
            table_map = {
                "users": User,
                "notifications": Notification,
                "counters": Counter,
                "kufar_locations": KufarLocation,
                "metadata": Metadata,
            }
            model = table_map[table_name]
            count = session.query(model).count()
            user_logger.info(
                f"БАЗА ДАННЫХ: количество записей в {table_name} определено успешно"
            )
            return count == 0
        except SQLAlchemyError as e:
            user_logger.warning(
                f"БАЗА ДАННЫХ: ошибка подсчёта записей в {table_name} ({e})"
            )
            return True
        finally:
            session.close()

    def does_table_name_exist(self, table_name):
        exists = table_name in self.table_list
        user_logger.info(
            f"БАЗА ДАННЫХ: проверка существования таблицы {table_name} = {exists}"
        )
        return exists

    def select_counters(self, user_id_str):
        session = self.session_maker()
        user_id_hash = get_user_id_hash(user_id_str)
        try:
            counters = session.query(Counter).filter_by(user_id=user_id_hash).all()
            user_logger.info(f"БАЗА ДАННЫХ: данные счетчиков выгружены успешно")
            return counters
        except SQLAlchemyError as e:
            user_logger.warning(f"БАЗА ДАННЫХ: ошибка выгрузки счетчиков ({e})")
            return []
        finally:
            session.close()

    def insert_into_counters(self, data):
        user_id_str, electricity, warm_water, cold_water = data
        user_id_hash = get_user_id_hash(user_id_str)
        session = self.session_maker()
        try:
            count = session.query(Counter).filter_by(user_id=user_id_hash).count()
            if count >= 5:
                # Удаляем старую запись
                latest_record = (
                    session.query(Counter)
                    .filter_by(user_id=user_id_hash)
                    .order_by(Counter.registered_time.asc())
                    .first()
                )
                if latest_record:
                    session.delete(latest_record)

            new_counter = Counter(
                user_id=user_id_hash,
                electricity=electricity,
                warm_water=warm_water,
                cold_water=cold_water,
            )
            session.add(new_counter)
            session.commit()
            user_logger.info("БАЗА ДАННЫХ: данные счетчиков сохранены успешно")
        except SQLAlchemyError as e:
            session.rollback()
            user_logger.warning(f"БАЗА ДАННЫХ: ошибка сохранения счетчиков ({e})")
        finally:
            session.close()

    def delete_from_counters(self, data):
        user_id_str, electricity, warm_water, cold_water = data
        user_id_hash = get_user_id_hash(user_id_str)
        session = self.session_maker()
        try:
            counter_to_delete = (
                session.query(Counter)
                .filter_by(
                    user_id=user_id_hash,
                    electricity=electricity,
                    warm_water=warm_water,
                    cold_water=cold_water,
                )
                .first()
            )
            if counter_to_delete:
                session.delete(counter_to_delete)
                session.commit()
                user_logger.info("БАЗА ДАННЫХ: данные счетчиков удалены успешно")
            else:
                user_logger.warning("БАЗА ДАННЫХ: запись для удаления не найдена")
        except SQLAlchemyError as e:
            session.rollback()
            user_logger.warning(f"БАЗА ДАННЫХ: ошибка удаления счетчиков ({e})")
        finally:
            session.close()

    # Получение асинхронной сессии для расписания
    def get_async_session(self):
        return self.async_session_maker()
