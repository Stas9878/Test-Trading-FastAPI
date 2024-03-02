from sqlalchemy import (MetaData, 
                        Integer, String, 
                        TIMESTAMP, ForeignKey, 
                        Table, Column, 
                        JSON)
from datetime import datetime

metadata = MetaData()

roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registrated_at', TIMESTAMP, default=datetime.utcnow()),
    Column('role_id', Integer, ForeignKey('roles.id'))
)