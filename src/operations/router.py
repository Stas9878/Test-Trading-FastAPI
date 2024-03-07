from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_users_db_sqlalchemy import AsyncSession
from sqlalchemy import insert, select
from fastapi_cache.decorator import cache
from operations.models import operation
from operations.schemas import OperationCreate
from database import get_async_session



router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)



@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
        }
    
    except:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })
    
@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(operation).values(new_operation.model_dump())
    await session.execute(query)
    await session.commit()
    return {'status': 'success'}


import time
@router.get("/long")
@cache(expire=30)
async def index():
    time.sleep(2)
    return dict(hello="world")