import asyncio
import random
import os
import aiohttp 
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = '8443201655:AAHiyh2JDq5OOstYZsosbLicVGN5ztJM0fo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ТВОИ ДАННЫЕ ---
movie_photos = {
    "Майор Гром": "grom.jpg",
    "Бумажный дом": "bumazh.jpg",
    "Шрек": "shrek.jpg",
    "Очень странные дела": "osd.jpg"
}
food_photos = {
    "Макарошки с котлетками": "makarons.jpg",
    "Бутербродики": "buter.jpg",
    "Печеночный торт": "tort.jpg",
    "Квашеная капуста": "kkapusta.jpg",
    "Пакетик хвостика": "korm.jpg",
    "Бутербродик с шоколадной пастой": "butersladko.jpg"
}
skills = ["Бегит в могазин", "Атжумания", "Пачитат книгу", "Помыть попу", "Покакат", "Покушат", "Поваляца с хвостиком"]

# --- ФУНКЦИИ ---

async def get_random_meme():
    url = "https://meme-api.com" 
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('url')
    except Exception as e:
        print(f"Ошибка при поиске мема: {e}")
    return None

async def send_scheduled_meme(bot: Bot):
    my_id = 662501989 
    meme_url = await get_random_meme()
    if meme_url:
        await bot.send_photo(chat_id=my_id, photo=meme_url, caption="✨ Время случайного мема!")

# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🎬 Что посмотреть?"))
    builder.row(types.KeyboardButton(text="🍕 Что же съесть?"))
    builder.row(types.KeyboardButton(text="💡 Чем заняться?"))
    await message.answer("Привет! Выбери категорию:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "🎬 Что посмотреть?")
async def movie_choice(message: types.Message):
    try:
        selected_movie = random.choice(list(movie_photos.keys()))
        photo = FSInputFile(movie_photos[selected_movie])
        await message.answer_photo(photo=photo, caption=f"😋 Советую глянуть {selected_movie}!")
    except Exception as e:
        await message.answer(f"Ошибка с фото кино: {e}")

@dp.message(F.text == "🍕 Что же съесть?")
async def food_choice(message: types.Message):
    try:
        selected_dish = random.choice(list(food_photos.keys()))
        photo = FSInputFile(food_photos[selected_dish])
        await message.answer_photo(photo=photo, caption=f"😋 Попробуй {selected_dish}!")
    except Exception as e:
        await message.answer(f"Ошибка с фото еды: {e}")

@dp.message(F.text == "💡 Чем заняться?")
async def skill_choice(message: types.Message):
    await message.answer(f"🛠 Отличная идея: {random.choice(skills)}")

@dp.message()
async def talk(message: types.Message):
    await message.answer(f"Я тебя не понял. Ты прислал: '{message.text}'")

# --- ЗАПУСК ---

async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow") # Указываем время по Мск
    
    # Настройка: каждый день в 12 утра (час=12, минута=0)
    scheduler.add_job(
        send_scheduled_meme, 
        trigger="cron", 
        hour=12, 
        minute=0, 
        args=(bot,)
    )
    
    scheduler.start()
    print("Планировщик запущен на 12:00!")
    print("Бот-помощник запущен!")
    
    await dp.start_polling(bot)

