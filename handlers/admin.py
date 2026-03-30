from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import approve_user, ban_user, unban_user
from config import OWNER_ID, SENIOR_ADMINS

router = Router()


def is_owner(user_id):
    return user_id == OWNER_ID

def is_senior(user_id):
    return user_id in SENIOR_ADMINS or user_id == OWNER_ID


# --- МЕНЮ АДМИНКИ ---
@router.callback_query(F.data == "admin")
async def admin_panel(call: CallbackQuery):
    if not is_senior(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Заявки", callback_data="admin_apps")],
        [InlineKeyboardButton(text="🔨 Бан", callback_data="admin_ban")],
        [InlineKeyboardButton(text="♻️ Разбан", callback_data="admin_unban")],
    ])

    if is_owner(call.from_user.id):
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text="⚙️ OWNER PANEL", callback_data="owner_panel")]
        )

    await call.message.edit_text("⚙️ Админ панель", reply_markup=kb)


# --- АПРУВ ---
@router.callback_query(F.data.startswith("approve_"))
async def approve(call: CallbackQuery):
    if not is_senior(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    user_id = int(call.data.split("_")[1])

    approve_user(user_id)

    await call.message.edit_text("✅ Пользователь одобрен")
    await call.bot.send_message(user_id, "🎉 Ты одобрен")

    await call.answer()


# --- ОТКЛОН ---
@router.callback_query(F.data.startswith("reject_"))
async def reject(call: CallbackQuery):
    if not is_senior(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    user_id = int(call.data.split("_")[1])

    await call.message.edit_text("❌ Отклонен")
    await call.bot.send_message(user_id, "❌ Тебя отклонили")

    await call.answer()


# --- БАН ---
@router.callback_query(F.data.startswith("ban_"))
async def ban(call: CallbackQuery):
    if not is_senior(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    user_id = int(call.data.split("_")[1])

    ban_user(user_id)

    await call.message.edit_text("🔨 Пользователь забанен")
    await call.bot.send_message(user_id, "🚫 Ты забанен")

    await call.answer()


# --- РАЗБАН ---
@router.callback_query(F.data.startswith("unban_"))
async def unban(call: CallbackQuery):
    if not is_senior(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    user_id = int(call.data.split("_")[1])

    unban_user(user_id)

    await call.message.edit_text("♻️ Пользователь разбанен")
    await call.bot.send_message(user_id, "✅ Ты разбанен")

    await call.answer()


# --- OWNER ПАНЕЛЬ ---
@router.callback_query(F.data == "owner_panel")
async def owner_panel(call: CallbackQuery):
    if not is_owner(call.from_user.id):
        return await call.answer("Нет доступа", show_alert=True)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="broadcast")],
    ])

    await call.message.edit_text("👑 OWNER PANEL", reply_markup=kb)
