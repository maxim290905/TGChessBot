import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from config import Token

# Функция для создания Inline-клавиатуры с кнопкой для игры
def webapp_builder() -> types.InlineKeyboardMarkup:
    # Создаем клавиатуру с одной кнопкой
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[  # Список кнопок
            [
                types.InlineKeyboardButton(
                    text="Начать игру", 
                    web_app=WebAppInfo(url="https://127.0.0.1:8000")  # Укажите URL вашего FastAPI-сервера
                )
            ]
        ]
    )
    return keyboard

# Обработчик команды /start
async def on_start(message: types.Message):
    await message.reply(
        "Привет! Нажмите кнопку ниже, чтобы начать игру.",
        reply_markup=webapp_builder()  # Отправляем кнопку с ссылкой на веб-приложение
    )

async def main():
    bot = Bot(token=Token, session=AiohttpSession(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.message.register(on_start, CommandStart())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
