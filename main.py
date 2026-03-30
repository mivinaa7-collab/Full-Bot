import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start, user, admin
from handlers.admin import router as admin_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


from database import init_db

async def main():
    print("Bot started")

    init_db()

    # подключаем хендлеры
    dp.include_router(start.router)
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # фикс конфликта (ВАЖНО)
    await bot.delete_webhook(drop_pending_updates=True)

    # запуск
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
