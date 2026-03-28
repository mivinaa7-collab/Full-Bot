import random
import string

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.kb import projects_kb, main_menu_kb
from database import create_link

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
    user_id = callback.from_user.id
    project = callback.data.split("_")[1]

    link = generate_link(project)

    create_link(user_id, project, link)

    await callback.message.edit_caption(
        caption=f"""✅ Ссылка создана

🏷 Проект: {project}
🔗 {link}
""",
        reply_markup=main_menu_kb()
    )


# --- НАЗАД ---
@router.callback_query(F.data == "back_menu")
async def back(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="🌿 Главное меню",
        reply_markup=main_menu_kb()
    )
