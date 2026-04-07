import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start, user

from database import init_db

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    print("Bot started")

    init_db()

    dp.include_router(start.router)
    dp.include_router(user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
