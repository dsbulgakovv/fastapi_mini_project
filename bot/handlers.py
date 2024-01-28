import os

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import keyboards as kb
import logging
from utils import PetClinicAPI

# API_URL = os.environ['API_URL']
# api = PetClinicAPI(API_URL)
log = logging.getLogger()
log.setLevel('INFO')

api = PetClinicAPI()
router = Router()


class ServicesStates(StatesGroup):
    standard = State()
    dog_by_breed = State()
    dog_by_pk = State()
    new_dog = State()
    edit_dog = State()


markup_text = "<b>Name:</b> {}\n<b>PK:</b> {}\n<b>Breed:</b> {}"


# Hello
@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    response = await api.get_root()
    reply = response.get('message')
    await msg.answer(text=reply, reply_markup=kb.standard_kb)
    await state.set_state(ServicesStates.standard)


@router.message(F.text == "Hello!")
async def process_hello(msg: Message, state: FSMContext):
    response = await api.get_root()
    reply = response.get('message')
    await msg.answer(text=reply, reply_markup=kb.standard_kb)
    await state.set_state(ServicesStates.standard)


# GET Breed
@router.message(F.text == "Get dogs by breed")
async def process_get_dog_by_breed(msg: Message, state: FSMContext):
    reply = "Choose a breed"
    await msg.answer(text=reply, reply_markup=kb.breeds_kb)
    await state.set_state(ServicesStates.dog_by_breed)


@router.message(StateFilter(ServicesStates.dog_by_breed))
async def process_get_dog_by_breed_core(msg: Message, state: FSMContext) -> None:
    response = await api.get_dog_by_breed(msg.text)
    dogs_qnt = len(response)
    reply = ''
    for i in range(dogs_qnt):
        dog = response[i]
        reply += markup_text.format(dog['name'], dog['pk'], dog['kind']) + '\n\n'
    await msg.answer(text=reply, reply_markup=kb.standard_kb)
    await state.set_state(ServicesStates.standard)


# GET PK
@router.message(F.text == "Get dog by PK")
async def process_dog_by_pk(msg: Message, state: FSMContext):
    response = await api.get_all_dogs()
    max_num = len(response) - 1
    reply = f"Type your dog PK (from 0 to {max_num})"
    await msg.answer(text=reply)
    await state.set_state(ServicesStates.dog_by_pk)


@router.message(StateFilter(ServicesStates.dog_by_pk))
async def process_dog_by_pk_core(msg: Message,  state: FSMContext) -> None:
    response_max_num = await api.get_all_dogs()
    max_num = len(response_max_num) - 1
    if max_num < int(msg.text):
        await msg.answer(text="Type correct PK")
        await state.set_state(ServicesStates.dog_by_pk)
    else:
        response = await api.get_dog_by_pk(msg.text)
        dog = response
        reply = markup_text.format(dog['name'], dog['pk'], dog['kind'])
        await msg.answer(text=reply, reply_markup=kb.standard_kb)
        await state.set_state(ServicesStates.standard)


# POST time
@router.message(F.text == "Post time")
async def process_time(msg: Message, state: FSMContext):
    response = await api.post()
    reply = "post id: " + str(response['id']) + "\n" + str(response['timestamp']) + " o'clock"
    await msg.answer(text=reply, reply_markup=kb.standard_kb)
    await state.set_state(ServicesStates.standard)


# POST new dog
@router.message(F.text == "Add new dog")
async def process_add_new_dog(msg: Message, state: FSMContext):
    reply = (
        "Please, type info about your new dog in the following format:\n"
        "<i>name, pk, breed</i>"
    )
    await msg.answer(text=reply)
    await state.set_state(ServicesStates.new_dog)


@router.message(StateFilter(ServicesStates.new_dog))
async def process_add_new_dog_core(msg: Message, state: FSMContext) -> None:
    name, pk, breed = tuple(map(str.strip, msg.text.split(',')))
    response, status = await api.post_dog(name, int(pk), breed)
    if status == 200:
        reply = (
            'Your dog is successfully added:\n\n'
            +
            markup_text.format(name, pk, breed)
        )
        await msg.answer(text=reply, reply_markup=kb.standard_kb)
        await state.set_state(ServicesStates.standard)
    else:
        reply = f'Error {str(status)}\nSomething went wrong...\nPlease, try again.\nFormat: <i>name, pk, breed</i>'
        await msg.answer(text=reply)
        await state.set_state(ServicesStates.new_dog)


# Edit dog
@router.message(F.text == "Edit existing dog")
async def process_edit_dog(msg: Message, state: FSMContext):
    reply = (
        "Please, type info about your dog you want to change in the following format:\n"
        "<i>new_name, old_pk, new_breed</i>"
    )
    await msg.answer(text=reply)
    await state.set_state(ServicesStates.edit_dog)


@router.message(StateFilter(ServicesStates.edit_dog))
async def process_edit_dog_core(msg: Message, state: FSMContext) -> None:
    name, pk, breed = tuple(map(str.strip, msg.text.split(',')))
    response, status = await api.edit_dog(int(pk), name, breed)
    if status == 200:
        reply = (
            'Your dog is successfully updated:\n\n'
            +
            markup_text.format(name, pk, breed)
        )
        await msg.answer(text=reply, reply_markup=kb.standard_kb)
        await state.set_state(ServicesStates.standard)
    else:
        reply = f'Error {str(status)}\nSomething went wrong...\nPlease, try again.\nFormat: <i>name, pk, breed</i>'
        await msg.answer(text=reply)
        await state.set_state(ServicesStates.new_dog)
