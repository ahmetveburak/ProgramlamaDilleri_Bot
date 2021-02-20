from typing import List
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.engine import base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import JSON
from sqlalchemy.types import (
    BigInteger,
    Boolean,
    String,
    Integer,
    DateTime,
    ARRAY,
    Float,
)
from sqlalchemy.orm import sessionmaker, relationship
from configparser import ConfigParser, SectionProxy
from datetime import datetime

sqlconfig: ConfigParser = ConfigParser()
sqlconfig.read("sql.ini")
csql: SectionProxy = sqlconfig["SQLSETTINGS"]

ConnectionString = f"{csql['DB_ENGINE']}://{csql['DB_USERNAME']}:{csql['DB_PASSWORD']}@{csql['DB_ADRESSES']}:{csql['DB_PORT']}/{csql['DB_DATABASE']}"
DbEngine = create_engine(ConnectionString)
Base: declarative_base = declarative_base()


class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    path = Column(String(100), nullable=False)
    authors = Column(ARRAY(String(100)), nullable=False)
    tags = Column(ARRAY(String(15)), nullable=False)
    note = Column(String(300), nullable=False)
    enabled = Column(Boolean, nullable=False)
    rating = Column(Float, default=0.5)
    file_id = Column(String(100), nullable=False)

    # userteatables = relationship("UserTeaTable")

    def __init__(
        self,
        name: str,
        path: str,
        authors: list,
        tags: list,
        note: str,
        enabled: bool,
        rating: float,
        file_id: str,
    ) -> None:
        self.name = name
        self.path = path
        self.authors = authors
        self.tags = tags
        self.note = note
        self.enabled = enabled
        self.rating = rating
        self.file_id = file_id


class Links(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    path = Column(String(100), nullable=False)
    authors = Column(ARRAY(String(100)), nullable=False)
    tags = Column(ARRAY(String(15)), nullable=False)
    note = Column(String(300), nullable=False)
    enabled = Column(Boolean, nullable=False)
    rating = Column(Float, default=0.5)

    # userteatables = relationship("UserTeaTable")

    def __init__(
        self,
        name: str,
        path: str,
        authors: list,
        tags: list,
        note: str,
        enabled: bool,
        rating: float,
    ) -> None:
        self.name = name
        self.path = path
        self.authors = authors
        self.tags = tags
        self.note = note
        self.enabled = enabled
        self.rating = rating


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(100), nullable=False)
    authors = Column(ARRAY(String(100)), nullable=False)
    tags = Column(ARRAY(String(15)), nullable=False)
    note = Column(String(300), nullable=False)
    enabled = Column(Boolean, nullable=False)
    rating = Column(Float, default=0.5)

    def __init__(
        self,
        name: str,
        authors: list,
        tags: list,
        note: str,
        enabled: bool,
        rating: float,
    ) -> None:
        self.name = name
        self.authors = authors
        self.tags = tags
        self.note = note
        self.enabled = enabled
        self.rating = rating


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(100), nullable=False)
    first_name = Column(ARRAY(String(70)))
    last_name = Column(ARRAY(String(70)))
    username = Column(ARRAY(String(40)))
    history = Column(JSON, nullable=False)

    def __init__(
        self, uid: int, first_name: str, last_name: str, username: str, history: JSON
    ) -> None:
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.history = history


# class Questions(Base):
#     __tablename__ = "questions"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     question = Column(JSON, nullable=False)

#     def __init__(self, question: JSON) -> None:
#         self.question = question


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    p_lang = Column(JSON, nullable=False)
    level = Column(JSON, nullable=False)
    lang = Column(JSON, nullable=False)
    resources = Column(JSON, nullable=False)

    def __init__(self, p_lang: JSON, level: JSON, lang: JSON, resources: JSON) -> None:
        self.p_lang = p_lang
        self.level = level
        self.lang = lang
        self.resources = resources


Documents.__table__.create(bind=DbEngine, checkfirst=True)
Links.__table__.create(bind=DbEngine, checkfirst=True)
Books.__table__.create(bind=DbEngine, checkfirst=True)
Users.__table__.create(bind=DbEngine, checkfirst=True)
Questions.__table__.create(bind=DbEngine, checkfirst=True)


Session: sessionmaker = sessionmaker(DbEngine)
session = Session()