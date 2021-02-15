#!/usr/bin/env python3
# -*- coding: utf-8-*-
#
# (c) https://t.me/TelethonChat/37677 and SpEcHiDe
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""Vá para my.telegram.org
Faça login usando sua conta do Telegram
Clique em API Development Tools
Crie um novo aplicativo, inserindo as informações necessárias
Verifique a seção de mensagens salvas do Telegram para copiar a STRING_SESSION""")
API_KEY = int(input("Digite sua API_ID aqui: "))
API_HASH = input("Digita sua API_HASH aqui: ")

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    print("Verifique a seção de mensagens salvas do Telegram para copiar a STRING_SESSION")
    session_string = client.session.save()
    saved_messages_template = """Suporte: @Soulvessel

<code>STRING_SESSION</code>: <code>{}</code>
⚠️ <i>NÃO envie isso para ninguém!</i>""".format(
        session_string
    )
    client.send_message("me", saved_messages_template, parse_mode="html")
