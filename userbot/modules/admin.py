# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
"""
Userbot module to help you manage a group
"""

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import (
    BadRequestError,
    MessageTooLongError,
    UserAdminInvalidError,
    UserIdInvalidError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
    PeerChat,
)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "**A imagem é muito pequena!**"
PP_ERROR = "**Falha ao processar a imagem!**"
NO_ADMIN = "**Eu não sou um administrador!**"
NO_PERM = "**Eu não tenho permissões suficientes!**"
NO_SQL = "**Executando em modo não SQL!**"

CHAT_PP_CHANGED = "**Imagem do bate-papo alterada!**"
INVALID_MEDIA = "**Extensão inválida!**"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@register(outgoing=True, pattern=r"^\.setgpic$")
async def set_group_photo(gpic):
    """ For .setgpic command, changes the picture of a group """
    if not gpic.is_group:
        await gpic.edit("**Não acho que seja um grupo.**")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not (admin or creator):
        return await gpic.edit(NO_ADMIN)

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern=r"^\.promote(?: |$)(.*)")
async def promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not (admin or creator):
        return await promt.edit(NO_ADMIN)

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    await promt.edit("**Promovendo...**")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "admin"  # Just in case.
    if not user:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("**Promovido com sucesso!**")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        return await promt.edit(NO_PERM)

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USUÁRIO: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.demote(?: |$)(.*)")
async def demote(dmod):
    """ For .demote command, demotes the replied/tagged person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not (admin or creator):
        return await dmod.edit(NO_ADMIN)

    # If passing, declare that we're going to demote
    await dmod.edit("**Rebaixando...**")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        return await dmod.edit(NO_PERM)
    await dmod.edit("**Rebaixado com sucesso!**")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USUÁRIO: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.ban(?: |$)(.*)")
async def ban(bon):
    """ For .ban command, bans the replied/tagged person """
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not (admin or creator):
        return await bon.edit(NO_ADMIN)

    user, reason = await get_user_from_event(bon)
    if not user:
        return

    # Announce that we're going to whack the pest
    await bon.edit("**Banindo...**")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await bon.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await bon.edit(
            "**Não tenho direitos de excluir mensagens, mas o usuário foi banido!**"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.edit(f"**{str(user.id)}** foi banido!\nMotivo: {reason}")
    else:
        await bon.edit(f"**{str(user.id)}** foi banido!")
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USUÁRIO: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ For .unban command, unbans the replied/tagged person """
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not (admin or creator):
        return await unbon.edit(NO_ADMIN)

    # If everything goes well...
    await unbon.edit("**Desbanindo...**")

    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return

    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("**Desbanido com sucesso!**")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USUÁRIO: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await unbon.edit("**Erro ao completar a ação!**")


@register(outgoing=True, pattern=r"^\.mute(?: |$)(.*)")
async def spider(spdr):
    """
    This function is basically muting peeps
    """
    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await spdr.edit(NO_SQL)

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not (admin or creator):
        return await spdr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(spdr)
    if not user:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        return await spdr.edit(
            "**Mãos muito curtas, não consigo adesivar a mim mesmo...**\n(ヘ･_･)ヘ┳━┳"
        )

    # If everything goes well, do announcing and mute
    await spdr.edit("**Silenciando...**")
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit("**Erro! O usuário provavelmente já está silenciado.**")
    try:
        await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

    except UserIdInvalidError:
        return await spdr.edit("**Erro ao completar a ação!**")
    except UserAdminInvalidError:
        pass

    # Announce that the function is done
    if reason:
        await spdr.edit(f"**Silenciado com sucesso!**\nMotivo: {reason}")
    else:
        await spdr.edit("**Silenciado com sucesso!**")

    # Announce to logging group
    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID,
            "#MUTE\n"
            f"USUÁRIO: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ For .unmute command, unmute the replied/tagged person """
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not (admin or creator):
        return await unmot.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await unmot.edit(NO_SQL)

    # If admin or creator, inform the user and start unmuting
    await unmot.edit("**Desmutando...**")
    user = await get_user_from_event(unmot)
    user = user[0]
    if not user:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("**Erro! O usuário provavelmente já está desmutado.**")
    try:
        await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
        await unmot.edit("**Desmutado com sucesso!**")
    except UserIdInvalidError:
        return await unmot.edit("**Erro ao completar a ação!**")
    except UserAdminInvalidError:
        pass

    if BOTLOG:
        await unmot.client.send_message(
            BOTLOG_CHATID,
            "#UNMUTE\n"
            f"USUÁRIO: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)",
        )


@register(incoming=True, disable_errors=True)
async def muter(moot):
    """ Used for deleting the messages of muted people """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                try:
                    await moot.delete()
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                    )
                except (
                    BadRequestError,
                    UserAdminInvalidError,
                    ChatAdminRequiredError,
                    UserIdInvalidError,
                ):
                    await moot.client.send_read_acknowledge(moot.chat_id, moot.id)


