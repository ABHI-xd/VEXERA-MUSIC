from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, BG_IMAGE, SUPPORT_GROUP
from Abhixd.filters import command, other_filters
from Abhixd.decorators import errors
from Abhixd.errors import DurationLimitError
from Abhixd.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("fplay") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("ıllıllı **Ꭾяσ¢єѕѕιηg**ıllıllı  ♩✌")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="💬 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                        url=f"https://t.me/SNEHABHI_SERVER"),
                    InlineKeyboardButton(
                        text="🔊 𝐔𝐩𝐝𝐚𝐭𝐞𝐬",
                        url=f"https://t.me/SNEHABHI_UPDATES")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("𝐒𝐨𝐧𝐠 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.𝐓𝐫𝐲 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐬𝐨𝐧𝐠 𝐨𝐫 𝐦𝐚𝐲𝐛𝐞 𝐬𝐩𝐞𝐥𝐥 𝐢𝐭 𝐩𝐫𝐨𝐩𝐞𝐫𝐥𝐲.")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=f"{BG_IMAGE}",
        reply_markup=keyboard,
        caption=f"#⃣ 𝐘𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠 **queued** 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{BG_IMAGE}",
        reply_markup=keyboard,
        caption=f"▶️ **Playing** 𝐡𝐞𝐫𝐞 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲 {costumer}"
        )
        return await lel.delete()
