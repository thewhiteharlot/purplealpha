# Copyright (C) 2020 MoveAngel and MinaProject
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Multifunction memes
#
# Based code + improve from AdekMaulana and aidilaryanto

import asyncio
import os
import random
import re
import textwrap
import time
from asyncio.exceptions import TimeoutError

from glitch_this import ImageGlitcher
from PIL import Image, ImageDraw, ImageFont
from telethon import events, functions, types
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from userbot.utils import check_media, progress

Glitched = TEMP_DOWNLOAD_DIRECTORY + "glitch.gif"

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


@register(outgoing=True, pattern=r"^\.glitch(?: |$)(.*)")
async def glitch(event):
    if not event.reply_to_msg_id:
        await event.edit("`Não vou falhar um fantasma!`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`responda a uma imagem/sticker`")
        return
    await bot.download_file(reply_message.media)
    await event.edit("`Baixando mídia..`")
    if event.is_reply:
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await event.edit("`Arquivos não suportados...`")
            return
    else:
        await event.edit("`Responda a qualquer mídia`")
        return

    try:
        value = int(event.pattern_match.group(1))
        if value > 8:
            raise ValueError
    except ValueError:
        value = 2
    await event.edit("```Falhando essa mídia```")
    await asyncio.sleep(2)
    file_name = "glitch.png"
    to_download_directory = TEMP_DOWNLOAD_DIRECTORY
    downloaded_file_name = os.path.join(to_download_directory, file_name)
    downloaded_file_name = await bot.download_media(
        reply_message,
        downloaded_file_name,
    )
    glitch_file = downloaded_file_name
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    glitch_img = glitcher.glitch_image(img, value, color_offset=True, gif=True)
    DURATION = 200
    LOOP = 0
    glitch_img[0].save(
        Glitched,
        format="GIF",
        append_images=glitch_img[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP,
    )
    await event.edit("`Enviando mídia falhada...`")
    c_time = time.time()
    nosave = await event.client.send_file(
        event.chat_id,
        Glitched,
        force_document=False,
        reply_to=event.reply_to_msg_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]")
        ),
    )
    await event.delete()
    os.remove(Glitched)
    await bot(
        functions.messages.SaveGifRequest(
            id=types.InputDocument(
                id=nosave.media.document.id,
                access_hash=nosave.media.document.access_hash,
                file_reference=nosave.media.document.file_reference,
            ),
            unsave=True,
        )
    )
    os.remove(glitch_file)


@register(outgoing=True, pattern=r"^\.mmf(?: |$)(.*)")
async def mim(event):
    if not event.reply_to_msg_id:
        await event.edit(
            "`Syntax: responda a uma imagem com .mmf` 'texto de cima' ; 'texto de baixo' "
        )
        return

    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("```responda a uma imagem/sticker/gif```")
        return
    await bot.download_file(reply_message.media)
    if event.is_reply:
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await event.edit("`Arquivos não suportados...`")
            return

        await event.edit(
            "```Hora da Transfiguração! Mwahaha Memificando essa imagem! (」ﾟﾛﾟ)｣ ```"
        )
        await asyncio.sleep(5)
        text = event.pattern_match.group(1)
        if event.reply_to_msg_id:
            file_name = "meme.jpg"
            to_download_directory = TEMP_DOWNLOAD_DIRECTORY
            downloaded_file_name = os.path.join(to_download_directory, file_name)
            downloaded_file_name = await bot.download_media(
                reply_message,
                downloaded_file_name,
            )
            dls_loc = downloaded_file_name
        webp_file = await draw_meme_text(dls_loc, text)
        await event.client.send_file(
            event.chat_id, webp_file, reply_to=event.reply_to_msg_id
        )
        await event.delete()
        os.remove(webp_file)
        os.remove(dls_loc)


async def draw_meme_text(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    m_font = ImageFont.truetype(
        "resources/MutantAcademyStyle.ttf", int((70 / 640) * i_width)
    )
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 1,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 1,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, image_name)
    img.save(webp_file, "WebP")
    return webp_file


