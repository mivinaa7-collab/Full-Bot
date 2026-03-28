import random
import string

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.kb import projects_kb, main_menu_kb
from database import create_link
from states.states import Form

router = Router()


# --- НАЖАЛ СОЗДАТЬ ССЫЛКУ ---
@router.callback_query(F.data == "create_link")
async def create_link_menu(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="🏝 Выбери проект:",
        reply_markup=projects_kb()
    )


# --- ГЕНЕРАЦИЯ ---
def generate_link(project):
    rand = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"https://your-domain.com/{project}/{rand}"


# --- ВЫБОР ПРОЕКТА ---
@router.callback_query(F.data.startswith("proj_"))
async def choose_project(callback: CallbackQuery):
    
    project = callback.data.split("_")[1]
    
    await state.update_data(project=project)

    await callback.message.edit_caption(
    caption="💸 Введи цену:"
)

    await state.set_state(Form.price)


# --- НАЗАД ---
@router.callback_query(F.data == "back_menu")
async def back(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="🌿 Главное меню",
        reply_markup=main_menu_kb()
    )

@router.message(Form.price)
async def set_price(message: Message, state: FSMContext):
    data = await state.get_data()

    project = data.get("project")
    user_id = message.from_user.id
    price = message.text

    link = generate_link(project)

    create_link(user_id, project, price, link)

    await message.answer(
        f"""✅ Ссылка создана

📁 Проект: {project}
💸 Цена: {price}
🔗 {link}""",
        reply_markup=main_menu_kb()
    )

    await state.clear()
