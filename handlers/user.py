from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards.kb import projects_kb, main_menu_kb
from database import create_link, get_user_links, delete_link
from states.states import LinkForm
from config import PHOTO_URL

router = Router()


# --- СОЗДАТЬ ССЫЛКУ ---
@router.callback_query(F.data == "create_link")
async def create_link_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_caption(
            caption="🏝 Выбери проект:",
            reply_markup=projects_kb()
        )
    except:
        await callback.message.edit_text(
            "🏝 Выбери проект:",
            reply_markup=projects_kb()
        )
    await callback.answer()


# --- ВЫБОР ПРОЕКТА ---
@router.callback_query(F.data.startswith("proj_"))
async def choose_project(callback: CallbackQuery, state: FSMContext):
    project = callback.data.split("_")[1]
    await state.update_data(project=project)

    try:
        await callback.message.edit_caption(
            caption="💸 Введи цену:"
        )
    except:
        await callback.message.edit_text(
            "💸 Введи цену:"
        )

    await state.set_state(LinkForm.price)
    await callback.answer()


# --- НАЗАД ---
@router.callback_query(F.data == "back_menu")
async def back(callback: CallbackQuery):
    try:
        await callback.message.edit_caption(
            caption="🌿 Главное меню",
            reply_markup=main_menu_kb(callback.from_user.id)
        )
    except:
        await callback.message.edit_text(
            "🌿 Главное меню",
            reply_markup=main_menu_kb(callback.from_user.id)
        )
    await callback.answer()


# --- ВВОД ЦЕНЫ ---
@router.message(StateFilter(LinkForm.price))
async def set_price(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        return await message.answer("💸 Введи число")

    data = await state.get_data()

    project = data.get("project")
    user_id = message.from_user.id
    price = int(message.text)

    link_id = create_link(user_id, project, price)
    link = f"https://web-production-0572a.up.railway.app/link/{link_id}"

    await message.answer_photo(
        photo=PHOTO_URL,
        caption=f"""✅ Ссылка создана

📁 Проект: {project}
💸 Цена: {price}
🔗 {link}""",
        reply_markup=main_menu_kb(user_id)
    )

    await state.clear()


# --- МОИ ОБЪЯВЛЕНИЯ ---
@router.callback_query(F.data == "my_links")
async def my_links(callback: CallbackQuery):
    user_id = callback.from_user.id
    links = get_user_links(user_id)

    if not links:
        try:
            await callback.message.edit_caption(
                caption="❌ У тебя нет объявлений",
                reply_markup=main_menu_kb(user_id)
            )
        except:
            await callback.message.edit_text(
                "❌ У тебя нет объявлений",
                reply_markup=main_menu_kb(user_id)
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

    try:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    except:
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )

    await callback.answer()


# --- УДАЛЕНИЕ ---
@router.callback_query(F.data.startswith("delete_"))
async def delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    index = int(callback.data.split("_")[1])

    links = get_user_links(user_id)

    if index >= len(links):
        return await callback.answer("Ошибка", show_alert=True)

    link_to_delete = links[index][2]
    delete_link(user_id, link_to_delete)

    await callback.answer("Удалено ✅")

    # обновляем список
    await my_links(callback)
