from aiogram.fsm.state import StatesGroup, State


# анкета
class Form(StatesGroup):
    about = State()
    source = State()


# создание ссылки
class LinkForm(StatesGroup):
    project = State()
    price = State()
    link = State()


# админка (оставляем)
class AdminFSM(StatesGroup):
    broadcast = State()
    ban = State()
