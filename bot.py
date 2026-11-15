import asyncio, time, json, os
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8683133632:AAGagr__2eD8a9jyBcgGVW8trQtLx4zNzyE"
ADMIN_ID = 0  # o'z Telegram ID'ingiz (ixtiyoriy)

BYPASS_URL = "http://127.0.0.1:2233/delta"  # delta-bypass server manzili
LINK_FILE = "link.txt"  # yangi havola shu faylga yoziladi

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Boshlang'ich havola
key_link = ("https://auth.platorelay.com/a?d=6sF6xR2QHSqhaQv7MqjvuFbP3xvQHHGrVgNG7YD9bxI60PjHnZsp9yFwCGVcoCvcGJr7g8nEpv6jKWMNUtPUp7LyQReplZNCUKrkTV2NZAn2LFZ0LTicX1RJf6xSrXcgvK1qX0ZcBy5a3LGDz8zKjMoXRhrGHLbjp2GctfRCdYzrc265ziZRVFoWyv15F8f5cWfcpRqNw6bxXrIdKHltGdbl7Qu53CSSnjjGR9rUGKzaCGSuWll0tvNYtUDL4yVMmtrl0UtSdmmytQGwkhMgvGjc7aihXGaIOQ9jYuphq5gPc0bGZwcwOD2fuQypd4ZO8iNYQNBgnaVBivjlhZ0rEIuRcs5OmvOG57SMZSD4Ijkk1LxqAxF51bvBXiv7JnjttRy7DecTkG140WVu3Rzz91OtXxmCi08QIux8UNYsy7Mqauh4BGB4ko9Ha1cT9KOaXsCn5jzA24v4o1NNHjipq1KLYCuJxlxSKhQFwsA38aUK70h3ghg")

# Fayldan saqlangan havolani yuklash
if os.path.exists(LINK_FILE):
    with open(LINK_FILE) as f:
        key_link = f.read().strip()


def main_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔑 Get Delta Key", callback_data="get_key")
    kb.button(text="✅ Receive Key", callback_data="receive_key")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "👋 <b>Delta Key Bot</b>ga xush kelibsiz!\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_keyboard()
    )


@dp.callback_query(lambda c: c.data == "get_key")
async def get_key(cb: types.CallbackQuery):
    await cb.message.answer("⏳ Kalit olinmoqda, 10-15 soniya kuting...")
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.get(BYPASS_URL, params={"url": key_link})
            data = r.json()
        if data.get("key"):
            await cb.message.answer(
                f"✅ <b>Kalitingiz tayyor:</b>\n\n<code>{data['key']}</code>\n\n"
                f"⏱ Bajarilish vaqti: {data.get('times','?')}"
            )
        else:
            err = data.get("error") or "Noma'lum xato"
            await cb.message.answer(f"❌ Kalit olinmadi: {err}\n\n"
                                    "Admin yangi havola qo'ysin: /setkey <havola>")
    except Exception as e:
        await cb.message.answer(f"❌ Server bilan aloqa xatosi: {e}")


@dp.callback_query(lambda c: c.data == "receive_key")
async def receive_key(cb: types.CallbackQuery):
    await cb.message.answer(
        "📋 Yuqoridagi kalitni nusxalab, Delta Executor'ning key oynasiga joylashtiring."
    )


@dp.message(Command("setkey"))
async def setkey(msg: types.Message):
    global key_link
    if ADMIN_ID and msg.from_user.id != ADMIN_ID:
        await msg.answer("❌ Sizda ruxsat yo'q.")
        return
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer("Foydalanish: /setkey <havola>")
        return
    key_link = parts[1].strip()
    with open(LINK_FILE, "w") as f:
        f.write(key_link)
    await msg.answer("✅ Yangi havola saqlandi va key faylga yozildi!")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
