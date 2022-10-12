from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, select
from datetime import datetime

metadata = MetaData()

engine = create_engine("sqlite:///toptoon.db")

# items model
items = Table('items', metadata,
    Column('id', Integer(), primary_key=True),
    Column('link', String(200), nullable=False),
    Column('orig_title', String(200), nullable=False),
    Column('en_title', String(200), nullable=False),
    Column('ru_title', String(200), nullable=False),
    Column('resource', String(200), nullable=False),
    Column('created_on', DateTime(), default=datetime.now)
)

# create table
# metadata.create_all(engine)

def get_item(link):
    query = select([items]).where(items.c.link == link)
    return engine.connect().execute(query).first()
