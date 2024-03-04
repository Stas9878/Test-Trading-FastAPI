from fastapi import APIRouter, Depends
from fastapi_users_db_sqlalchemy import AsyncSession
from sqlalchemy import insert, select
from operations.models import operation
from operations.schemas import OperationCreate
from database import get_async_session


router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)

@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)

    return result.all()

@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(operation).values(new_operation.model_dump())
    await session.execute(query)
    return {'status': 'success'}