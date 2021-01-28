# Originally from Bothub
# Port to UserBot by @heyworld
import asyncio
import glob
import os
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from selenium import webdriver
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeVideo

from userbot import CMD_HELP, GOOGLE_CHROME_BIN, bot
from userbot.events import register
from userbot.utils import progress


# Copyright (C) 2020 azrim.
# imported .song and .vsong form catuserbot
async def catmusic(cat, QUALITY, hello):
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not video_link:
        await hello.edit(f"Desculpa. Não consigo encontrar essa música. `{search}`")
        return
    try:
        command = (
            'youtube-dl -o "./temp/%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality '
            + QUALITY
            + " "
            + video_link
        )
        os.system(command)
    except Exception as e:
        return await hello.edit(f"`Error:\n {e}`")
    try:
        thumb = (
            'youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download '
            + video_link
        )
        os.system(thumb)
    except Exception as e:
        return await hello.edit(f"`Error:\n {e}`")


@register(outgoing=True, pattern="^.song(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await event.edit("`O que devo encontrar? `")
        return
    event = await event.edit("`Espere..! Estou encontrando sua música...`")
    await catmusic(str(query), "128k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("Sim..! Eu encontrei algo, um minuto..🥰")
    else:
        await event.edit(f"Perdão..! Eu não consigo encontrar nada com `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    catthumb = thumbcat[0] if thumbcat else None
    loa = l[0]
    await bot.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@register(outgoing=True, pattern="^.song360(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        event = await event.edit("`O que devo encontrar? `")
        return
    event = await event.edit("`Espere..! Estou encontrando sua música...`")
    await catmusic(str(query), "320k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("Sim..! Eu encontrei algo, um minuto..🥰")
    else:
        await event.edit(f"Perdão..! Eu não consigo encontrar nada com `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    catthumb = thumbcat[0] if thumbcat else None
    loa = l[0]
    await bot.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


async def getmusicvideo(cat):
    video_link = ""
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    command = 'youtube-dl -f "[filesize<50M]" --merge-output-format mp4 ' + video_link
    os.system(command)


@register(outgoing=True, pattern=r"^\.vsong(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Espere..! Estou encontrando seu vídeo..`")
    elif reply:
        query = str(reply.message)
        await event.edit("`Espere..! Estou encontrando seu vídeo..`")
    else:
        await event.edit("`O que devo encontrar?`")
        return
    await getmusicvideo(query)
    l = glob.glob(("*.mp4")) + glob.glob(("*.mkv")) + glob.glob(("*.webm"))
    if l:
        await event.edit("`Sim..! Eu encontrei algo..`")
    else:
        await event.edit(f"`Perdão..! Eu não consigo encontrar nada com` **{query}**")
        return
    try:
        loa = l[0]
        metadata = extractMetadata(createParser(loa))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        os.system("cp *mp4 thumb.mp4")
        os.system("ffmpeg -i thumb.mp4 -vframes 1 -an -s 480x360 -ss 5 thumb.jpg")
        thumb_image = "thumb.jpg"
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            loa,
            force_document=False,
            thumb=thumb_image,
            allow_cache=False,
            caption=query,
            supports_streaming=True,
            reply_to=reply_to_id,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    round_message=False,
                    supports_streaming=True,
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "[UPLOAD]", loa)
            ),
        )
        await event.edit(f"**{query}** `Enviado com sucesso..!`")
        os.remove(thumb_image)
        os.system("rm -rf *.mkv")
        os.system("rm -rf *.mp4")
        os.system("rm -rf *.webm")
    except BaseException:
        os.remove(thumb_image)
        os.system("rm -rf *.mkv")
        os.system("rm -rf *.mp4")
        os.system("rm -rf *.webm")
        return


@register(outgoing=True, pattern="^.spd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Adquirindo sua música```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit(
            "`Baixando músicas pode levar algum tempo, então pegue uma pipoca .....`"
        )
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=752979930)
            )
            await bot.send_message(chat, link)
            respond = await response
        except YouBlockedUserError:
            await event.reply(
                "```Desbloqueie @SpotifyMusicDownloaderBot e tente novamente```"
            )
            return
        await event.delete()
        await bot.forward_messages(event.chat_id, respond.message)


@register(outgoing=True, pattern="^.netease(?: |$)(.*)")
async def WooMai(netase):
    if netase.fwd_from:
        return
    song = netase.pattern_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {song}"
    await netase.edit("```Adquirindo sua música```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await netase.edit("`Baixando...Um minuto`")
        try:
            msg = await conv.send_message(link)
            response = await conv.get_response()
            respond = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await netase.reply("```Desbloqueie @WooMaiBot e tente novamente```")
            return
        await netase.edit("`Enviando sua música...`")
        await asyncio.sleep(3)
        await bot.send_file(netase.chat_id, respond)
    await netase.client.delete_messages(conv.chat_id, [msg.id, response.id, respond.id])
    await netase.delete()


@register(outgoing=True, pattern="^.dzd(?: |$)(.*)")
async def DeezLoader(Deezlod):
    if Deezlod.fwd_from:
        return
    d_link = Deezlod.pattern_match.group(1)
    if ".com" not in d_link:
        await Deezlod.edit("` Preciso de um link para baixar algo.`**(._.)**")
    else:
        await Deezlod.edit("**Iniciando Download!**")
    chat = "@DeezLoadBot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            song = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await Deezlod.edit(
                "**Erro:** `Desbloqueie` @DeezLoadBot `e tente novamente!`"
            )
            return
        await bot.send_file(Deezlod.chat_id, song, caption=details.text)
        await Deezlod.client.delete_messages(
            conv.chat_id, [msg_start.id, response.id, r.id, msg.id, details.id, song.id]
        )
        await Deezlod.delete()


CMD_HELP.update(
    {
        "music": "`.spd`<Artist - Song Title>\
            \nUso:For searching songs from Spotify.\
            \n\n`.song` or `.vsong`\
            \nUso:for downloading music\
            \n\n`.netease` <Artist - Song Title>\
            \nUso:Download music with @WooMaiBot\
            \n\n`.dzd` <Spotify/Deezer Link>\
            \nUso:Download music from Spotify or Deezer.\
            \n\n`.deezload` <spotify/deezer link> <Format>\
            \nUso: Download music from deezer.\
            \n\nWell deezer is not available in India so create an deezer account using vpn. Set `DEEZER_ARL_TOKEN` in vars to make this work.\
            \n\n**Format**= `FLAC`, `MP3_320`, `MP3_256`, `MP3_128`.\
            \n\n\n Guide:Video guide of arl token: [here](https://www.youtube.com/watch?v=O6PRT47_yds&feature=youtu.be) or Read [This](https://notabug.org/RemixDevs/DeezloaderRemix/wiki/Login+via+userToken)."
    }
)
