# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.cspam (.*)")
async def leter_spam(cspammer):
    cspam = str(cspammer.pattern_match.group(1))
    message = cspam.replace(" ", "")
    await cspammer.delete()
    for letter in message:
        await cspammer.respond(letter)
    if BOTLOG:
        await cspammer.client.send_message(
            BOTLOG_CHATID, "#CSPAM\n" "TSpam foi executado com sucesso"
        )


@register(outgoing=True, pattern="^.wspam (.*)")
async def word_spam(wspammer):
    wspam = str(wspammer.pattern_match.group(1))
    message = wspam.split()
    await wspammer.delete()
    for word in message:
        await wspammer.respond(word)
    if BOTLOG:
        await wspammer.client.send_message(
            BOTLOG_CHATID, "#WSPAM\n" "WSpam foi executado com sucesso"
        )


@register(outgoing=True, pattern="^.spam (.*)")
async def spammer(spamm):
    counter = int(spamm.pattern_match.group(1).split(" ", 1)[0])
    spam_message = str(spamm.pattern_match.group(1).split(" ", 1)[1])
    await spamm.delete()
    await asyncio.wait([spamm.respond(spam_message) for i in range(counter)])
    if BOTLOG:
        await spamm.client.send_message(
            BOTLOG_CHATID, "#SPAM\n" "Spam foi executado com sucesso"
        )


@register(outgoing=True, pattern="^.picspam")
async def tiny_pic_spam(pspam):
    message = pspam.text
    text = message.split()
    counter = int(text[1])
    link = str(text[2])
    await pspam.delete()
    for _ in range(1, counter):
        await pspam.client.send_file(pspam.chat_id, link)
    if BOTLOG:
        await pspam.client.send_message(
            BOTLOG_CHATID, "#PICSPAM\n" "PicSpam foi executado com sucesso"
        )


@register(outgoing=True, pattern="^.delayspam (.*)")
async def dspammer(dspam):
    spamDelay = float(dspam.pattern_match.group(1).split(" ", 2)[0])
    counter = int(dspam.pattern_match.group(1).split(" ", 2)[1])
    spam_message = str(dspam.pattern_match.group(1).split(" ", 2)[2])
    await dspam.delete()
    for _ in range(1, counter):
        await dspam.respond(spam_message)
        await sleep(spamDelay)
    if BOTLOG:
        await dspam.client.send_message(
            BOTLOG_CHATID, "#DelaySPAM\n" "DelaySpam foi executado com sucesso"
        )


CMD_HELP.update(
    {
        "spam": ".cspam <texto>\
\nUso: Spamma o texto letra por letra.\
\n\n.spam <número> <texto>\
\nUso: Spamma texto no chat !!\
\n\n.wspam <texto>\
\nUso: Spamma texto no chat, letra por letra.\
\n\n.picspam <número> <link para imagem/gif>\
\nUso: Como se o spam de texto não fosse suficiente !!\
\n\n.delayspam <atraso> <número> <texto>\
\nUso: .bigspam, mas com atraso personalizado.\
\n\n\nNOTA: Spamme por sua própria conta e risco !!"
    }
)
