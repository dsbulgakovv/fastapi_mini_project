from enum import Enum
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {'message': 'Welcome to our pet clinic! Healthy pets make us happy.'}


@app.get('/dog')
def get_dog_by_breed(breed: DogType) -> list:
    """ Get dogs by breed. """
    dogs_searched = list()
    for pk, dog in dogs_db.items():
        if dog.kind == breed:
            dogs_searched.append(dog)
        else:
            continue

    return dogs_searched


@app.get('/dog/{primary_key}')
def get_dog_by_pk(primary_key: int) -> Dog:
    """ Get dog by primary key. """
    try:
        dog = dogs_db[primary_key]
    except KeyError:
        raise HTTPException(status_code=422, detail=f'The specified PK doesn\'t exist.')

    return dog


@app.post('/post')
def post() -> Timestamp:
    """ Post empty body. """
    next_id = post_db[-1].id + 1
    now = Timestamp(id=next_id, timestamp=datetime.now().hour)
    post_db.append(now)

    return now


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog) -> Dog:
    """ Post a new dog to the database """
    existing_pks = dogs_db.keys()
    if dog.pk in existing_pks:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    else:
        dogs_db[dog.pk] = dog

    return dog


@app.patch('/dog/{primary_key}')
def edit_dog(primary_key: int, dog: Dog) -> Dog:
    """ Edit an existing dog """
    existing_pks = dogs_db.keys()
    if primary_key in existing_pks:
        dogs_db[primary_key] = dog
    else:
        raise HTTPException(status_code=409,
                            detail='The specified PK doesn\'t exist.')

    return dog