@register(outgoing=True, pattern=r"^\.zombies(?: |$)(.*)", groups_only=False)
async def rm_deletedacc(show):
    """ For .zombies command, list all the ghost/deleted/zombie accounts in a chat. """

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**Nenhuma conta excluída encontrada, o grupo está limpo.**"

    if con != "clean":
        await show.edit("**Procurando contas excluídas...**")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"Encontradas **{del_u}** contas excluídas neste grupo."
                "\nLimpe-os usando `.zombies clean`"
            )
        return await show.edit(del_status)

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not (admin or creator):
        return await show.edit(NO_ADMIN)

    await show.edit("**Removendo contas excluídas...**")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit(NO_PERM)
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Removidas **{del_u}** contas excluídas."

    if del_a > 0:
        del_status = (
            f"Removidas **{del_u}** contas excluídas."
            f"\n**{del_a}** contas de administrador excluídas não foram removidas."
        )
    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#CLEANUP\n"
            f"Removidas **{del_u}** contas excluídas."
            f"\nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )


@register(outgoing=True, pattern=r"^\.admins$")
async def get_admin(show):
    """ For .admins command, list all of the admins of the chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "neste chat"
    mentions = f"<b>Admins em {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n{link}"
            else:
                mentions += f"\nConta excluída <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern=r"^\.pin(?: |$)(.*)")
async def pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not (admin or creator):
        return await msg.edit(NO_ADMIN)

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        return await msg.edit("**Responda a uma mensagem para fixá-la.**")

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        return await msg.edit(NO_PERM)

    await msg.edit("**Fixado com sucesso!**")


@register(outgoing=True, pattern=r"^\.kick(?: |$)(.*)")
async def kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not (admin or creator):
        return await usr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(usr)
    if not user:
        return await usr.edit("**Não foi possível encontrar o usuário.**")

    await usr.edit("**Removendo...**")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        return await usr.edit(NO_PERM + f"\n{str(e)}")

    if reason:
        await usr.edit(
            f"**Removido** [{user.first_name}](tg://user?id={user.id})**!**\nMotivo: {reason}"
        )
    else:
        await usr.edit(f"**Removido** [{user.first_name}](tg://user?id={user.id})**!**")


@register(outgoing=True, pattern=r"^\.users ?(.*)")
async def get_users(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "neste chat"
    mentions = f"Usuários em {title}: \n"
    try:
        if show.pattern_match.group(1):
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nConta excluída `{user.id}`"
        else:
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    mentions += f"\nConta excluída `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "**Carregando lista de usuários como arquivo...**"
        )
        with open("userslist.txt", "w+") as file:
            file.write(mentions)
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption=f"Usuários em {title}",
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("**Envie o nome de usuário, ID ou responda ao usuário!**")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@register(outgoing=True, pattern=r"^\.usersdel ?(.*)")
async def get_usersdel(show):
    """ For .usersdel command, list all of the deleted users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "neste chat"
    mentions = f"Usuários excluídos em {title}: \n"
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        #       else:
        #                mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        #       else:
    #              mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "**Carregando lista de usuários excluídos como arquivo...**"
        )
        with open("deleteduserslist.txt", "w+") as file:
            file.write(mentions)
        await show.client.send_file(
            show.chat_id,
            "deleteduserslist.txt",
            caption=f"Users in {title}",
            reply_to=show.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """ Get the deleted user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit(
                "**Envie o nome de usuário, ID ou responda ao usuário!**"
            )

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@register(outgoing=True, pattern=r"^\.bots$", groups_only=True)
async def get_bots(show):
    """ For .bots command, list all of the bots of the chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "neste chat"
    mentions = f"<b>Bots em {title}:</b>\n"
    try:
        if isinstance(show.to_id, PeerChat):
            return await show.edit("**Apenas supergrupos podem ter bots.**")
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsBots
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nBot excluído <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit("**Fazendo upload da lista de bots como arquivo...**")
        with open("botlist.txt", "w+") as file:
            file.write(mentions)
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption=f"Bots in {title}",
            reply_to=show.id,
        )
        remove("botlist.txt")


CMD_HELP.update(
    {
        "admin": ">`.promote <nome de usuário/resposta> <cargo (opcional)>`"
        "\n**Uso:** Concede direitos de administrador para a pessoa no bate-papo."
        "\n\n>`.demote <nome de usuário/resposta>`"
        "\n**Uso:** Revoga as permissões de administrador da pessoa no chat."
        "\n\n>`.ban <nome de usuário/resposta> <motivo (opcional)>`"
        "\n**Uso:** Bane a pessoa do seu chat."
        "\n\n>`.unban <nome de usuário/resposta>`"
        "\n**Uso:** Remove o banimento da pessoa no chat."
        "\n\n>`.mute <nome de usuário/resposta> <motivo (opcional)>`"
        "\n**Uso:** Silencia a pessoa no chat, também funciona com administradores."
        "\n\n>`.unmute <nome de usuário/resposta>`"
        "\n**Uso:** Remove a pessoa da lista de silenciados."
        "\n\n>`.zombies`"
        "\n**Uso:** Pesquisa contas excluídas em um grupo. "
        "Use .zombies clean para remover contas excluídas do grupo."
        "\n\n>`.admins`"
        "\n**Uso:** Mostra uma lista de administradores no chat."
        "\n\n>`.bots`"
        "\n**Uso:** Mostra uma lista de bots no chat."
        "\n\n>`.users` ou >`.users <nome do membro>`"
        "\n**Uso:** Mostra todos os usuários (ou consultados) no chat."
        "\n\n>`.setgppic <responder a imagem>`"
        "\n**Uso:** Altera a imagem de exibição do grupo."
    }
)
