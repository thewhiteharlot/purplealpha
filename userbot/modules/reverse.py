# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Thanks to @kandnub, for this awesome module !!
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for reverse searching stickers and images on Google """

import io
import os
import shutil
import urllib

import requests
from bs4 import BeautifulSoup
from PIL import Image

from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.utils import googleimagesdownload

opener = urllib.request.build_opener()
useragent = (
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/80.0.3987.149 Mobile Safari/537.36"
)
opener.addheaders = [("User-agent", useragent)]


@register(outgoing=True, pattern=r"^\.reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, Google search images and stickers. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    message = await img.get_reply_message()

    if not message or not message.media:
        return await img.edit("**Responda a uma foto ou adesivo.**")

    photo = io.BytesIO()
    await bot.download_media(message, photo)
    if not photo:
        return await img.edit("**Não foi possível baixar a imagem.**")

    await img.edit("**Processando...**")

    try:
        image = Image.open(photo)
    except OSError:
        return await img.edit("**Arquivo não suportado.**")

    name = "okgoogle.png"
    image.save(name, "PNG")
    image.close()

    # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
    searchUrl = "https://www.google.com/searchbyimage/upload"
    multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers["Location"]

    if response == 400:
        return await img.edit("**Erro do Google.**")

    await img.edit(
        "**Imagem carregada com sucesso para o Google.**" "\n**Analisando fonte agora**"
    )
    os.remove(name)
    match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
    guess = str(match["best_guess"])
    imgspage = match["similar_images"]

    if not guess and not imgspage:
        return await img.edit("**Não foram encontrados resultados**")

    try:
        counter = int(img.pattern_match.group(1))
    except:
        counter = int(3)
    counter = int(10) if counter > 10 else counter
    counter = int(3) if counter < 0 else counter

    if counter == 0:
        return await img.edit(
            f"**Melhor combinação:** `{guess}`\
                              \n\n[Imagens visualmente semelhantes]({fetchUrl})\
                              \n\n[Resultados para {guess}]({imgspage})"
        )

    await img.edit(
        f"**Melhor combinação:** `{guess}`\
                   \n\n[Imagens visualmente semelhantes]({fetchUrl})\
                   \n\n[Resultados para {guess}]({imgspage})\
                   \n\n**Buscando imagens...**"
    )

    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": guess,
        "limit": counter,
        "format": "png",
        "no_directory": "no_directory",
    }

    try:
        paths = response.download(arguments)
    except Exception as e:
        return await img.edit(
            f"**Melhor combinação:** `{guess}`\
                              \n\n[Imagens visualmente semelhantes]({fetchUrl})\
                              \n\n[Resultados para {guess}]({imgspage})\
                              \n\n**Erro:** `{e}`**.**"
        )

    lst = paths[0][guess]
    await img.client.send_file(
        entity=img.chat_id,
        file=lst,
        reply_to=img,
    )
    await img.edit(
        f"**Melhor combinação:** `{guess}`\
                   \n\n[Imagens visualmente semelhantes]({fetchUrl})\
                   \n\n[Resultados para {guess}]({imgspage})"
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}

    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    results["best_guess"] = results["best_guess"][12:]
    return results


CMD_HELP.update(
    {
        "reverse": ">`.reverse [número] <opcional>`"
        "\n**Uso:** Responda a uma foto/sticker para fazer uma busca reversa no Imagens do Google."
        "\nO número de resultados pode ser especificado, o padrão é 3."
        "\nSe o contador for 0, apenas informações e links serão fornecidos."
        "\nO bot pode falhar ao enviar imagens se um grande número de resultados for solicitado."
    }
)
