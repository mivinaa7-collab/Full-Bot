from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database import approve_user, ban_user, unban_user
from config import OWNER_ID, SENIOR_ADMINS

router = Router()


class Broadcast:
    text = "broadcast_text"


def is_senior(user_id):
    return user_id in SENIOR_ADMINS


@router.callback_query(F.data == "admin_panel")
async def admin_panel(call: CallbackQuery):
    if not is_senior(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="broadcast")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_menu")]
    ])

    await call.message.edit_text("⚙️ Админ панель", reply_markup=kb)
    await call.answer()


@router.callback_query(F.data == "broadcast")
async def start_broadcast(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("✍️ Введи текст рассылки:")
    await state.set_state(Broadcast.text)
    await call.answer()


@router.message(StateFilter(Broadcast.text))
async def send_broadcast(message: Message, state: FSMContext):
    users = get_all_users()

    sent = 0
    for user_id in users:
        try:
            await message.bot.send_message(user_id, message.text)
            sent += 1
        except:
            pass

    await message.answer(f"✅ Отправлено: {sent}")
    await state.clear()


@router.callback_query(F.data.startswith("approve_"))
async def approve(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    approve_user(user_id)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔨 Бан", callback_data=f"ban_{user_id}"),
            InlineKeyboardButton(text="♻️ Разбан", callback_data=f"unban_{user_id}")
        ]
    ])

    await call.message.edit_text("✅ Одобрен", reply_markup=kb)
    await call.bot.send_message(user_id, "🎉 Ты одобрен")
    await call.answer()


@router.callback_query(F.data.startswith("reject_"))
async def reject(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    await call.message.edit_text("❌ Отклонен")
    await call.bot.send_message(user_id, "❌ Тебя отклонили")
    await call.answer()


@router.callback_query(F.data.startswith("ban_"))
async def ban(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    ban_user(user_id)

    await call.answer("Забанен")


@router.callback_query(F.data.startswith("unban_"))
async def unban(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    unban_user(user_id)

    await call.answer("Разбанен")
