import sys
import os
import time
import traceback
import asyncio
import shutil
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message, Dialog, Chat
from pyrogram.errors import UserAlreadyParticipant
from datetime import datetime
from functools import wraps
from os import environ, execle, path, remove

from callsmusic.callsmusic import client as pakaya
from Abhixd.decorators import sudo_users_only
from vexera.song import humanbytes, get_text
from config import SUDO_USERS, SUPPORT_GROUP


# Stats Of Your Bot
@Client.on_message(filters.command("stats"))
@sudo_users_only
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    await message.reply_text(
        text=f"📊 𝗦𝘁𝗮𝘁𝘀  \n\n**🤖 Vᴇʀꜱɪᴏɴ:** `v8.3` \n\n**💾 𝗗𝗶𝘀𝗸 𝗨𝘀𝗮𝗴𝗲,** \n » **Dɪꜱᴋ Sᴘᴀᴄᴇ:** `{total}` \n » **Uꜱᴇᴅ:** `{used}({disk_usage}%)` \n » **Fʀᴇᴇ:** `{free}` \n\n**🎛 𝗛𝗮𝗿𝗱𝘄𝗮𝗿𝗲 𝗨𝘀𝗮𝗴𝗲,** \n » **CPU Uꜱᴀɢᴇ:** `{cpu_usage}%` \n » **RAM Uꜱᴀɢᴇ:** `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True
    )
