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
)

todos_done = Table('todos_done', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item', Unicode(length=128)),
    Column('thanks_received', Integer, default=ColumnDefault(0)),
    Column('created_time', DateTime, default=ColumnDefault(<function datetime.utcnow at 0x7fee6dd4e2f0>)),
    Column('board_id', Integer),
    Column('user_id', Integer),
)

thanks = Table('thanks', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('done_id', Integer, nullable=False),
    Column('done_item', Unicode(length=128)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['todos_created_num'].create()
    post_meta.tables['users'].columns['todos_done_num'].create()
    post_meta.tables['todos_done'].columns['thanks_received'].create()
    post_meta.tables['thanks'].columns['done_item'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['todos_created_num'].drop()
    post_meta.tables['users'].columns['todos_done_num'].drop()
    post_meta.tables['todos_done'].columns['thanks_received'].drop()
    post_meta.tables['thanks'].columns['done_item'].drop()
