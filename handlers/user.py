import random
import string

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.kb import projects_kb, main_menu_kb
from database import create_link, get_user_links
from states.states import Form, LinkForm
from aiogram.filters import StateFilter
from database import delete_link
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PHOTO_URL

router = Router()


# --- НАЖАЛ СОЗДАТЬ ССЫЛКУ ---
@router.callback_query(F.data == "create_link")
async def create_link_menu(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="🏝 Выбери проект:",
        reply_markup=projects_kb()
    )


# --- ГЕНЕРАЦИЯ ---


# --- ВЫБОР ПРОЕКТА ---
@router.callback_query(F.data.startswith("proj_"))
async def choose_project(callback: CallbackQuery, state: FSMContext):
   
    await callback.answer()
    
    project = callback.data.split("_")[1]
    
    await state.update_data(project=project)

    await callback.message.edit_caption(
    caption="💸 Введи цену:"
)

    await state.set_state(LinkForm.price)


# --- НАЗАД ---
@router.callback_query(F.data == "back_menu")
async def back(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="🌿 Главное меню",
        reply_markup=main_menu_kb()
    )

@router.message(StateFilter(LinkForm.price))
async def set_price(message: Message, state: FSMContext):
    data = await state.get_data()

    project = data.get("project")
    user_id = message.from_user.id
    price = int(message.text)

    link_id = create_link(user_id, project, price)
    link = f"https://ТВОЙ-ДОМЕН/link/{link_id}"

    await message.answer_photo(
        photo=PHOTO_URL,
        caption=f"""✅ Ссылка создана

📁 Проект: {project}
💸 Цена: {price}
🔗 {link}""",
        reply_markup=main_menu_kb()
    )

    await state.clear()

@router.callback_query(F.data == "my_links")
async def my_links(callback: CallbackQuery):
    user_id = callback.from_user.id

    links = get_user_links(user_id)

    if not links:
        await callback.message.edit_caption(
            caption="❌ У тебя нет объявлений",
            reply_markup=main_menu_kb()
        )
        await callback.answer()
        return

    text = "📂 Твои объявления:\n\n"
    keyboard = []

    for i, (project, price, link) in enumerate(links):
        text += f"""📁 {project}
💸 {price}
🔗 {link}

"""

        keyboard.append([
            InlineKeyboardButton(
                text=f"❌ Удалить {i+1}",
                callback_data=f"delete_{i}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_menu")
    ])

    await callback.message.edit_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

    await callback.answer()

@router.callback_query(F.data.startswith("delete_"))
async def delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    index = int(callback.data.split("_")[1])

    links = get_user_links(user_id)

    if index >= len(links):
        await callback.answer("Ошибка", show_alert=True)
        return

    link_to_delete = links[index][2]

    delete_link(user_id, link_to_delete)

    await callback.answer("Удалено ✅")

    # обновляем список
    await my_links(callback)
