from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.kb import main_menu_kb, approve_kb
from states.states import Form
from database import is_approved

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if is_approved(message.from_user.id):
        await message.answer_photo(
            photo="https://i.ibb.co/F4qhJVTk/325-ACC37-3-A44-4513-90-B6-3794-A64-CD078.png",
            caption="🌿 Добро пожаловать\n\n👇 Куда дальше?",
            reply_markup=main_menu_kb()
        )
        return

    await message.answer("📋 Заполни анкету\n\nРасскажи о себе:")
    await state.set_state(Form.about)


@router.message(Form.about)
async def about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Откуда узнал?")
    await state.set_state(Form.source)


@router.message(Form.source)
async def source(message: Message, state: FSMContext):
    data = await state.get_data()

    text = (
        f"🆕 Новая анкета\n\n"
        f"👤 ID: {message.from_user.id}\n"
        f"📝 О себе: {data['about']}\n"
        f"📡 Источник: {message.text}"
    )

    # 🔥 отправка админу
    await message.bot.send_message(
        ADMIN_ID,
        text,
        reply_markup=approve_kb(message.from_user.id)
    )

    await message.answer("⏳ Заявка отправлена на проверку")
    await state.clear()
