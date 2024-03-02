from enum import Enum
from typing import List
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

app = FastAPI(
    title='Trading App'
)

@app.exception_handler(ValidationException)
async def validation_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            'detail': exc.errors()
        })
    )

fake = [
    {'id': 1, 'name': ['Stas']},
    {'id': 2, 'name': 'Julia'},
    {'id': 3, 'name': 'Nadya'},
    {'id': 4, 'name': 'Nadya', 'degree': [{'id': 1, 'type': 'expert'}]},
    {'id': 5, 'name': 'Nadya', 'degree': [{'id': 2, 'type': 'newbie'}]}
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'

class Degree(BaseModel):
    id: int
    type: DegreeType


class User(BaseModel):
    id: int
    name: str
    degree: List[Degree] | List = []

@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake if user['id'] == user_id]

fake_trades = [
    {'id': 1, 'name': 'Stas', 'price': 123, 'amount': 2.12},
    {'id': 2, 'name': 'Julia', 'price': 111, 'amount': 1.22},
    {'id': 3, 'name': 'Nadya', 'price': 20, 'amount': 3.11}
]

@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users = [
    {'id': 1, 'name': 'Stas'},
    {'id': 2, 'name': 'Julia'},
    {'id': 3, 'name': 'Nadya'}
]

@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda x: x['id'] == user_id, fake_users))[0]
    old_name = current_user['name']
    current_user['name'] = new_name

    return {
        'status': 200,
        'old_name': old_name,
        'new_name': new_name 
    }

class Trades(BaseModel):
    id: int
    user_id: int
    price: int = Field(ge=0)
    amount: float

@app.post('/trades')
def add_trades(trades: List[Trades]):
    fake_trades.extend(trades)
    return {
        'status': 200,
        'data': fake_trades
    }
    