# Copyright (C) 2020 KenHV
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, disable_edited=True, pattern="^.fban(?: |$)(.*)")
async def fban(event):
    """Bans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não-SQL!**")

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        fban_id = reply_msg.from_id
        reason = event.pattern_match.group(1)
        user_link = f"[{fban_id}](tg://user?id={fban_id})"
    else:
        pattern = str(event.pattern_match.group(1)).split()
        fban_id = pattern[0]
        reason = " ".join(pattern[1:])
        user_link = fban_id

    self_user = await event.client.get_me()

    if fban_id == self_user.id or fban_id == "@" + self_user.username:
        return await event.edit(
            "**Erro: Esta ação foi impedida pelos protocolos de autopreservação do PurpleBot.**"
        )

    if len((fed_list := get_flist())) == 0:
        return await event.edit("**Você ainda não se conectou a nenhuma federação!**")

    if len(fban_id) == 0 or fban_id == (None, ""):
        return await event.edit("**Usuário não especificado, não posso banir o vento!**")

    await event.edit(f"**Fbanindo...** {user_link}...")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/fban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if (
                    ("New FedBan" not in reply.text)
                    and ("Starting a federation ban" not in reply.text)
                    and ("Start a federation ban" not in reply.text)
                    and ("FedBan reason updated" not in reply.text)
                ):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Não especificado."

    if failed:
        status = f"Falha no fban em {len(failed)}/{total} federações.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Sucesso! Fbanido em {total} federações."

    await event.edit(
        f"**Fbanido **{user_link}!\n**Motivo:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^\.unfban(?: |$)(.*)")
async def unfban(event):
    """Unbans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não-SQL!**")

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        unfban_id = reply_msg.from_id
        reason = event.pattern_match.group(1)
        user_link = f"[{unfban_id}](tg://user?id={unfban_id})"
    else:
        pattern = str(event.pattern_match.group(1)).split()
        unfban_id = pattern[0]
        reason = " ".join(pattern[1:])
        user_link = unfban_id

    self_user = await event.client.get_me()

    if unfban_id == self_user.id or unfban_id == "@" + self_user.username:
        return await event.edit("**Espere, isso é ilegal**")

    if len((fed_list := get_flist())) == 0:
        return await event.edit("**Você ainda não se conectou a nenhuma federação!!**")

    await event.edit(f"**Des-fbanindo **{user_link}**...**")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/unfban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if (
                    ("New un-FedBan" not in reply.text)
                    and ("I'll give" not in reply.text)
                    and ("Un-FedBan" not in reply.text)
                ):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Não especificado."

    if failed:
        status = f"Falha ao des-fbanir em {len(failed)}/{total} federações.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Success! Un-fbanned in {total} feds."

    reason = reason if reason else "Não especificado."
    await event.edit(
        f"**Des-fbanido** {user_link}!\n**Motivo:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, pattern=r"^\.addf *(.*)")
async def addf(event):
    """Adds current chat to connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import add_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não-SQL!**")

    if not (fed_name := event.pattern_match.group(1)):
        return await event.edit("**Passe um nome para se conectar a este grupo!**")

    try:
        add_flist(event.chat_id, fed_name)
    except IntegrityError:
        return await event.edit(
            "**Este grupo já está conectado à lista de federações.**"
        )

    await event.edit("**Adicionado este grupo à lista de federações!**")


@register(outgoing=True, pattern=r"^\.delf$")
async def delf(event):
    """Removes current chat from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não-SQL!**")

    del_flist(event.chat_id)
    await event.edit("**Removido este grupo da lista de federações!**")


@register(outgoing=True, pattern=r"^\.listf$")
async def listf(event):
    """List all connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não-SQL!**")

    if len((fed_list := get_flist())) == 0:
        return await event.edit("**Você ainda não se conectou a nenhuma federação!**")

    msg = "**Federações conectadas:**\n\n"

    for i in fed_list:
        msg += "• " + str(i.fed_name) + "\n"

    await event.edit(msg)


@register(outgoing=True, disable_edited=True, pattern=r"^\.clearf$")
async def delf(event):
    """Removes all chats from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist_all
    except IntegrityError:
        return await event.edit("**Executando em modo não-SQL!**")

    del_flist_all()
    await event.edit("**Desconectado de todas as federações conectadas!**")


CMD_HELP.update(
    {
        "fban": ".fban <id/nome de usuário> <motivo>"
        "\nUso: Bane o usuário de federações conectadas."
        "\nVocê pode responder ao usuário a quem deseja fbanir ou passar manualmente o nome de usuário/id."
        "\n\n.unfban <id/nome de usuário> <motivo>"
        "\nUso: Desbane o usuário de federações conectadas."
        "\n\n.addf <nome>"
        "\nUso: Adiciona o grupo atual e o armazena como <nome> nas federações conectadas."
        "\nAdicionar um grupo é o suficiente para uma federação."
        "\n\n.delf"
        "\nUso: Remove o grupo atual das federações conectadas."
        "\n\n.listf"
        "\nUso: Lista todas as federações conectadas por nome especificado."
    }
)
