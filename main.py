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
USERS-IDS = [662501989, 650682969] 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask('')

# --- ДАННЫЕ ---
movie_photos = {
    "Майор Гром": "grom.jpg", "Бумажный дом": "bumazh.jpg",
    "Шрек": "shrek.jpg", "Очень странные дела": "osd.jpg"
}
food_photos = {
    "Макарошки с котлетками": "makarons.jpg", "Бутербродики": "buter.jpg",
    "Печеночный торт": "tort.jpg", "Квашеная капуста": "kkapusta.jpg",
    "Пакетик хвостика": "korm.jpg", "Бутербродик с шоколадной пастой": "butersladko.jpg"
}
skills = ["Бегит в могазин", "Атжумания", "Пачитат книгу", "Помыть попу", "Покакат", "Покушат", "Поваляца с хвостиком"]

# --- МИНИ-САЙТ ДЛЯ RENDER ---
@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ФУНКЦИИ ПЛАНИРОВЩИКА ---
async def get_random_meme():
    """Берем случайную собачку (самый стабильный источник)"""
    url = "https://dog.ceo"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('message')
    except Exception as e:
        print(f"Ошибка поиска мема: {e}")
    return None

async def send_scheduled_meme(bot: Bot):
    meme_url = await get_random_meme()
    if meme_url:
        for user_id in USER_IDS:
            try:
                await bot.send_photo(chat_id=user_id, photo=meme_url, caption="✨ Ежедневный мем для вас!")
            except Exception as e:
                print(f"Ошибка отправки пользователю {user_id}: {e}")

async def self_ping():
    """Бот сам заходит на свою страницу, чтобы не уснуть"""
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                # ЗАМЕНИ ЭТУ ССЫЛКУ НА СВОЮ, если она отличается:
                async with session.get("https://ksyusha256.onrender.com") as response:
                    print(f"Самопроверка: {response.status}")
        except:
            print("Самопроверка не удалась")
        await asyncio.sleep(600) # Спит 10 минут

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🎬 Что посмотреть?"), types.KeyboardButton(text="🍕 Что же съесть?"))
    builder.row(types.KeyboardButton(text="💡 Чем заняться?"))
    await message.answer("Привет! Я работаю в облаке 24/7. Выбери категорию:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "🎬 Что посмотреть?")
async def movie_choice(message: types.Message):
    try:
        movie = random.choice(list(movie_photos.keys()))
        await message.answer_photo(photo=FSInputFile(movie_photos[movie]), caption=f"🎬 Глянь '{movie}'!")
    except: await message.answer("Ошибка с фото кино.")

@dp.message(F.text == "🍕 Что же съесть?")
async def food_choice(message: types.Message):
    try:
        dish = random.choice(list(food_photos.keys()))
        await message.answer_photo(photo=FSInputFile(food_photos[dish]), caption=f"😋 Как насчет: {dish}?")
    except: await message.answer("Ошибка с фото еды.")

@dp.message(F.text == "💡 Чем заняться?")
async def skill_choice(message: types.Message):
    await message.answer(f"🛠 Идея: {random.choice(skills)}")

# --- ЗАПУСК ---
async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # Каждый день в 11:35
    scheduler.add_job(send_scheduled_meme, trigger="cron", hour=11, minute=35, args=(bot,))
    scheduler.start()
    
    # Запускаем само-будильник фоном
    asyncio.create_task(self_ping())
    
    print("Бот и планировщик (10:00) запущены!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    keep_alive() # Запуск Flask
    asyncio.run(main())


