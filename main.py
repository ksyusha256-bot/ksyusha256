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
    VK_TOKEN = 'f1cd8672f1cd8672f1cd867284f2f316d0ff1cdf1cd867298bb898200940aaf45fbe5e9'
    GROUP_ID = '-460389' 
    
    # ВОТ ИСПРАВЛЕННАЯ ССЫЛКА:
    url = f"https://api.vk.com/method/wall.get?owner_id={GROUP_ID}&count=50&access_token={VK_TOKEN}&v=5.131"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if 'error' in data:
                    print(f"Ошибка ВК: {data['error']['error_msg']}")
                    return None
                posts = data['response']['items']
                images = []
                for post in posts:
                    if 'attachments' in post:
                        for att in post['attachments']:
                            if att['type'] == 'photo':
                                photo_url = att['photo']['sizes'][-1]['url']
                                images.append(photo_url)
                if images:
                    return random.choice(images)
    except Exception as e:
        print(f"Ошибка при запросе к ВК: {e}")
    return None

async def send_scheduled_meme(bot: Bot):
    meme_url = await get_random_meme()
    if meme_url:
        for user_id in USER_IDS:
            try:
                await bot.send_photo(chat_id=user_id, photo=meme_url, caption="✨ Ежедневный мем!")
            except: pass

async def rem_1(bot: Bot):
    try: await bot.send_message(chat_id=650682969, text="🌸 Ксю, сегодня 1-е число! Выбери категории в сберпрайме! Мяу.")
    except: pass

async def rem_11(bot: Bot):
    for uid in USER_IDS:
        try: await bot.send_message(chat_id=uid, text="🙄 Сегодня 11-е число йоу! Позвони Изабэле и договорись насчет завтра! ✨🌺🎉")
        except: pass

async def rem_12(bot: Bot):
    for uid in USER_IDS:
        try: await bot.send_message(chat_id=uid, text="📅 Сегодня уже 12-е число епта! Пора позвонить Изабэле и попрощаться с бабками! 😿💔💸 Вот Черт!")
        except: pass

async def rem_22(bot: Bot):
    for uid in USER_IDS:
        try: await bot.send_message(chat_id=uid, text="🤡 Приветики! Напоминаю, что завтра нужно скинуть счетчики за воду и свет! 🥀🌈🏆")
        except: pass

async def rem_23(bot: Bot):
    for uid in USER_IDS:
        try: await bot.send_message(chat_id=uid, text="🗓️ Здарова! Не забудь скинуть счетчики хозяйке и в почтовый ящик. Я же вчера напоминал тебе, ты чего блин? ✨🌙☁️ ")
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
    # Отправляем команду на удаление кнопок
    await message.answer("Бот в сети! 🌺 ", reply_markup=types.ReplyKeyboardRemove())

async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    
    # ТЕСТ: поставил на 16:30, чтобы ты успела загрузить!
    scheduler.add_job(send_scheduled_meme, trigger="cron", hour=15, minute=30, args=(bot,))
    
    scheduler.add_job(rem_1,  trigger="cron", day="1",  hour=6, minute=0, args=(bot,))
    scheduler.add_job(rem_11, trigger="cron", day="11", hour=9, minute=0, args=(bot,))
    scheduler.add_job(rem_12, trigger="cron", day="12", hour=9, minute=0, args=(bot,))
    scheduler.add_job(rem_22, trigger="cron", day="22", hour=9, minute=0, args=(bot,))
    scheduler.add_job(rem_23, trigger="cron", day="23", hour=9, minute=0, args=(bot,))
    
    scheduler.start()
    asyncio.create_task(self_ping())
    await dp.start_polling(bot)

if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())