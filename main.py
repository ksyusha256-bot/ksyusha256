import asyncio
import random
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask
from threading import Thread

# --- НАСТРОЙКИ ---
API_TOKEN = '8443201655:AAHiyh2JDq5OOstYZsosbLicVGN5ztJM0fo'
USER_IDS = [662501989, 650682969] 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask('')

@app.route('/')
def home(): return "I'm alive!"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def get_random_meme():
    # ТУТ ТЕПЕРЬ ПРАВИЛЬНАЯ ССЫЛКА
    url = "https://dog.ceo" 
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('message')
    except: return None

async def send_scheduled_meme(bot: Bot):
    meme_url = await get_random_meme()
    if meme_url:
        for user_id in USER_IDS:
            try:
                await bot.send_photo(chat_id=user_id, photo=meme_url, caption="✨ Ежедневный мем!")
            except: pass

async def self_ping():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ksyusha256.onrender.com") as response: pass
        except: pass
        await asyncio.sleep(600)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🎬 Что посмотреть?"), types.KeyboardButton(text="🍕 Что же съесть?"))
    builder.row(types.KeyboardButton(text="💡 Чем заняться?"))
    await message.answer("Бот в сети! Ждем мем.", reply_markup=builder.as_markup(resize_keyboard=True))

movie_photos = {"Майор Гром": "grom.jpg", "Бумажный дом": "bumazh.jpg", "Шрек": "shrek.jpg", "Очень странные дела": "osd.jpg"}
food_photos = {"Макарошки с котлетками": "makarons.jpg", "Бутербродики": "buter.jpg", "Печеночный торт": "tort.jpg", "Квашеная капуста": "kkapusta.jpg", "Пакетик хвостика": "korm.jpg", "Бутербродик с шоколадной пастой": "butersladko.jpg"}
skills = ["Бегит в могазин", "Атжумания", "Пачитат книгу", "Помыть попу", "Покакат", "Покушат", "Поваляца с хвостиком"]

@dp.message(F.text == "🎬 Что посмотреть?")
async def movie_choice(message: types.Message):
    try: await message.answer_photo(photo=FSInputFile(movie_photos[random.choice(list(movie_photos.keys()))]))
    except: await message.answer("Ошибка фото.")

@dp.message(F.text == "🍕 Что же съесть?")
async def food_choice(message: types.Message):
    try: await message.answer_photo(photo=FSInputFile(food_photos[random.choice(list(food_photos.keys()))]))
    except: await message.answer("Ошибка фото.")

@dp.message(F.text == "💡 Чем заняться?")
async def skill_choice(message: types.Message):
    await message.answer(f"🛠 Идея: {random.choice(skills)}")

async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # ТЕСТ НА 12:20 (БЕЗ НУЛЯ ПЕРЕД 20)
    scheduler.add_job(send_scheduled_meme, trigger="cron", hour=12, minute=20, args=(bot,))
    scheduler.start()
    asyncio.create_task(self_ping())
    await dp.start_polling(bot)

if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
