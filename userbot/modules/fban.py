# Copyright (C) 2020 KenHV

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, disable_edited=True, pattern=r"^\.fban(?: |$)(.*)")
async def fban(event):
    """Bans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não SQL!**")

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        fban_id = reply_msg.sender_id
        reason = event.pattern_match.group(1)
    else:
        pattern = str(event.pattern_match.group(1)).split()
        fban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        fban_id = await event.client.get_peer_id(fban_id)
    except:
        pass

    if event.sender_id == fban_id:
        return await event.edit(
            "**Erro: Esta ação foi impedida pelos protocolos de autopreservação.**"
        )

    if len(fed_list := get_flist()) == 0:
        return await event.edit("**Você ainda não se conectou a nenhuma federação!**")

    user_link = f"[{fban_id}](tg://user?id={fban_id})"

    await event.edit(f"**Fbanindo** {user_link}...")
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
        status = f"Falha no FBan em {len(failed)}/{total} federações.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Sucesso! FBanido em {total} federações."

    await event.edit(
        f"**FBanido **{user_link}!\n**Motivo:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^\.unfban(?: |$)(.*)")
async def unfban(event):
    """Unbans a user from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não SQL!**")

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        unfban_id = reply_msg.sender_id
        reason = event.pattern_match.group(1)
    else:
        pattern = str(event.pattern_match.group(1)).split()
        unfban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        unfban_id = await event.client.get_peer_id(unfban_id)
    except:
        pass

    if event.sender_id == unfban_id:
        return await event.edit("**Espere, isso é ilegal**")

    if len(fed_list := get_flist()) == 0:
        return await event.edit("**Você ainda não se conectou a nenhuma federação!**")

    user_link = f"[{unfban_id}](tg://user?id={unfban_id})"

    await event.edit(f"**Un-fbanindo **{user_link}**...**")
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
        status = f"Falha ao un-fbanir em {len(failed)}/{total} federações.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Sucesso! Un-fbanido em {total} federações."

    reason = reason if reason else "Not specified."
    await event.edit(
        f"**Un-fbanido** {user_link}!\n**Motivo:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, pattern=r"^\.addf(?: |$)(.*)")
async def addf(event):
    """Adds current chat to connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import add_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não SQL!**")

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
        return await event.edit("**Executando em modo não SQL!**")

    del_flist(event.chat_id)
    await event.edit("**Removido este grupo da lista de federações!**")


@register(outgoing=True, pattern=r"^\.listf$")
async def listf(event):
    """List all connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Executando em modo não SQL!**")

    if len(fed_list := get_flist()) == 0:
        return await event.edit("**Você ainda não se conectou a nenhuma federação!**")

    msg = "**Federações conectadas:**\n\n"

    for i in fed_list:
        msg += "• " + str(i.fed_name) + "\n"

    await event.edit(msg)


@register(outgoing=True, disable_edited=True, pattern=r"^\.clearf$")
async def clearf(event):
    """Removes all chats from connected federations."""
    try:
        from userbot.modules.sql_helper.fban_sql import del_flist_all
    except IntegrityError:
        return await event.edit("**Executando em modo não SQL!**")

    del_flist_all()
    await event.edit("**Desconectado de todas as federações conectadas!**")


CMD_HELP.update(
    {
        "fban": ">`.fban <id/nome de usuário> <motivo>`"
        "\n**Uso:** Bane o usuário de federações conectadas."
        "\nVocê pode responder ao usuário que deseja fbanir ou passar manualmente o nome de usuário/id."
        "\n\n`>.unfban <id/nome de usuário> <motivo>`"
        "\n**Uso:** O mesmo que fban, mas desbane o usuário"
        "\n\n>`.addf <name>`"
        "\n**Uso:** Adiciona o grupo atual e o armazena como <nome> nas federações conectadas."
        "\nAdicionar um grupo é suficiente para uma federação."
        "\n\n>`.delf`"
        "\n**Uso:** Remove o grupo atual das federações conectadas."
        "\n\n>`.listf`"
        "\n**Uso:** Lista todas as federações conectadas por nome especificado. "
        "\n\n>`.clearf`"
        "\n**Uso:** Desconecta de todas as federações conectadas. Use-o com cuidado."
    }
)
