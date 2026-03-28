from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# --- ОСНОВНОЕ МЕНЮ ПОД ФОТО ---
def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏝 Создать ссылку", callback_data="create_link")],
            [InlineKeyboardButton(text="🤍 Мои объявления", callback_data="my_posts")],
            [InlineKeyboardButton(text="🍬 Настройки", callback_data="settings")]
        ]
    )


# --- АДМИНКА ---
def admin_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Стата", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📩 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔨 Бан", callback_data="admin_ban")],
            [InlineKeyboardButton(text="🧾 Логи", callback_data="admin_logs")]
        ]
    )


# --- КНОПКИ ОДОБРЕНИЯ АНКЕТЫ ---
def approve_kb(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Одобрить",
                    callback_data=f"approve_{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"decline_{user_id}"
                )
            ]
        ]
    )

# --- ПРОЕКТЫ ---
def projects_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇦 Privat24", callback_data="proj_privat"),
                InlineKeyboardButton(text="🇺🇦 Oshad24", callback_data="proj_oshad"),
            ],
            [
                InlineKeyboardButton(text="🇺🇦 Viber", callback_data="proj_viber"),
                InlineKeyboardButton(text="🇺🇦 Дія", callback_data="proj_diya"),
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_menu")
            ]
        ]
    )
