import os
import aiohttp
from Python_ARQ import ARQ
from os import getenv
from dotenv import load_dotenv
from Abhixd.uptools import fetch_heroku_git_url

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
que = {}
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
ARQ_API_KEY = getenv("ARQ_API_KEY")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "★[ᴠᴇxᴇʀᴀ ᴍᴜꜱɪᴄ]★")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/0f6f8a8a5ad69fe5ecf3d.png")
AUD_IMG = getenv("AUD_IMG", "https://telegra.ph/file/3ba727ff3ba2542022dbf.jpg")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/3ba727ff3ba2542022dbf.jpg")
THUMB_IMG = getenv("THUMB_IMG", "https://telegra.ph/file/e258c02de5453faef0d7a.jpg")
BOT_IMG = getenv("BOT_IMG", "https://telegra.ph/file/e954fc1ac5f7aa16d4f91.jpg")
ALIVE_IMG = getenv("ALIVE_IMG", "")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME", "VEXERAMUSICBOT")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "VEXERAMUSIC")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "VEXERA_SUPPORT")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "VEXERA_UPDATES")
OWNER_NAME = getenv("OWNER_NAME", "ABHI_PAGAL") # isi dengan username kamu tanpa simbol @
ALIVE_EMOJI = getenv("ALIVE_EMOJI", "🌻")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/aa63b2b2cb28b357140a7.png")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/d13a980aa20a9c6af069b.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/0f6f8a8a5ad69fe5ecf3d.png")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", "False"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
DATABASE_URL = os.environ.get("DATABASE_URL")
OWNER_ID = int(os.environ.get("OWNER_ID"))
PMPERMIT = getenv("PMPERMIT", "ENABLE")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! . x as # , @").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
# UPDATER CONFIG
U_BRANCH = "main"
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/ABHI-xd/VEXERA-MUSIC")
HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)

aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
