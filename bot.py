import aiogram.exceptions
import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from logger import logger

from bot_utils import parse_wildberries, check_input


load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start_bot(message: types.Message):
    """Start bot"""
    await message.answer(f'Hello {message.chat.first_name}! '
                         'Bot is running.')


@dp.message()
async def search_item(message: types.Message):
    try:
        vendor_code, item_name = check_input(message.text)
    except ValueError as er:
        return await message.answer(str(er))
    await message.answer(
        parse_wildberries(
            vendor_code=vendor_code,
            item_name=item_name
        )
    )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except aiogram.exceptions.TelegramUnauthorizedError:
        logger.error('Wrong tg token')
