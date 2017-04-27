from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
meetup_times = Table('meetup_times', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('board_id', Integer),
    Column('start_time', DateTime),
    Column('end_time', DateTime),
)

boards = Table('boards', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', Unicode(length=64)),
    Column('created_time', DateTime, default=ColumnDefault(<function datetime.utcnow at 0x7fde47442730>)),
    Column('meetup_status', SmallInteger, default=ColumnDefault(0)),
    Column('meetup_location', Unicode(length=128)),
    Column('meetup_time', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['meetup_times'].create()
    post_meta.tables['boards'].columns['meetup_location'].create()
    post_meta.tables['boards'].columns['meetup_status'].create()
    post_meta.tables['boards'].columns['meetup_time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['meetup_times'].drop()
    post_meta.tables['boards'].columns['meetup_location'].drop()
    post_meta.tables['boards'].columns['meetup_status'].drop()
    post_meta.tables['boards'].columns['meetup_time'].drop()
