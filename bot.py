import logging
logging.basicConfig(level=logging.DEBUG)
import os
os.makedirs("downloads", exist_ok=True)
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv

from spotify import get_track_info
from downloader import search_youtube, download_by_url

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Старт
@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.reply("Привет! Пришли ссылку на трек из Spotify или просто название, и я найду тебе mp3 ✨")

# Ссылка на Spotify
@dp.message_handler(lambda message: "open.spotify.com/track/" in message.text)
async def handle_spotify_link(message: Message):
    await message.reply("Ищу трек по ссылке... 🎧")
    track_info = get_track_info(message.text)
    if "Ошибка" in track_info:
        await message.reply(f"Не удалось получить трек: {track_info}")
        return

    await show_search_results(message, track_info)

# Поиск по названию
@dp.message_handler()
async def handle_text_query(message: Message):
    query = message.text.strip()
    await show_search_results(message, query)

# Показываем кнопки с треками
async def show_search_results(message, query):
    await message.reply("Ищу... 🔍")

    results = search_youtube(query)

    if not results:
        await message.reply("Ничего не нашла 😥 Попробуй уточнить название.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in results:
        title = item["title"]
        url = item["url"]
        dur = item["duration"]
        mins = dur // 60
        secs = dur % 60
        keyboard.add(InlineKeyboardButton(text=f"{title} [{mins}:{secs:02d}]", callback_data=url))

    await message.reply("Выбери нужный трек:", reply_markup=keyboard)

@dp.callback_query_handler()
async def handle_selection(callback: CallbackQuery):
    print(f"⚡️ КНОПКА НАЖАТА: callback.data = {callback.data}")
    await bot.answer_callback_query(callback.id, text="Скачиваю... 🎧", show_alert=False)

    try:
        file_path = download_by_url(callback.data)

        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            await bot.send_message(callback.from_user.id, f"😥 Не удалось скачать.\n<b>file_path:</b> {file_path}", parse_mode="HTML")
            return

        with open(file_path, "rb") as audio:
            await bot.send_audio(callback.from_user.id, audio, caption="@Sposhleybot")

        os.remove(file_path)

    except Exception as e:
        await bot.send_message(callback.from_user.id, f"⚠️ Произошла ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, allowed_updates=["message", "callback_query"])