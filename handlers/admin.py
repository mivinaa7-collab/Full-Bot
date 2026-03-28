from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import *
from keyboards.kb import admin_kb
from states.states import AdminFSM
from config import ADMIN_ID

router = Router()


# ---------- ВХОД В АДМИНКУ ----------

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    set_role(message.from_user.id, "owner")
    await message.answer("⚙️ Админ панель", reply_markup=admin_kb())


# ---------- СТАТИСТИКА ----------

@router.callback_query(F.data == "admin_stats")
async def admin_stats(c: CallbackQuery):
    await c.answer()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM roles WHERE banned=1")
    banned = cursor.fetchone()[0]

    await c.message.answer(
        f"📊 Статистика:\n\n"
        f"👤 Юзеров: {users}\n"
        f"🔨 Забанено: {banned}"
    )


# ---------- РАССЫЛКА ----------

@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(c: CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.answer("📩 Введи текст рассылки:")
    await state.set_state(AdminFSM.broadcast)


@router.message(AdminFSM.broadcast)
async def send_broadcast(message: Message, state: FSMContext):
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    ok = 0

    for (user_id,) in users:
        try:
            await message.bot.send_message(user_id, message.text)
            ok += 1
        except:
            pass

    await message.answer(f"✅ Отправлено: {ok}")
    await state.clear()


# ---------- БАН ----------

@router.callback_query(F.data == "admin_ban")
async def start_ban(c: CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.answer("🔨 Введи ID пользователя:")
    await state.set_state(AdminFSM.ban)


@router.message(AdminFSM.ban)
async def process_ban(message: Message, state: FSMContext):
    try:
        uid = int(message.text)
    except:
        await message.answer("❌ Нужен ID числом")
        return

    role, banned = get_role(uid)

    if banned:
        unban_user(uid)
        await message.answer("✅ Разбанен")
    else:
        ban_user(uid)
        await message.answer("🔨 Забанен")

    await state.clear()
