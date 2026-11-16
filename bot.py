import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8683133632:AAGagr__2eD8a9jyBcgGVW8trQtLx4zNzyE"
BYPASS_URL = "http://127.0.0.1:2233/delta"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "👋 <b>Delta Key Bot</b>ga xush kelibsiz!\n\n"
        "🔗 Delta key havolangizni (auth.platorelay.com / auth.platoboost.app) "
        "shu chatga tashlang — men kalitni olib beraman.\n\n"
        "ℹ️ Har bir havola faqat bir marta ishlaydi. Yangi kalit uchun "
        "Delta Executor'dan yangi havola olib tashlang."
    )


# Foydalanuvchi havola tashlaganda ishlaydi
@dp.message(lambda m: m.text and ("platorelay.com" in m.text or "platoboost" in m.text))
async def handle_link(msg: types.Message):
    link = msg.text.strip().split()[0]  # faqat birinchi havola olindi

    status = await msg.answer("⏳ Kalit olinmoqda, 10-15 soniya kuting...")
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            r = await client.get(BYPASS_URL, params={"url": link})
            data = r.json()
    except Exception as e:
        await status.edit_text(f"❌ Server bilan aloqa xatosi: {e}")
        return

    if data.get("key"):
        await status.edit_text(
            f"✅ <b>Kalitingiz tayyor:</b>\n\n"
            f"<code>{data['key']}</code>\n\n"
            f"📋 Shu kalitni nusxalab, Delta Executor'dagi key oynasiga joylashtiring.\n"
            f"⏱ Vaqt: {data.get('times', '?')}"
        )
    else:
        err = data.get("error") or "Noma'lum xato"
        await status.edit_text(
            f"❌ Kalit olinmadi:\n<b>{err}</b>\n\n"
            "💡 Havola eskirgan bo'lishi mumkin — Delta Executor'dan yangi "
            "havola olib qayta tashlang."
        )


# Boshqa har qanday xabar uchun yordam
@dp.message()
async def fallback(msg: types.Message):
    await msg.answer(
        "🤖 Menga Delta key havolasini tashlang "
        "(auth.platorelay.com bilan boshlanadigan havola)."
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
