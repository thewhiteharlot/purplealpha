# Copyright (C) 2020 AnggaR96s.
# All rights reserved.

from asyncio.exceptions import TimeoutError

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ddl(?: |$)(.*)")
async def ddl(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Enviando informações..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit(r"`¯\_ (ツ) _/¯`")
        return
    await event.edit("```Gerando link direto..```")
    try:
        async with bot.conversation("@jnckbot") as conv:
            chat = "@jnckbot"
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=994325826)
                )
                await bot.forward_messages(chat, reply_message)
                response = await response
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("```Desbloqueie @jnckbot ```")
                return
            await event.delete()
    except TimeoutError:
        return await event.edit("**Erro:** @jnckbot **não está respondendo.**")
    await event.client.send_message(
        event.chat_id, response.message, reply_to=event.message.reply_to_msg_id
    )


CMD_HELP.update(
    {
        "ddl": ">`.ddl` \
\nUsage: Responda a uma mídia para obter um link direto."
    }
)
