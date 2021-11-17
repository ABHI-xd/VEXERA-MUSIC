import asyncio
from pytgcalls import idle
from Abhixd.snehabhi import call_py, bot

async def mulai_bot():
    print("[VEXERA MUSIC]: STARTING BOT CLIENT")
    await bot.start()
    print("[VEXERA MUSIC]: STARTING PYTGCALLS CLIENT")
    await call_py.start()
    await idle()
    await pidle()
    print("[VEXERA MUSIC]: STOPPING BOT & USERBOT")
    await bot.stop()
print(f"[INFO]: VEXERA MUSIC STARTED !")

loop = asyncio.get_event_loop()
loop.run_until_complete(mulai_bot())





