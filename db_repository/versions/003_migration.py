from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', Unicode(length=64)),
    Column('email', String(length=64)),
    Column('password_hash', String(length=128)),
    Column('_confirmed', SmallInteger, default=ColumnDefault(0)),
    Column('thanks_received', Integer, default=ColumnDefault(0)),
    Column('todos_created_num', Integer, default=ColumnDefault(0)),
    Column('todos_done_num', Integer, default=ColumnDefault(0)),
    Column('memos_created_num', Integer, default=ColumnDefault(0)),
    Column('device_token', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['device_token'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['device_token'].drop()
