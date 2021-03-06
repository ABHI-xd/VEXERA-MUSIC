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
from config import SUDO_USERS, GROUP_SUPPORT


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
        text=f"๐ ๐ฆ๐๐ฎ๐๐  \n\n**๐ค Vแดส๊ฑษชแดษด:** `v8.3` \n\n**๐พ ๐๐ถ๐๐ธ ๐จ๐๐ฎ๐ด๐ฒ,** \n ยป **Dษช๊ฑแด Sแดแดแดแด:** `{total}` \n ยป **U๊ฑแดแด:** `{used}({disk_usage}%)` \n ยป **Fสแดแด:** `{free}` \n\n**๐ ๐๐ฎ๐ฟ๐ฑ๐๐ฎ๐ฟ๐ฒ ๐จ๐๐ฎ๐ด๐ฒ,** \n ยป **CPU U๊ฑแดษขแด:** `{cpu_usage}%` \n ยป **RAM U๊ฑแดษขแด:** `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True
    )
