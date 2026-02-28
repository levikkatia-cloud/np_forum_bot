import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Отримуємо дані з налаштувань Render (Environment Variables)
API_TOKEN = os.getenv(8783067050:AAGa88HcpDfuz8Sky5r4tcsIjej6wI2z_8c)
ADMIN_ID = int(os.getenv(NpForumbot, '0'))
USERS_FILE = "users_db.txt"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, 'a').close()
    with open(USERS_FILE, 'r+') as f:
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id}\n")

def get_all_users():
    if not os.path.exists(USERS_FILE): return []
    with open(USERS_FILE, 'r') as f: return f.read().splitlines()

def get_main_menu():
    buttons = [
        [KeyboardButton(text="🗓 Розклад виступів"), KeyboardButton(text="📍 Карта локації")],
        [KeyboardButton(text="📸 Новини з форуму"), KeyboardButton(text="🆘 Отримати допомогу")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    save_user(message.from_user.id)
    text = "🔴 **Вітаємо на @NpForumbot!**\n\nРазом святкуємо 25 років Нової пошти!"
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="Markdown")

@dp.message(F.text == "🗓 Розклад виступів")
async def show_agenda(message: types.Message):
    await message.answer("⏳ **Програма на 19 березня:**\n\n10:00 — Реєстрація\n11:00 — Відкриття", parse_mode="Markdown")

@dp.message(F.text == "📍 Карта локації")
async def show_map(message: types.Message):
    await message.answer("📍 КВЦ «Парковий», 3-й поверх. Карту готуємо!")

@dp.message(F.text == "🆘 Отримати допомогу")
async def ask_help(message: types.Message):
    await message.answer("Напишіть ваше питання сюди 👇, ми відповімо!")

@dp.message(F.text.startswith("Розсилка:"))
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    text = message.text.replace("Розсилка:", "").strip()
    users = get_all_users()
    for user_id in users:
        try: await bot.send_message(user_id, f"🔔 **ОГОЛОШЕННЯ:**\n\n{text}")
        except: pass
    await message.answer("✅ Розсилку відправлено!")

@dp.message()
async def handle_messages(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if message.reply_to_message and "ID:" in message.reply_to_message.text:
            try:
                user_id = message.reply_to_message.text.split("ID:")[1].strip()
                await bot.send_message(user_id, f"✉️ **Відповідь від організаторів:**\n\n{message.text}")
                await message.answer("✅ Відповідь надіслана!")
            except: pass
        return
    await bot.send_message(ADMIN_ID, f"❓ Питання від @{message.from_user.username}:\n{message.text}\n\nID:{message.from_user.id}")
    await message.answer("Повідомлення надіслано організаторам! 🙌")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
