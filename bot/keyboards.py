from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
button_say_hello = KeyboardButton(text='Hello!')
button_dog_breed = KeyboardButton(text='Get dogs by breed')
button_dog_pk = KeyboardButton(text='Get dog by PK')
button_time_now = KeyboardButton(text='Post time')
button_dog_create = KeyboardButton(text='Add new dog')
button_dog_edit = KeyboardButton(text='Edit existing dog')

standard_kb = ReplyKeyboardMarkup(
    keyboard=[
        [button_say_hello, button_dog_breed],
        [button_dog_pk, button_time_now],
        [button_dog_create, button_dog_edit]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


terrier = KeyboardButton(text='terrier')
bulldog = KeyboardButton(text='bulldog')
dalmatian = KeyboardButton(text='dalmatian')

breeds_kb = ReplyKeyboardMarkup(
    keyboard=[
        [terrier, bulldog, dalmatian]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)