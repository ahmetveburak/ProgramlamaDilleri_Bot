from enum import unique
from mongoengine import Document
from mongoengine.fields import StringField, FloatField, ListField, BooleanField
from mongoengine.fields import LongField, DictField, DateTimeField


class Questions(Document):
    question = DictField()
    meta = {"db_alias": "core", "collection": "Questions"}


class Documents(Document):

    name = StringField(reqired=True, unique=True)
    path = StringField(reqired=True)
    authors = ListField(reqired=True)
    tags = ListField(reqired=True)
    note = StringField(default="")
    enabled = BooleanField(default=True, reqired=True)
    rating = FloatField(default=0.0, max_value=10.0, reqired=True)
    file_id = StringField(default="")

    meta = {"db_alias": "core", "collection": "Documents"}


class Links(Document):

    name = StringField(reqired=True)
    path = StringField(reqired=True)
    authors = ListField(reqired=True)
    tags = ListField(reqired=True)
    note = StringField(reqired=True)
    enabled = BooleanField(default=True, reqired=True)
    rating = FloatField(max_value=10.0, reqired=True)

    meta = {"db_alias": "core", "collection": "Links"}


class Books(Document):

    name = StringField(reqired=True)
    authors = ListField(reqired=True)
    tags = ListField(reqired=True)
    note = StringField(reqired=True)
    enabled = BooleanField(default=True, reqired=True)
    rating = FloatField(max_value=10.0, reqired=True)

    meta = {"db_alias": "core", "collection": "Books"}


class Users(Document):
    user_id = LongField(reqired=True)
    first_name = StringField(max_length=200, required=True)
    last_name = StringField(max_length=200, default=None)
    username = StringField(max_length=200, default=None)
    tags = ListField()
    books = ListField()
    date = DateTimeField()

    meta = {"db_alias": "core", "collection": "Users"}
