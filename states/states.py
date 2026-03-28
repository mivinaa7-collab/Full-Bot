from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    about = State()     # о себе
    source = State()    # откуда узнал
    price = State()     # цена ссылки
    tag = State()       # тег


class AdminFSM(StatesGroup):
    broadcast = State()  # рассылка
    ban = State()        # бан
