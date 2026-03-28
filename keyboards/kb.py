from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏝 Создать ссылку", callback_data="create_link")],
            [InlineKeyboardButton(text="🤍 Мои объявления", callback_data="my_posts")],
            [InlineKeyboardButton(text="🍬 Настройки", callback_data="settings")]
        ]
    )


def admin_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Стата", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📩 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="🔨 Бан", callback_data="admin_ban")],
            [InlineKeyboardButton(text="🧾 Логи", callback_data="admin_logs")]
        ]
    )
