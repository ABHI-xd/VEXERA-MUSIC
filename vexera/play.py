import asyncio
import re

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, BOT_NAME

from Abhixd.filters import command, other_filters
from Abhixd.queues import QUEUE, add_to_queue
from Abhixd.snehabhi import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• 𝐦𝐞𝐧𝐮", callback_data="cbmenu"),
                InlineKeyboardButton(text="• 𝐜𝐥𝐨𝐬𝐞", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("𝐘𝐨𝐮'𝐫𝐞 𝐚𝐧 __Anonymous Admin__ !\n\n» 𝐫𝐞𝐯𝐞𝐫𝐭 𝐛𝐚𝐜𝐤 𝐭𝐨 𝐮𝐬𝐞𝐫 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐟𝐫𝐨𝐦 𝐚𝐝𝐦𝐢𝐧 𝐫𝐢𝐠𝐡𝐭𝐬.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Manage video chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Manage video chat__"
        )
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **𝐢𝐬 𝐛𝐚𝐧𝐧𝐞𝐝 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩** {m.chat.title}\n\n» **𝐮𝐧𝐛𝐚𝐧 𝐭𝐡𝐞 𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐟𝐢𝐫𝐬𝐭 𝐢𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐟𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐣𝐨𝐢𝐧**\n\n**𝐫𝐞𝐚𝐬𝐨𝐧**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐟𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐣𝐨𝐢𝐧**\n\n**𝐫𝐞𝐚𝐬𝐨𝐧**: `{e}`"
                )

    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐮𝐝𝐢𝐨 𝐛𝐲 𝐕𝐄𝐗𝐄𝐑𝐀 𝐌𝐔𝐒𝐈𝐂 𝐣𝐨𝐢𝐧 @vexera_support ...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"🥺 **𝐒𝐨𝐧𝐠 𝐈𝐬 𝐖𝐚𝐢𝐭𝐢𝐧𝐠** 🥺\n\n😗 **𝐉𝐨𝐢𝐧 @VEXERA_SUPPORT**\n❤️ **𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💙 **𝐒𝐨𝐧𝐠 𝐋𝐢𝐦𝐢𝐭:** `{duration}`\n😇 **𝐏𝐥𝐚𝐲 𝐁𝐲:** {m.from_user.mention()}\n **𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲** {BOT_NAME}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💙 **𝐯𝐞𝐱𝐞𝐫𝐚 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 ❤️**\n\n😗 **𝐉𝐨𝐢𝐧 @VEXERA_SUPPORT**\n❤️ **𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💙 **𝐒𝐨𝐧𝐠 𝐋𝐢𝐦𝐢𝐭:** `{duration}`\n😇 **𝐏𝐥𝐚𝐲 𝐁𝐲:** {requester}\n **𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲** {BOT_NAME}",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f" 𝐏𝐚𝐡𝐥𝐞 𝐕𝐜 𝐭𝐨 𝐬𝐭𝐚𝐫𝐭 𝐤𝐚𝐫 𝐥𝐨 ")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲.**"
                )
            else:
                suhu = await m.reply("**ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("**𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"🥺 **𝐒𝐨𝐧𝐠 𝐈𝐬 𝐖𝐚𝐢𝐭𝐢𝐧𝐠** 🥺\n\n😗 **𝐉𝐨𝐢𝐧 @VEXERA_SUPPORT**\n❤️ **𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💙 **𝐒𝐨𝐧𝐠 𝐋𝐢𝐦𝐢𝐭:** `{duration}`\n😇 **𝐏𝐥𝐚𝐲 𝐁𝐲:** {m.from_user.mention()}\n **𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲** {BOT_NAME}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💙 **𝐯𝐞𝐱𝐞𝐫𝐚 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 ❤️**\n\n😗 **𝐉𝐨𝐢𝐧 @VEXERA_SUPPORT**\n❤️ **𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💙 **𝐒𝐨𝐧𝐠 𝐋𝐢𝐦𝐢𝐭:** `{duration}`\n😇 **𝐏𝐥𝐚𝐲 𝐁𝐲:** {requester}\n **𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲** {BOT_NAME}",                                   
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"𝐏𝐚𝐡𝐥𝐞 𝐕𝐜 𝐭𝐨 𝐬𝐭𝐚𝐫𝐭 𝐤𝐚𝐫 𝐥𝐨")

    else:
        if len(m.command) < 2:
            await m.reply(
                "**𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲.**"
            )
        else:
            suhu = await m.reply("**ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("**𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"🥺 **𝐒𝐨𝐧𝐠 𝐈𝐬 𝐖𝐚𝐢𝐭𝐢𝐧𝐠** 🥺\n\n😗 **𝐉𝐨𝐢𝐧 @VEXERA_SUPPORT**\n❤️ **𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💙 **𝐒𝐨𝐧𝐠 𝐋𝐢𝐦𝐢𝐭:** `{duration}`\n😇 **𝐏𝐥𝐚𝐲 𝐁𝐲:** {m.from_user.mention()}\n **𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲** {BOT_NAME}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💙 **𝐯𝐞𝐱𝐞𝐫𝐚 𝐌𝐮𝐬𝐢𝐜 𝐈𝐬 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 ❤️**\n\n😗 **𝐉𝐨𝐢𝐧 @VEXERA_SUPPORT**\n❤️ **𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💙 **𝐒𝐨𝐧𝐠 𝐋𝐢𝐦𝐢𝐭:** `{duration}`\n😇 **𝐏𝐥𝐚𝐲 𝐁𝐲:** {requester}\n **𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲** {BOT_NAME}",                                
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


# stream is used for live streaming only


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(c: Client, m: Message):
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Cʟᴏsᴇ", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous Admin__ !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Restrict users__\n» ❌ __Add users__\n» ❌ __Manage video chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Manage video chat__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Delete messages__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\n» ❌ __Add users__")
        return
    if not a.can_restrict_members:
        await m.reply_text("missing required permission:" + "\n\n» ❌ __Restrict users__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **is banned in group** {m.chat.title}\n\n» **unban the userbot first if you want to use this bot.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot failed to join**\n\n**reason**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        link = m.text.split(None, 1)[1]
        suhu = await m.reply("🔄 **processing stream...**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                try:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            livelink,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                    await suhu.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[Music live]({link}) stream started.**\n\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await suhu.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")
