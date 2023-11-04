from enum import Enum
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
    """ Get dog by bread. """
    dogs_searched = list()
    for pk, dog in dogs_db.items():
        if dog.kind == breed:
            dog_dsc = dict()
            dog_dsc['name'] = dog.name
            dog_dsc['pk'] = dog.pk
            dog_dsc['kind'] = dog.kind
            dogs_searched.append(dog_dsc)
        else:
            continue

    return dogs_searched


@app.get('/dog/{primary_key}')
def get_dog_by_pk(primary_key: int) -> dict:
    """ Get dog by primary key. """
    try:
        dog = dogs_db[primary_key]
        dog_searched = dict()
        dog_searched['name'] = dog.name
        dog_searched['pk'] = dog.pk
        dog_searched['kind'] = dog.kind
    except KeyError:
        raise HTTPException(status_code=422, detail=f'There is no dog with index {primary_key} :(')

    return dog_searched