@register(outgoing=True, pattern=r"^\.q")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Responda a qualquer mensagem do usuário.```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Responda a uma mensagem de texto```")
    chat = "@QuotLyBot"
    if reply_message.sender.bot:
        return await qotli.edit("```Responda a uma mensagem de usuários reais.```")
    await qotli.edit("```Fazendo uma citação```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1031952739)
                )
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply(
                    "```Desbloqueie @QuotLyBot e tente novamente```"
                )
            if response.text.startswith("Hi!"):
                await qotli.edit(
                    "```Você pode gentilmente desativar suas configurações de privacidade de encaminhamento?```"
                )
            else:
                await qotli.delete()
                await bot.forward_messages(qotli.chat_id, response.message)
                await bot.send_read_acknowledge(qotli.chat_id)
                """ - cleanup chat after completed - """
                await qotli.client.delete_messages(conv.chat_id, [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()


@register(outgoing=True, pattern=r"^.hz(:? |$)(.*)?")
async def hazz(hazmat):
    await hazmat.edit("`Enviando informação...`")
    level = hazmat.pattern_match.group(2)
    if hazmat.fwd_from:
        return
    if not hazmat.reply_to_msg_id:
        await hazmat.edit("`WoWoWo Capt!, não vamos vestir um fantasma!...`")
        return
    reply_message = await hazmat.get_reply_message()
    if not reply_message.media:
        await hazmat.edit("`Palavras podem destruir qualquer coisa Capt!...`")
        return
    if reply_message.sender.bot:
        await hazmat.edit("`Responda a um usuário real...`")
        return
    chat = "@hazmat_suit_bot"
    await hazmat.edit("```Se vista Capt!, Vamos exterminar alguns vírus...```")
    message_id_to_reply = hazmat.message.reply_to_msg_id
    msg_reply = None
    async with hazmat.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/hazmat {level}"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            elif reply_message.gif:
                m = f"/hazmat"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hazmat.reply("`Desbloqueie` @hazmat_suit_bot`...`")
            return
        if response.text.startswith("I can't"):
            await hazmat.edit("`GIF não suportado...`")
            await hazmat.client.delete_messages(
                conv.chat_id, [msg.id, response.id, r.id, msg_reply.id]
            )
            return
        else:
            downloaded_file_name = await hazmat.client.download_media(
                response.media, TEMP_DOWNLOAD_DIRECTORY
            )
            await hazmat.client.send_file(
                hazmat.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply,
            )
            """ - cleanup chat after completed - """
            if msg_reply is not None:
                await hazmat.client.delete_messages(
                    conv.chat_id, [msg.id, msg_reply.id, r.id, response.id]
                )
            else:
                await hazmat.client.delete_messages(conv.chat_id, [msg.id, response.id])
    await hazmat.delete()
    return os.remove(downloaded_file_name)


@register(outgoing=True, pattern=r"^.df(:? |$)([1-8])?")
async def fryerrr(fry):
    await fry.edit("`Enviando informação...`")
    level = fry.pattern_match.group(2)
    if fry.fwd_from:
        return
    if not fry.reply_to_msg_id:
        await fry.edit("`Responda a qualquer foto de mensagem do usuário...`")
        return
    reply_message = await fry.get_reply_message()
    if not reply_message.media:
        await fry.edit("`Nenhuma imagem encontrada para fritar...`")
        return
    if reply_message.sender.bot:
        await fry.edit("`Responda a um usuário real...`")
        return
    chat = "@image_deepfrybot"
    message_id_to_reply = fry.message.reply_to_msg_id
    async with fry.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/deepfry {level}"
                msg_level = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await fry.reply("`Desbloqueie` @image_deepfrybot`...`")
            return
        if response.text.startswith("Forward"):
            await fry.edit("`Desative sua configuração de privacidade de encaminhamento...`")
        else:
            downloaded_file_name = await fry.client.download_media(
                response.media, TEMP_DOWNLOAD_DIRECTORY
            )
            await fry.client.send_file(
                fry.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply,
            )
            """ - cleanup chat after completed - """
            try:
                msg_level
            except NameError:
                await fry.client.delete_messages(conv.chat_id, [msg.id, response.id])
            else:
                await fry.client.delete_messages(
                    conv.chat_id, [msg.id, response.id, r.id, msg_level.id]
                )
    await fry.delete()
    return os.remove(downloaded_file_name)


@register(outgoing=True, pattern="^.sg(?: |$)(.*)")
async def lastname(steal):
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await steal.edit("```Responda a qualquer mensagem do usuário.```")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await steal.edit("```Responda a mensagem de usuários reais.```")
        return
    await steal.edit("```Espere enquanto eu roubo alguns dados da NASA```")
    async with bot.conversation(chat) as conv:
        try:
            msg = await conv.send_message(id)
            r = await conv.get_response()
            response = await conv.get_response()
        except YouBlockedUserError:
            await steal.reply("```Desbloqueie @sangmatainfo_bot e tente novamente```")
            return
        if response.text.startswith("No records"):
            await steal.edit("```Nenhum registro encontrado para este usuário```")
            await steal.client.delete_messages(
                conv.chat_id, [msg.id, r.id, response.id]
            )
            return
        else:
            respond = await conv.get_response()
            await steal.edit(f"{response.message}")
        await steal.client.delete_messages(
            conv.chat_id, [msg.id, r.id, response.id, respond.id]
        )


@register(outgoing=True, pattern="^.waifu(?: |$)(.*)")
async def waifu(animu):
    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`Nenhum texto fornecido, por isso a waifu fugiu.`")
            return
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        animu.chat_id,
        reply_to=animu.reply_to_msg_id,
        silent=True if animu.is_reply else False,
        hide_via=True,
    )
    await animu.delete()


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, "", inputString)


CMD_HELP.update(
    {
        "glitch": ".glitch <1-8>\
            \nUso: Responda a um sticker/imagem e envia com cmd.\
            \no valor varia de 1 a 8 se não, ele usará o valor padrão que é 2"
    }
)

CMD_HELP.update(
    {
        "memify": ".mmf textodecima ; textodebaixo\
            \nUso: Responda a um sticker/imagem/gif e envia com cmd."
    }
)

CMD_HELP.update(
    {
        "quotly": ".q \
          \nUso: Transforma um texto em sticker."
    }
)

CMD_HELP.update(
    {
        "hazmat": ".hz or .hz [flip, x2, rotate (graus), background (numero), black]"
        "\nUso: Responda a uma imagem/sticker para se vestir!"
        "\n@hazmat_suit_bot"
    }
)

CMD_HELP.update(
    {
        "deepfry": ".df ou .df [level(1-8)]"
        "\nUso: Frita a imagem/sticker da resposta."
        "\n@image_deepfrybot"
    }
)


CMD_HELP.update(
    {
        "sangmata": ".sg \
          \nUso: Descobre nomes passados do usuário."
    }
)


CMD_HELP.update(
    {
        "waifu": ".waifu \
          \nUso: Melhore seu texto com belos modelos de anime girl. \
          \n@StickerizerBot"
    }
)