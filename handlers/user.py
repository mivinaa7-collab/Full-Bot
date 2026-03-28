from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import create_link, get_links
from keyboards.kb import main_menu_kb
from states.states import LinkForm

router = Router()

# --- СОЗДАНИЕ ССЫЛКИ ---

@router.callback_query(F.data == "create_link")
async def create_link_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введи название проекта:")
    await state.set_state(LinkForm.project)
    await call.answer()


@router.message(LinkForm.project)
async def link_project(message: Message, state: FSMContext):
    await state.update_data(project=message.text)
    await message.answer("Введи цену:")
    await state.set_state(LinkForm.price)


@router.message(LinkForm.price)
async def link_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Вставь ссылку:")
    await state.set_state(LinkForm.link)


@router.message(LinkForm.link)
async def link_done(message: Message, state: FSMContext):
    data = await state.get_data()

    create_link(
        user_id=message.from_user.id,
        project=data["project"],
        price=int(data["price"]),
        link=message.text
    )

    await message.answer("✅ Ссылка создана", reply_markup=main_menu_kb())
    await state.clear()


# --- МОИ ОБЪЯВЛЕНИЯ ---

@router.callback_query(F.data == "my_posts")
async def my_posts(call: CallbackQuery):
    links = get_links(call.from_user.id)

    if not links:
        await call.message.answer("❌ У тебя нет объявлений")
        await call.answer()
        return

    text = "📦 Твои объявления:\n\n"

    for project, price, link in links:
        text += f"🏝 {project}\n💰 {price}\n🔗 {link}\n\n"

    await call.message.answer(text)
    await call.answer()


# --- НАСТРОЙКИ ---

@router.callback_query(F.data == "settings")
async def settings(call: CallbackQuery):
    await call.message.answer("⚙️ Настройки (пока пусто)")
    await call.answer()
