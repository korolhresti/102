import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncpg

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привіт! Це твій персональний новинний бот.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)