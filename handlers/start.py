from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database import is_approved
from keyboards.kb import main_menu_kb
from states.states import Form

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if is_approved(message.from_user.id):

        await message.answer_photo(
            photo="https://i.ibb.co/F4qhJVTk/325-ACC37-3-A44-4513-90-B6-3794-A64-CD078.png",
            caption=f"🌿 Привет, {message.from_user.full_name}"
            reply_markup=main_menu_kb()
        )

        return

    await message.answer("Расскажи о себе:")
    await state.set_state(Form.about)


@router.message(Form.about)
async def about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Откуда узнал?")
    await state.set_state(Form.source)

from database import approve_user

@router.message(Form.source)
async def source(message: Message, state: FSMContext):
    await state.update_data(source=message.text)

    approve_user(message.from_user.id)

    await message.answer("✅ Ты одобрен! Напиши /start")
    await state.clear()
