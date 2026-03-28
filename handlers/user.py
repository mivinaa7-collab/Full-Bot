from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import uuid

from database import *
from states.states import Form

router = Router()


def generate_link(user_id, project):
    return f"https://example.com/{project}/{uuid.uuid4().hex[:6]}"


# ---------- АНКЕТА ----------

@router.message(Form.source)
async def source(message: Message, state: FSMContext):
    approve_user(message.from_user.id)
    await message.answer("✅ Ты одобрен! Напиши /start")
    await state.clear()


# ---------- СОЗДАНИЕ ССЫЛКИ ----------

@router.callback_query(F.data == "create_link")
async def create_link(c: CallbackQuery, state: FSMContext):
    await c.answer()
    await c.message.answer("Введи цену:")
    await state.set_state(Form.price)


@router.message(Form.price)
async def price(m: Message, state: FSMContext):
    if not m.text.isdigit():
        return await m.answer("❌ Введи число")

    link = generate_link(m.from_user.id, "default")

    cursor.execute(
        "INSERT INTO links (user_id, project, price, link) VALUES (?, ?, ?, ?)",
        (m.from_user.id, "default", int(m.text), link)
    )
    conn.commit()

    log(m.from_user.id, "create link")

    await m.answer(f"🔗 Ссылка:\n{link}")
    await state.clear()


# ---------- МОИ ССЫЛКИ ----------

@router.callback_query(F.data == "my_posts")
async def my_posts(c: CallbackQuery):
    await c.answer()

    cursor.execute("SELECT link FROM links WHERE user_id=?", (c.from_user.id,))
    data = cursor.fetchall()

    if not data:
        await c.message.answer("📭 Нет ссылок")
        return

    text = "\n".join([i[0] for i in data])
    await c.message.answer(f"🐰 Твои ссылки:\n\n{text}")
