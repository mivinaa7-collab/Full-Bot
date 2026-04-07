from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏝 Создать ссылку", callback_data="create_link")],
            [InlineKeyboardButton(text="🤍 Мои объявления", callback_data="my_links")],
        ]
    )


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
                    callback_data=f"reject_{user_id}"
                )
            ]
        ]
    )


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
