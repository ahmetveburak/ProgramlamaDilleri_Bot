from sqlalchemy import create_engine, Column, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import JSON
from sqlalchemy.types import Boolean, String, Integer, DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship
from configparser import ConfigParser, SectionProxy
from datetime import datetime

sqlconfig: ConfigParser = ConfigParser()
sqlconfig.read("sql.ini")
csql: SectionProxy = sqlconfig["SQLSETTINGS"]

ConnectionString = f"{csql['DB_ENGINE']}://{csql['DB_USERNAME']}:{csql['DB_PASSWORD']}@{csql['DB_ADRESSES']}:{csql['DB_PORT']}/{csql['DB_DATABASE']}"
DbEngine = create_engine(ConnectionString)
Base: declarative_base = declarative_base()


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=True)
    site = Column(String(100), nullable=True)

    def __init__(self, first_name: str, last_name: str, site: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.site = site


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=False)


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime)
    history = Column(JSON)

    def __init__(self, user_id: int, date: datetime, history: dict):
        self.user_id = user_id
        self.date = date
        self.history = history


class UserInfo(Base):
    __tablename__ = "userinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    first_name = Column(String(70), nullable=False)
    last_name = Column(String(70), nullable=True)
    username = Column(String(40), nullable=True)

    def __init__(self, user_id, first_name, last_name, username) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), nullable=False)
    history = relationship(History)
    userinfo = relationship(UserInfo)

    def __init__(self, user_id) -> None:
        self.user_id = user_id


doc_tag_table = Table(
    "document_tags",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("document.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)

doc_author_table = Table(
    "document_authors",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("document.id")),
    Column("author_id", Integer, ForeignKey("author.id")),
)


class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    path = Column(String(100), nullable=True, unique=True)
    note = Column(String(300), nullable=True)
    enabled = Column(Boolean, default=False)
    rating = Column(Float, default=0.5)
    file_id = Column(String(100), nullable=True)
    tags = relationship(Tag, secondary=doc_tag_table)
    authors = relationship(Author, secondary=doc_author_table)

    def __init__(self, name, path, note, enabled, rating, file_id):
        self.name = name
        self.path = path
        self.note = note
        self.enabled = enabled
        self.rating = rating
        self.file_id = file_id


link_tag_table = Table(
    "link_tags",
    Base.metadata,
    Column("link_id", Integer, ForeignKey("link.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)

link_author_table = Table(
    "link_authors",
    Base.metadata,
    Column("link_id", Integer, ForeignKey("link.id")),
    Column("author_id", Integer, ForeignKey("author.id")),
)


class Link(Base):
    __tablename__ = "link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    path = Column(String(100), nullable=False)
    note = Column(String(300), nullable=True)
    enabled = Column(Boolean, default=False)
    rating = Column(Float, default=0.5)
    tags = relationship(Tag, secondary=link_tag_table)
    authors = relationship(Author, secondary=link_author_table)

    def __init__(self, name, path, note, enabled, rating):
        self.name = name
        self.path = path
        self.note = note
        self.enabled = enabled
        self.rating = rating


book_tag_table = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)

book_author_table = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("book.id")),
    Column("author_id", Integer, ForeignKey("author.id")),
)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    note = Column(String(300), nullable=True)
    enabled = Column(Boolean, default=False)
    rating = Column(Float, default=0.5)
    tags = relationship(Tag, secondary=book_tag_table)
    authors = relationship(Author, secondary=book_author_table)

    def __init__(self, name, note, enabled, rating):
        self.name = name
        self.note = note
        self.enabled = enabled
        self.rating = rating


class Question(Base):
    # TODO
    # need to improve for button ordering.
    __tablename__ = "question"

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


Session: sessionmaker = sessionmaker(DbEngine)
session = Session()