from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from function.admins import set
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from callsmusic import callsmusic
from callsmusic.queues import queues


@Client.on_message(filters.command(["adminreset", "snehabhi", "vexera"]))
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ 𝐀𝐝𝐦𝐢𝐧 𝐜𝐚𝐜𝐡𝐞 𝐫𝐞𝐟𝐫𝐞𝐬𝐡𝐞𝐝!")


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ Nothing is playing!")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ 𝐏𝐚𝐮𝐬𝐞𝐝!")


@Client.on_message(command(["resume", "ruk"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ Nothing is paused!")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ 𝐑𝐞𝐬𝐮𝐦𝐞𝐝!")


@Client.on_message(command(["end", " band") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐬𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠!")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 𝐬𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠!")


@Client.on_message(command(["skip", "next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐩𝐥𝐚𝐲𝐢𝐧𝐠 𝐭𝐨 𝐬𝐤𝐢𝐩!")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"~ 𝐒𝐤𝐢𝐩𝐩𝐞𝐝 **{skip[0]}**\n\n~ 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 **{qeue[0][0]}**")


@Client.on_message(filters.command(["reload", "snehabhi", "vexera"]))
@errors
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ 𝐀𝐝𝐦𝐢𝐧 𝐜𝐚𝐜𝐡𝐞 𝐫𝐞𝐟𝐫𝐞𝐬𝐡𝐞𝐝!")
