from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.kb import main_menu_kb, approve_kb
from states.states import Form
from database import is_approved, add_user, approve_user, is_banned, ban_user
from config import OWNER_ID, PHOTO_URL

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    add_user(user_id)

    if is_banned(user_id):
        return await message.answer("🚫 Ты забанен")

    if is_approved(user_id):
        await message.answer_photo(
            photo=PHOTO_URL,
            caption="🌿 Добро пожаловать\n\n👇 Куда дальше?",
            reply_markup=main_menu_kb(user_id)
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

    await message.bot.send_message(
        OWNER_ID,
        text,
        reply_markup=approve_kb(message.from_user.id)
    )

    await message.answer("⏳ Заявка отправлена")
    await state.clear()


# --- ОДОБРЕНИЕ ---
@router.callback_query(F.data.startswith("approve_"))
async def approve(call: CallbackQuery):
    if call.from_user.id != OWNER_ID:
        return await call.answer("Нет доступа", show_alert=True)

    user_id = int(call.data.split("_")[1])

    approve_user(user_id)

    await call.message.edit_text("✅ Одобрен")
    await call.bot.send_message(user_id, "🎉 Ты одобрен")
    await call.answer()


# --- БАН ---
@router.message(F.text.startswith("/ban"))
async def ban_cmd(message: Message):
    if message.from_user.id != OWNER_ID:
        return

    try:
        user_id = int(message.text.split()[1])
    except:
        return await message.answer("Формат: /ban ID")

    ban_user(user_id)
    await message.answer("🔨 Забанен")
