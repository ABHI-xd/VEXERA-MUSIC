import json
import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import Voice
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch

#addyxd
from config import BOT_USERNAME
from config import ARQ_API_KEY
from config import BOT_NAME as bn
from config import DURATION_LIMIT
from config import UPDATES_CHANNEL as updateschannel
from config import que
from function.admins import admins as a
from Abhixd.admins import get_administrators
from Abhixd.channelmusic import get_chat_id
from Abhixd.errors import DurationLimitError
from Abhixd.decorators import errors
from Abhixd.decorators import authorized_users_only
from Abhixd.filters import command, other_filters
from Abhixd.gets import get_file_name
from callsmusic import callsmusic
from callsmusic.callsmusic import client as USER
from converter.converter import convert
from downloaders import youtube
from callsmusic.queues import queues

aiohttpsession = aiohttp.ClientSession()
chat_id = None
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
DISABLED_GROUPS = []
useer ="NaN"
def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("Yᴏᴜ Aʀᴇ Nᴏᴛ Aʟʟᴏᴡᴇᴅ!", show_alert=True)
            return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("./etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.ttf", 60)
    draw.text((40, 550), f"Playing here...", (0, 0, 0), font=font)
    draw.text((985, 20), f"A KabeerXCode", fill="white", font=font)
    draw.text((1100, 50), f"Project", fill="white", font=font)
    draw.text((40, 630),
        f"{title}",
        (0, 0, 0),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(command(["playlist", f"playlist@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return    
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("Nᴏᴛʜɪɴɢ Iꜱ Pʟᴀʏɪɴɢ")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "Pʟᴀʏɪɴɢ Aᴛ {}".format(message.chat.title)
    msg += "\n\n- " + now_playing
    msg += "\n-Fᴏʀ " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "𝐐𝐮𝐞𝐮𝐞"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n-Fᴏʀ {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐨𝐟 **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "𝐕𝐨𝐥𝐮𝐦𝐞 : {}%\n".format(vol)
            stats += "𝐒𝐨𝐧𝐠𝐬 𝐢𝐧 𝐪𝐮𝐞𝐮𝐞 : `{}`\n".format(len(que))
            stats += "𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 : **{}**\n".format(queue[0][0])
            stats += "𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲 : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
            ],
            [
                InlineKeyboardButton("𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 📖", "playlist"),
            ],
            [InlineKeyboardButton("❌Cʟᴏꜱᴇ", "cls")],
        ]
    )
    return mar


@Client.on_message(command(["current", f"current@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def ee(client, message):
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("𝐍𝐨 𝐕𝐂 𝐢𝐧𝐬𝐭𝐚𝐧𝐜𝐞𝐬 𝐫𝐮𝐧𝐧𝐢𝐧𝐠 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭")


@Client.on_message(command(["player", f"player@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    if message.chat.id in DISABLED_GROUPS:
        await message.reply("𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐢𝐬 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝")
        return    
    playing = None
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(chat_id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("𝐍𝐨 𝐕𝐂 𝐢𝐧𝐬𝐭𝐚𝐧𝐜𝐞𝐬 𝐫𝐮𝐧𝐧𝐢𝐧𝐠 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭")


@Client.on_message(
    filters.command("musicplayer") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "I only recognize `/musicplayer on` and /musicplayer `off only`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await message.reply("`ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 𝐅𝐨𝐫 𝐔𝐬𝐞𝐫𝐬 𝐈𝐧 𝐓𝐡𝐞 𝐂𝐡𝐚𝐭 {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await message.reply("`ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌`")
        
        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐭𝐮𝐫𝐧𝐞𝐝 𝐨𝐟𝐟 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐞𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐅𝐨𝐫 𝐔𝐬𝐞𝐫𝐬 𝐈𝐧 𝐓𝐡𝐞 𝐂𝐡𝐚𝐭 {message.chat.id}"
        )
    else:
        await message.reply_text(
            "I only recognize `/musicplayer on` and /musicplayer `off only`"
        )    
        

@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("𝐏𝐥𝐚𝐲𝐞𝐫 𝐢𝐬 𝐢𝐝𝐥𝐞")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "Pʟᴀʏɪɴɢ Aᴛ {}".format(cb.message.chat.title)
        msg += "\n\n- " + now_playing
        msg += "\n-Fᴏʀ " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "𝐐𝐮𝐞𝐮𝐞"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n-Fᴏʀ {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("𝐂𝐡𝐚𝐭 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("𝐌𝐮𝐬𝐢𝐜 𝐏𝐚𝐮𝐬𝐞𝐝!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "play":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("𝐂𝐡𝐚𝐭 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("𝐌𝐮𝐬𝐢𝐜 𝐑𝐞𝐬𝐮𝐦𝐞𝐝!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("𝐏𝐥𝐚𝐲𝐞𝐫 𝐢𝐬 𝐢𝐝𝐥𝐞")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "Pʟᴀʏɪɴɢ Aᴛ {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n-Fᴏʀ " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "𝐐𝐮𝐞𝐮𝐞"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n-Fᴏʀ {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "resume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("𝐂𝐡𝐚𝐭 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐨𝐫 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐩𝐥𝐚𝐲𝐢𝐧𝐠", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("𝐌𝐮𝐬𝐢𝐜 𝐑𝐞𝐬𝐮𝐦𝐞𝐝!")
    elif type_ == "puse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("𝐂𝐡𝐚𝐭 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐨𝐫 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐩𝐚𝐮𝐬𝐞𝐝", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("𝐌𝐮𝐬𝐢𝐜 𝐏𝐚𝐮𝐬𝐞𝐝!")
    elif type_ == "cls":
        await cb.answer("Closed menu")
        await cb.message.delete()

    elif type_ == "menu":
        stats = updated_stats(cb.message.chat, qeue)
        await cb.answer("Menu opened")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 📖", "playlist"),
                ],
                [InlineKeyboardButton("❌Cʟᴏꜱᴇ", "cls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "skip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("𝐂𝐡𝐚𝐭 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝!", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("- 𝐍𝐨 𝐌𝐨𝐫𝐞 𝐏𝐥𝐚𝐲𝐥𝐢𝐬𝐭..\𝐧- 𝐋𝐞𝐚𝐯𝐢𝐧𝐠 𝐕𝐂!")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("Skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- 𝐒𝐤𝐢𝐩𝐩𝐞𝐝 𝐭𝐫𝐚𝐜𝐤\𝐧- 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 **{qeue[0][0]}**"
                )

    else:
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐋𝐞𝐟𝐭 𝐭𝐡𝐞 𝐂𝐡𝐚𝐭!")
        else:
            await cb.answer("𝐂𝐡𝐚𝐭 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝!", show_alert=True)


@Client.on_message(command("play") & other_filters)
async def play(_, message: Message):
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return    
    lel = await message.reply("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>Remember to add helper to your channel</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>𝐀𝐝𝐝 𝐦𝐞 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐟𝐢𝐫𝐬𝐭 𝐰𝐢𝐭𝐡 𝐚𝐥𝐥 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "𝐈 𝐣𝐨𝐢𝐧𝐞𝐝 𝐭𝐡𝐢𝐬 𝐠𝐫𝐨𝐮𝐩 𝐟𝐨𝐫 𝐩𝐥𝐚𝐲𝐢𝐧𝐠 𝐦𝐮𝐬𝐢𝐜♩ 𝐢𝐧 𝐕𝐂"
                    )
                    await lel.edit(
                        "<b>𝐇𝐞𝐥𝐩𝐞𝐫 𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐣𝐨𝐢𝐧𝐞𝐝 𝐲𝐨𝐮𝐫 𝐜𝐡𝐚𝐭</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 𝐅𝐥𝐨𝐨𝐝 𝐖𝐚𝐢𝐭 𝐄𝐫𝐫𝐨𝐫 🔴 \n𝐔𝐬𝐞𝐫 {user.first_name} 𝐜𝐨𝐮𝐥𝐝𝐧'𝐭 𝐣𝐨𝐢𝐧 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐝𝐮𝐞 𝐭𝐨 𝐡𝐞𝐚𝐯𝐲 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬 𝐟𝐨𝐫 𝐮𝐬𝐞𝐫𝐛𝐨𝐭! 𝐌𝐚𝐤𝐞 𝐬𝐮𝐫𝐞 𝐮𝐬𝐞𝐫 𝐢𝐬 𝐧𝐨𝐭 𝐛𝐚𝐧𝐧𝐞𝐝 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩.</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐧𝐨𝐭 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭, 𝐀𝐬𝐤 𝐚𝐝𝐦𝐢𝐧 𝐭𝐨 𝐬𝐞𝐧𝐝 /userbotjoin 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐟𝐨𝐫 𝐟𝐢𝐫𝐬𝐭 𝐭𝐢𝐦𝐞 𝐨𝐫 𝐚𝐝𝐝 {user.first_name} 𝐦𝐚𝐧𝐮𝐚𝐥𝐥𝐲</i>"
        )
        return
    text_links=None
    await lel.edit("ıllıllı **Fιɳԃιɳɠ**ıllıllı  ♩✌")
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ 𝐕𝐢𝐝𝐞𝐨𝐬 𝐥𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐦𝐢𝐧𝐮𝐭𝐞(𝐬) 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲!"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁", callback_data="playlist"),
                    InlineKeyboardButton("𝗠𝗲𝗻𝘂 ⏯  ", callback_data="menu"),
                ],
                [InlineKeyboardButton(text="❌Cʟᴏꜱᴇ", callback_data="cls")],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/f6086f8909fbfeb0844f2.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲."
            )
            print(str(e))
            return
        dlurl=url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton(text="🎬 𝗬𝗧", url=f"{url}"),
                  InlineKeyboardButton(text="𝗦𝗮𝘃𝗲 📥", url=f"{dlurl}"),
                ],
                 [InlineKeyboardButton(text="❌Cʟᴏꜱᴇ", callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        
        try:
          results = YoutubeSearch(query, max_results=5).to_dict()
        except:
          await lel.edit("𝐆𝐢𝐯𝐞 𝐦𝐞 𝐬𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐭𝐨 𝐩𝐥𝐚𝐲")
        # Looks like hell. Aren't it?? FUCK OFF
        try:
            toxxt = "**🥳𝐂𝐡𝐨𝐨𝐬𝐞 𝐘𝐨𝐮𝐫 𝐒𝐨𝐧𝐠**\n\n"
            j = 0
            useer=user_name
            emojilist = ["1","2","3","4","5","6"]

            while j < 5:
                toxxt += f"{emojilist[j]} [{results[j]['title']}](https://youtube.com{results[j]['url_suffix']})\n"
                toxxt += f" ├ 🙃 ᴅᴜʀᴀᴛɪᴏɴ - {results[j]['duration']}\n"
                toxxt += f" └ 𝗔ᴅᴅʏ 𝗣ᴏᴡᴇʀᴇᴅ💜\n\n"
                j += 1            
            koyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1", callback_data=f'plll 0|{query}|{user_id}'),
                        InlineKeyboardButton("2", callback_data=f'plll 1|{query}|{user_id}'),
                        InlineKeyboardButton("3", callback_data=f'plll 2|{query}|{user_id}'),
                    ],
                    [
                        InlineKeyboardButton("4", callback_data=f'plll 3|{query}|{user_id}'),
                        InlineKeyboardButton("5", callback_data=f'plll 4|{query}|{user_id}'),
                    ],
                    [InlineKeyboardButton(text="❌ᑕᒪOSE", callback_data="cls")],
                ]
            )       
            await lel.edit(toxxt,reply_markup=koyboard,disable_web_page_preview=True)
            # WHY PEOPLE ALWAYS LOVE PORN ?? (A point to think)
            # Kanged by @AddyxD
            return
            # Returning to pornhub
        except:
            await lel.edit("𝐍𝐨 𝐄𝐧𝐨𝐮𝐠𝐡 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐭𝐨 𝐜𝐡𝐨𝐨𝐬𝐞.. 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐝𝐢𝐫𝐞𝐜𝐭 𝐩𝐥𝐚𝐲..")
                        
            # print(results)
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"thumb{title}.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                views = results[0]["views"]

            except Exception as e:
                await lel.edit(
                    "𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲."
                )
                print(str(e))
                return
            dlurl=url
            dlurl=dlurl.replace("youtube","youtubepp")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝗠𝗲𝗻𝘂 ⏯ ", callback_data="menu"),
                    ],
                    [
                        InlineKeyboardButton(text="🎬 𝗬𝗧", url=f"{url}"),
                        InlineKeyboardButton(text="𝗦𝗮𝘃𝗲 📥", url=f"{dlurl}"),
                    ],
                    [InlineKeyboardButton(text="❌Cʟᴏꜱᴇ", callback_data="cls")],
                ]
            )
            requested_by = message.from_user.first_name
            await generate_cover(requested_by, title, views, duration, thumbnail)
            file_path = await convert(youtube.download(url))   
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"#⃣ 𝐘𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠 **queued** 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("𝐆𝐫𝐨𝐮𝐩 𝐂𝐚𝐥𝐥 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐨𝐫 𝐈 𝐜𝐚𝐧'𝐭 𝐣𝐨𝐢𝐧 𝐢𝐭")
            return
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="𝗡ᴏᴡ 𝗣ʟᴀʏɪɴɢ 𝗙ᴏʀ {} ".format(
                message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()
    
@Client.on_message(filters.command("ytplay") & filters.group & ~filters.edited)
async def ytplay(_, message: Message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>Remember to add helper to your channel</b>",
                    )
                    pass
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>𝐀𝐝𝐝 𝐦𝐞 𝐚𝐬 𝐚𝐝𝐦𝐢𝐧 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐟𝐢𝐫𝐬𝐭 𝐰𝐢𝐭𝐡 𝐚𝐥𝐥 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "𝐈 𝐣𝐨𝐢𝐧𝐞𝐝 𝐭𝐡𝐢𝐬 𝐠𝐫𝐨𝐮𝐩 𝐟𝐨𝐫 𝐩𝐥𝐚𝐲𝐢𝐧𝐠 𝐦𝐮𝐬𝐢𝐜♩ 𝐢𝐧 𝐕𝐂"
                    )
                    await lel.edit(
                        "<b>𝐇𝐞𝐥𝐩𝐞𝐫 𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐣𝐨𝐢𝐧𝐞𝐝 𝐲𝐨𝐮𝐫 𝐜𝐡𝐚𝐭</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 𝐅𝐥𝐨𝐨𝐝 𝐖𝐚𝐢𝐭 𝐄𝐫𝐫𝐨𝐫 🔴 \n𝐔𝐬𝐞𝐫 {user.first_name} 𝐜𝐨𝐮𝐥𝐝𝐧'𝐭 𝐣𝐨𝐢𝐧 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩 𝐝𝐮𝐞 𝐭𝐨 𝐡𝐞𝐚𝐯𝐲 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬 𝐟𝐨𝐫 𝐮𝐬𝐞𝐫𝐛𝐨𝐭! 𝐌𝐚𝐤𝐞 𝐬𝐮𝐫𝐞 𝐮𝐬𝐞𝐫 𝐢𝐬 𝐧𝐨𝐭 𝐛𝐚𝐧𝐧𝐞𝐝 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩."
                        "\n\n𝐎𝐫 𝐦𝐚𝐧𝐮𝐚𝐥𝐥𝐲 𝐚𝐝𝐝 𝐚𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 @MusicAssistantOfCarnival 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 𝐚𝐧𝐝 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐧𝐨𝐭 𝐢𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭, 𝐀𝐬𝐤 𝐚𝐝𝐦𝐢𝐧 𝐭𝐨 𝐬𝐞𝐧𝐝 /userbotjoin 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐟𝐨𝐫 𝐟𝐢𝐫𝐬𝐭 𝐭𝐢𝐦𝐞 𝐨𝐫 𝐚𝐝𝐝 {user.first_name} 𝐦𝐚𝐧𝐮𝐚𝐥𝐥𝐲</i>"
        )
        return
    await lel.edit("ıllıllı **Fιɳԃιɳɠ**ıllıllı  ♩✌")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
     

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit(
            "𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲."
        )
        print(str(e))
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton(text="🎬 𝗬𝗧", url=f"{url}"),
                  InlineKeyboardButton(text="𝗦𝗮𝘃𝗲 📥", url=f"{dlurl}"),
                ],
                 [InlineKeyboardButton(text="❌Cʟᴏꜱᴇ", callback_data="cls")],
            ]
    )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"#⃣ 𝐘𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠 **queued** 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("𝐆𝐫𝐨𝐮𝐩 𝐂𝐚𝐥𝐥 𝐢𝐬 𝐧𝐨𝐭 𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐞𝐝 𝐨𝐫 𝐈 𝐜𝐚𝐧'𝐭 𝐣𝐨𝐢𝐧 𝐢𝐭")
            return
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="𝗡ᴏᴡ 𝗣ʟᴀʏɪɴɢ 𝗙ᴏʀ {} ".format(
                message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()
    
@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que

    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_=cbd.split(None, 1)[1]
    #useer_id = cb.message.reply_to_message.from_user.id
    try:
        x,query,useer_id = typed_.split("|")      
    except:
        await cb.message.edit("𝐒𝐨𝐧𝐠 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("𝐘𝐨𝐮 𝐚𝐢𝐧'𝐭 𝐭𝐡𝐞 𝐩𝐞𝐫𝐬𝐨𝐧 𝐰𝐡𝐨 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠!", show_alert=True)
        return
    await cb.message.edit("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐖𝐚𝐢𝐭...💘")
    x=int(x)
    try:
        useer_name = cb.message.reply_to_message.from_user.first_name
    except:
        useer_name = cb.message.from_user.first_name
    
    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss=results[x]["url_suffix"]
    title=results[x]["title"][:40]
    thumbnail=results[x]["thumbnails"][0]
    duration=results[x]["duration"]
    views=results[x]["views"]
    url = f"https://youtube.com{resultss}"
    
    try:    
        duuration= round(duration / 60)
        if duuration > DURATION_LIMIT:
            await cb.message.edit(f"𝐌𝐮𝐬𝐢𝐜 𝐥𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 {DURATION_LIMI} 𝐦𝐢𝐧 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲")
            return
    except:
        pass
    try:
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl=url
    dlurl=dlurl.replace("youtube","youtubepp")
    keyboard = InlineKeyboardMarkup(
            [
                [
                  InlineKeyboardButton("𝗠𝗲𝗻𝘂 ⏯ ", callback_data="menu"),
                ],
                [
                  InlineKeyboardButton(text="🎬 𝗬𝗧", url=f"{url}"),
                  InlineKeyboardButton(text="𝗦𝗮𝘃𝗲 📥", url=f"{dlurl}"),
                ],
                [InlineKeyboardButton(text="❌Cʟᴏꜱᴇ", callback_data="cls")],
            ]
    )
    requested_by = useer_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await convert(youtube.download(url))  
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(chat_id,
            photo="final.png",
            caption=f"#⃣  𝐒𝐨𝐧𝐠 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲 {r_by.mention} **queued** 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        qeue.append(appendable)
        try:
            await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            await cb.message.delete()
            await b.send_photo(chat_id,
            photo="final.png",
            reply_markup=keyboard,
            caption=f"▶️ 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 𝗵𝗲𝗿𝗲 𝘁𝗵𝗲 𝘀𝗼𝗻𝗴 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗯𝘆 {r_by.mention} \n 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 : {duration} \n ",
        )
        os.remove("final.png")
