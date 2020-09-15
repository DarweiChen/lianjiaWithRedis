# -*- coding: utf-8 -*-
from peewee import *
import datetime
import settings

database = MySQLDatabase(
        settings.DBNAME,
        host=settings.DBHOST,
        port=settings.DBPORT,
        user=settings.DBUSER,
        passwd=settings.DBPASSWORD,
        charset='utf8',
        use_unicode=True,
    )

class BaseModel(Model):

    class Meta:
        database = database

class Houseinfo(BaseModel):
    houseID = CharField(primary_key=True)
    region = CharField()
    title = CharField()
    link = CharField()
    community = CharField()
    years = CharField()
    housetype = CharField()
    square = CharField()
    direction = CharField()
    floor = CharField()
    taxtype = CharField()
    totalPrice = CharField()
    unitPrice = CharField()
    followInfo = IntegerField()
    decoration = CharField()
    validdate = DateTimeField(default=datetime.datetime.now)


class Hisprice(BaseModel):
    houseID = CharField()
    totalPrice = CharField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        primary_key = CompositeKey('houseID', 'totalPrice')


def database_init():
    database.connect()
    database.create_tables(
        [Houseinfo, Hisprice], safe=True)
    database.close()
