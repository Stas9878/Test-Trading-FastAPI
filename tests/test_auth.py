import pytest
from sqlalchemy import insert, select

from auth.models import role
from conftest import client, async_session_maker


# pytest tests -p no:warnings -v

async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name='admin', permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], 'Роль не добавилась'


def test_register():
    response = client.post('/auth/register', json={
        'email': 'test@mail.ru',
        'password': 'string',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'username': 'testname',
        'role_id': 0
        })
    assert response.status_code == 201