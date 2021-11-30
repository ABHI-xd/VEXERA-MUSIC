import os
import shutil
import sys
import traceback
from functools import wraps
from os import environ, execle

import heroku3
import psutil
from config import OWNER_ID


from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from vexera.song import get_text, humanbytes
from vexera import __version__
from Abhixd.database import db
from Abhixd.dbtools import main_broadcast_handler
from Abhixd.decorators import sudo_users_only
from Abhixd.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(
    filters.private
    & filters.command("broadcast")
    & filters.user(OWNER_ID)
    & filters.reply
)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)
