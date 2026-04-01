from sqlmodel import SQLModel, Session, create_engine
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True) # echo для отладки, чтобы запросы в консоль выписывались

def init_db():
    SQLModel.metadata.create_all(engine) # создание таблиц

"""
            ЗАМЕТКА:
            Таблицы в атрибуте metadata появляются при создании модели таблицы,
            если указать параметр table=true
            ВСЕ ЭТО ПРОИСХОДИТ ПОД КАПОТОМ SQLModel
"""