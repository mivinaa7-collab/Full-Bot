from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import approve_user

router = Router()


@router.callback_query(F.data.startswith("approve_"))
async def approve(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    approve_user(user_id)

    await call.message.edit_text("✅ Пользователь одобрен")
    await call.bot.send_message(user_id, "🎉 Ты одобрен! Напиши /start")
    await call.answer()


@router.callback_query(F.data.startswith("reject_"))
async def reject(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    await call.message.edit_text("❌ Отклонено")
    await call.bot.send_message(user_id, "❌ Заявка отклонена")
    await call.answer()
