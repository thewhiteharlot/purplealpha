# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module for having some fun with people. """

from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub

import requests
from cowpy import cow

from userbot import CMD_HELP
from userbot.events import register
from userbot.modules.admin import get_user_from_event

# ================= CONSTANT =================
METOOSTR = [
    "Eu também, obrigado",
    "Haha sim, eu também",
    "Também lol",
    "Eu ai",
    "Mesmo aqui",
    "Haha sim",
    "Eu agora",
]

ZALG_LIST = [
    [
        "",
        " ̗",
        " ̘",
        " ̙",
        " ̜",
        " ̝",
        " ̞",
        " ̟",
        " ̠",
        " ̤",
        " ̥",
        " ̦",
        " ̩",
        " ̪",
        " ̫",
        " ̬",
        " ̭",
        " ̮",
        " ̯",
        " ̰",
        " ̱",
        " ̲",
        " ̳",
        " ̹",
        " ̺",
        " ̻",
        " ̼",
        " ͅ",
        " ͇",
        " ͈",
        " ͉",
        " ͍",
        " ͎",
        " ͓",
        " ͔",
        " ͕",
        " ͖",
        " ͙",
        " ͚",
        " ",
    ],
    [
        " ̍",
        " ̎",
        " ̄",
        " ̅",
        " ̿",
        " ̑",
        " ̆",
        " ̐",
        " ͒",
        " ͗",
        " ͑",
        " ̇",
        " ̈",
        " ̊",
        " ͂",
        " ̓",
        " ̈́",
        " ͊",
        " ͋",
        " ͌",
        " ̃",
        " ̂",
        " ̌",
        " ͐",
        " ́",
        " ̋",
        " ̏",
        " ̽",
        " ̉",
        " ͣ",
        " ͤ",
        " ͥ",
        " ͦ",
        " ͧ",
        " ͨ",
        " ͩ",
        " ͪ",
        " ͫ",
        " ͬ",
        " ͭ",
        " ͮ",
        " ͯ",
        " ̾",
        " ͛",
        " ͆",
        " ̚",
    ],
    [
        " ̕",
        " ̛",
        " ̀",
        " ́",
        " ͘",
        " ̡",
        " ̢",
        " ̧",
        " ̨",
        " ̴",
        " ̵",
        " ̶",
        " ͜",
        " ͝",
        " ͞",
        " ͟",
        " ͠",
        " ͢",
        " ̸",
        " ̷",
        " ͡",
    ],
]

EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

INSULT_STRINGS = [
    "Owww ... que idiota estúpido.",
    "Não beba e digite.",
    "Eu acho que você deveria ir para casa ou melhor, um asilo mental.",
    "Comando não encontrado. Assim como seu cérebro.",
    "Você percebe que está fazendo papel de bobo? Aparentemente não.",
    "Você pode digitar melhor do que isso.",
    "A regra do bot 544, seção 9, me impede de responder a humanos estúpidos como você.",
    "Desculpe, nós não vendemos cérebros.",
    "Acredite em mim, você não é normal.",
    "Aposto que seu cérebro parece tão bom quanto novo, visto que você nunca o usa.",
    "Se eu quisesse me matar, escalaria seu ego e pularia para seu QI.",
    "Os zombies comem cérebros... você tá safo.",
    "Você não evoluiu dos macacos, eles evoluíram de você.",
    "Volte e fale comigo quando seu Q.I. exceder sua idade.",
    "Não estou dizendo que você é estúpido, só estou dizendo que você dá azar quando se trata de pensar.",
    "Que língua você está falando? Porque parece besteira.",
    "Estupidez não é um crime, então você está livre.",
    "Você é a prova de que a evolução PODE ir ao contrário.",
    "Eu perguntaria quantos anos você tem, mas eu acho que você não sabe como contar até lá.",
    "Como um alien, o que você acha da raça humana?",
    "Cérebros não são tudo. No seu caso, eles não são nada",
    "Normalmente as pessoas vivem e aprendem. Você só vive.",
    "Eu não sei o que te torna tão estúpido, mas realmente funciona.",
    "Continue falando, algum dia você dirá algo inteligente! (Eu duvido entretanto)",
    "Me choque, diga algo inteligente.",
    "Seu QI é menor do que o tamanho do seu sapato.",
    "Ai de mim! Seus neurotransmissores não estão mais funcionando.",
    "Você está louco, seu tolo.",
    "Todo mundo tem o direito de ser estúpido, mas você está abusando do privilégio.",
    "Lamento ter magoado seus sentimentos quando chamei você de estúpido. Achei que você já soubesse disso.",
    "Você deveria experimentar provar cianeto.",
    "Suas enzimas são destinadas a digerir veneno de rato.",
    "Você deveria tentar dormir para sempre.",
    "Pegue uma arma e atire em si mesmo.",
    "Você poderia fazer um recorde mundial pulando de um avião sem pára-quedas.",
    "Pare de falar besteira e pule na frente de um trem-bala em execução.",
    "Experimente tomar banho com ácido clorídrico em vez de água.",
    "Tente isto: se você prender a respiração debaixo d'água por uma hora, poderá prendê-la para sempre.",
    "Go Green! Pare de inalar oxigênio.",
    "Deus estava procurando por você. Você deveria ir ao seu encontro.",
    "Dê seus 100%! Agora vá doar sangue.",
    "Tente pular de um prédio de cem andares, mas você só pode fazer isso uma vez.",
    "Você deveria doar seu cérebro, já que nunca o usou.",
    "Voluntário para o alvo em um campo de tiro.",
    "Tiros na cabeça são divertidos. Arranje um.",
    "Você deveria tentar nadar com grandes tubarões brancos.",
    "Você deveria se pintar de vermelho e correr em uma maratona de touros.",
    "Você pode ficar debaixo d'água pelo resto da vida sem voltar para cima.",
    "Que tal você parar de respirar por, tipo, 1 dia? Isso vai ser ótimo.",
    "Experimente provocar um tigre enquanto vocês dois estão em uma gaiola.",
    "Você já tentou atirar em si mesmo a uma altura de 100m usando um canhão?",
    "Você deve tentar segurar TNT na boca e acendê-lo.",
    "Tente pegar e jogar com fulminato de mercúrio, é divertido.",
    "Ouvi dizer que fosfina é tóxico, mas acho que você não se importaria em inalá-la por diversão.",
    "Lance-se ao espaço sideral enquanto se esquece do oxigênio na Terra.",
    "Você deve tentar brincar de cobra e escadas, com cobras de verdade e sem escadas.",
    "Dance pelado em alguns fios de alta tensão.",
    "Um vulcão ativo é a melhor piscina para você.",
    "Você deveria experimentar um banho quente em um vulcão.",
    "Tente passar um dia em um caixão e ele será seu para sempre.",
    "Acerte o Urânio com um nêutron lento em sua presença. Será uma experiência valiosa.",
    "Você pode ser a primeira pessoa a pisar no sol. Experimente.",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNS_STR = [
    "Corre para Thanos ..",
    "Corre pra muito, muito longe da terra ..",
    "Correndo mais rápido que o Bolt porque sou um userbolt !!",
    "Corre até a Marie ..",
    "Este grupo é canceroso demais para lidar com isso.",
    "Cya rapazes",
    "Kys",
    "Eu vou embora",
    "Estou indo embora, porque sou muito gordo.",
    "Eu fugi!",
    "Vou correr para o chocolate.",
    "Eu corro porque gosto muito de comida.",
    "Correndo...\nporque fazer dieta não é uma opção.",
    "Corredor muito louco e rápido",
    "Se você quer me pegar, você tem que ser rápido...\nSe você quer ficar comigo, você tem que ser bom...\nMas se você quiser me passar...\nVocê só pode estar de brincadeira.",
    "Qualquer um pode correr cem metros, são os próximos quarenta e dois mil e duzentos que contam.",
    "Por que todas essas pessoas estão me seguindo? ",
    "As crianças ainda estão me perseguindo?",
    "Correr uma maratona ... existe um aplicativo para isso.",
]

CHASE_STR = [
    "Onde você pensa que está indo?",
    "Huh? O quê? Eles escaparam?",
    "ZZzzZZzz ... Hã? O quê? Oh, só eles de novo, deixa pra lá.",
    "Volte aqui!",
    "Não tão rápido...",
    "Cuidado com a parede!",
    "Não me deixe sozinho com eles !!",
    "Você corre, você morre.",
    "Se ferrou, estou em todo lugar",
    "Você vai se arrepender disso ...",
    "Você também pode tentar /kickme, ouvi dizer que é divertido.",
    "Vá incomodar outra pessoa, ninguém aqui liga.",
    "Você pode correr, mas não pode se esconder.",
    "Isso é tudo que você tem?",
    "Estou atrás de você...",
    "Você tem companhia!",
    "Podemos fazer isso da maneira fácil ou da maneira mais difícil.",
    "Você simplesmente não entende, não é?",
    "Sim, é melhor você correr!",
    "Por favor, me lembre o quanto eu me importo?",
    "Eu correria mais rápido se fosse você.",
    "Esse é definitivamente o andróide que procuramos.",
    "Que as probabilidades estejam sempre a seu favor.",
    "Últimas palavras famosas.",
    "E eles desapareceram para sempre, para nunca mais serem vistos.",
    "Yeah yeah, just tap /kickme already.",
    "Aqui, pegue este anel e vá até Mordor enquanto faz isso.",
    "Diz a lenda que ainda estão em execução ...",
    "Ao contrário de Harry Potter, seus pais não podem proteger você de mim.",
    "O medo leva à raiva. A raiva leva ao ódio. O ódio leva ao sofrimento. Se você continuar correndo com medo, poderá"
    "ser o próximo Vader.",
    "Múltiplos cálculos depois, decidi que meu interesse em suas travessuras é exatamente 0.",
    "Reza a lenda que ainda estão em execução.",
    "Continue assim, não tenho certeza se queremos você aqui de qualquer maneira.",
    "Você é um brux- Oh. Espere. Você não é Harry, continue andando.",
    "SEM CORRER NOS CORREDORES!",
    "Hasta la vista, baby.",
    "Quem soltou os cachorros?",
    "É engraçado, porque ninguém liga.",
    "Ah, que desperdício. Gostei desse.",
    "Francamente, meu querido, não dou a mínima.",
    "Meu milkshake traz todos os meninos para o quintal ... Então corra mais rápido!",
    "Você não pode MANTER a verdade!",
    "Há muito tempo, em uma galáxia muito distante ... Alguém teria se importado com isso. Mas não mais.",
    "Ei, olhe para eles! Eles estão fugindo do inevitável martelo do banimento ... Fofo.",
    "Han atirou primeiro. Eu também",
    "O que você está correndo atrás, um coelho branco?",
    "Como diria o médico ... CORRA!",
]

HELLOSTR = [
    "Hi !",
    "‘Lá, cap'tão!",
    "Qq tá rolando’?",
    "‘Eae, cupcake?",
    "Oi, oi ,oi!",
    "Olá, quem está aí, estou falando.",
    "Você sabe quem é.",
    "Yo!",
    "Qual a boa?",
    "Saudações e felicitações!",
    "Olá, flor do dia!",
    "Hey, opa, hi!",
    "O que que houve, minha couve?",
    "Surpresa!",
    "Olá-holá!",
    "Olá calouro!",
    "Eu venho em paz!",
    "Ahoy, camarada!",
    "Hiya!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{hits} {victim} com um {item}.",
    "{hits} {victim} no rosto com um {item}.",
    "{hits} {victim} um pouco com um {item}.",
    "{throws} um {item} em {victim}.",
    "pega um {item} e {throws} ele no rosto de {victim}",
    "{hits} um {item} em {victim}.",
    "{throws} alguns {item} em {victim}.",
    "pega um {item} e {throws} ele no rosto de {victim}",
    "joga um {item} na direção de {victim}",
    "senta no rosto de {victim} enquanto bate um {item} {where}.",
    "começa a estapear {victim} com um {item}.",
    "imobiliza {victim} e repetidamente {hits} ele com um {item}.",
    "pega um {item} e {hits} {victim} com ele.",
    "começa a esbofeteá-lo {victim} com um {item}.",
    "mantém a {victim} pressionada e repetidamente os acerta com um {item}.",
    "cutuca {victim} com um {item}.",
    "pega um {item} e {hits} {victim} com ele.",
    "amarra {victim} a uma cadeira e {throws} um {item} nele.",
    "{hits} {victim} {where} com um {item}.",
    "amarra {victim} em um poste e os chicoteia {where} com um {item}."
    "deu um empurrão amigável para ajudar {victim} aprender a nadar na lava.",
    "mandou {victim} para /dev/null.",
    "enviou {victim} pelo buraco da memória.",
    "decapitou {victim}.",
    "jogou {victim} de um prédio.",
    "substituiu todas as músicas de {victim} por Nickelback.",
    "enviou spam ao e-mail de {victim}",
    "fez de {vítima} um sanduíche de junta.",
    "esbofeteou {vítima} com absolutamente nada.",
    "acertou {victim} com uma pequena nave espacial interestelar.",
    "deu um quickscope em {victim}.",
    "botou {victim} em cheque-mate.",
    "criptografou {victim} em RSA e excluiu a chave privada.",
    "botou {victim} na friendzone.",
    "bloqueou {victim} com um pedido de remoção DMCA!",
]

ITEMS = [
    "frigideira de ferro fundido",
    "truta grande",
    "taco de beisebol",
    "bastão de cricket",
    "bengala de madeira",
    "unha",
    "impressora",
    "pá",
    "par de calças",
    "Monitor CRT",
    "espada de diamante",
    "baguete",
    "livro de física",
    "torradeira",
    "retrato de Richard Stallman",
    "televisão",
    "cabeça mau5",
    "caminhão de cinco toneladas",
    "rolo de fita adesiva",
    "livro",
    "computador portátil",
    "televisão antiga",
    "saco de pedras",
    "truta arco-íris",
    "bloco de paralelepípedos",
    "balde de lava",
    "galinha de borracha",
    "bastão com espinhos",
    "bloco de ouro",
    "extintor de incêndio",
    "pedra pesada",
    "pedaço de sujeira",
    "colméia",
    "pedaço de carne podre",
    "Urso",
    "tonelada de tijolos",
]

THROW = [
    "arremessa",
    "lança",
    "zune",
    "joga",
]

HIT = [
    "acerta",
    "golpeia",
    "estapeia",
    "bate",
    "surra",
]

WHERE = ["no peito", "na cabeça", "na bunda", "na virilha"]

# ===========================================


@register(outgoing=True, pattern=r"^\.(\w+)say (.*)")
async def univsaye(cowmsg):
    """ For .cowsay module, userbot wrapper for cow which says things. """
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern=r"^\.coinflip(?: |$)(.*)")
async def coin(event):
    r = choice(["heads", "tails"])
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r == "heads":
        if input_str == "heads":
            await event.edit("A moeda caiu em: **Cara**.\nComo esperado.")
        elif input_str == "tails":
            await event.edit("A moeda caiu em: **Cara**.\nMais sorte da próxima vez?")
        else:
            await event.edit("A moeda caiu em: **Cara**.")
    elif r == "tails":
        if input_str == "tails":
            await event.edit("A moeda caiu em: **Coroa*.\nComo esperado.")
        elif input_str == "heads":
            await event.edit("A moeda caiu em: **Coroa*.\nMais sorte da próxima vez?")
        else:
            await event.edit("A moeda caiu em: **Coroa*.")


@register(pattern=r"^\.slap(?: |$)(.*)", outgoing=True)
async def who(event):
    """ slaps a user, or get slapped if not a reply. """
    replied_user = await get_user_from_event(event)
    if replied_user:
        replied_user = replied_user[0]
    else:
        return
    caption = await slap(replied_user, event)

    try:
        await event.edit(caption)

    except BaseException:
        await event.edit(
            "**Não posso dar um tapa nesta pessoa, preciso buscar alguns paus e pedras!**"
        )


async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = f"@{username}"
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)
    where = choice(WHERE)

    return "..." + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw, where=where
    )


@register(outgoing=True, pattern=r"^\.(yes|no|maybe|decide)$")
async def decide(event):
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id or None
    if decision != "decide":
        r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = requests.get("https://yesno.wtf/api").json()
    await event.delete()
    await event.client.send_message(
        event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"]
    )


@register(outgoing=True, pattern=r"^\.cry$")
async def cry(e):
    """ y u du dis, i cry everytime !! """
    await e.edit(choice(CRI))


@register(outgoing=True, pattern=r"^\.insult$")
async def insult(e):
    """ I make you cry !! """
    await e.edit(choice(INSULT_STRINGS))


@register(outgoing=True, pattern=r"^\.cp(?: |$)(.*)")
async def copypasta(cp_e):
    """ Copypasta the famous meme """
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await cp_e.edit("`😂🅱️Me👐dÊ💞uM👅tExTo👅pRa✌️Eu👌DeIXaR👐engr👀aça💞do!💦`")
        return

    reply_text = choice(EMOJIS)
    # choose a random character in the message to be substituted with 🅱️
    b_char = choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += choice(EMOJIS)
        elif owo in EMOJIS:
            reply_text += owo
            reply_text += choice(EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🅱️"
        else:
            reply_text += owo.upper() if bool(getrandbits(1)) else owo.lower()
    reply_text += choice(EMOJIS)
    await cp_e.edit(reply_text)


@register(outgoing=True, pattern=r"^\.vapor(?: |$)(.*)")
async def vapor(vpr):
    """ Vaporize everything! """
    reply_text = []
    textx = await vpr.get_reply_message()
    message = vpr.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await vpr.edit("`Ｍｅ　ｄá　ｕｍ　ｔｅｘｔｏ　ｐｒａ　ｅｕ　ｖａｐｏｒａｒ！`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await vpr.edit("".join(reply_text))


@register(outgoing=True, pattern=r"^\.str(?: |$)(.*)")
async def stretch(stret):
    """ Stretch it."""
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await stret.edit("**Meeeeeee ddddddáááááááá uuuuummmmm teeeexxxxttttooo!**")
        return

    count = randint(3, 10)
    reply_text = sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), message)
    await stret.edit(reply_text)


@register(outgoing=True, pattern=r"^\.zal(?: |$)(.*)")
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    reply_text = []
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "`Me̷̛ ͝͞͠d҉͢͢á ̧u͝͡m ̕t̡e̸͟͠x̶̛͡t͠o ̀p̕͢r̕͟a҉ ̡̧̨eu ̨́͘d͢e̕͏i̷̡͝x́҉͘ar̸̡͡ ͢͟m̛èdon̶h́͝o͘`"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(3):
            zalgint = randint(0, 2)

            if zalgint == 0:
                charac = charac.strip() + choice(ZALG_LIST[0]).strip()
            elif zalgint == 1:
                charac = charac.strip() + choice(ZALG_LIST[1]).strip()
            else:
                charac = charac.strip() + choice(ZALG_LIST[2]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))


@register(outgoing=True, pattern=r"^\.hi$")
async def hoi(hello):
    """ Greet everyone! """
    await hello.edit(choice(HELLOSTR))


@register(outgoing=True, pattern=r"^\.owo(?: |$)(.*)")
async def faces(owo):
    """ UwU """
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU nenhum texto fornecido! `")
        return

    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(UWUS)
    await owo.edit(reply_text)


@register(outgoing=True, pattern=r"^\.react$")
async def react_meme(react):
    """ Make your userbot react to everything. """
    await react.edit(choice(FACEREACTS))


@register(outgoing=True, pattern=r"^\.shg$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    await shg.edit(choice(SHGS))


@register(outgoing=True, pattern=r"^\.chase$")
async def police(chase):
    """ Run boi run, i'm gonna catch you !! """
    await chase.edit(choice(CHASE_STR))


@register(outgoing=True, pattern=r"^\.run$")
async def runner_lol(run):
    """ Run, run, RUNNN! """
    await run.edit(choice(RUNS_STR))


@register(outgoing=True, pattern=r"^\.metoo$")
async def metoo(hahayes):
    """ Haha yes """
    await hahayes.edit(choice(METOOSTR))


@register(outgoing=True, pattern="^.Oof$")
async def Oof(e):
    t = "Oof"
    for _ in range(15):
        t = t[:-1] + "of"
        await e.edit(t)


@register(outgoing=True, pattern="^.oof$")
async def oof(e):
    t = "oof"
    for _ in range(15):
        t = t[:-1] + "of"
        await e.edit(t)


@register(outgoing=True, pattern=r"^\.mock(?: |$)(.*)")
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    reply_text = []
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await mock.edit("**mE Da AlGo pRa zuAr!**")
        return

    for charac in message:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))


@register(outgoing=True, pattern=r"^\.clap(?: |$)(.*)")
async def claptext(memereview):
    """ Praise people! """
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await memereview.edit("**Hah, eu não bato palmas inutilmente!**")
        return
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@register(outgoing=True, pattern=r"^\.bt$")
async def bluetext(bt_e):
    """ Believe me, you will find this useful. """
    if bt_e.is_group:
        await bt_e.edit(
            "/CORES_PRECISO_CLICAR\n"
            "/VOCE_E_UM_ANIMAL_ESTUPIDO_QUE_E_ATRAIDO_A_CORES\n"
            "/CLIQUE_AQUI"
        )


@register(outgoing=True, pattern=r"^\.f (.*)")
async def payf(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8,
        paytext * 8,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 6,
        paytext * 6,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
    )
    await event.edit(pay)


@register(outgoing=True, pattern=r"^\.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {"format": "json", "url": lfy_url}
    r = requests.get("http://is.gd/create.php", params=payload)
    await lmgtfy_q.edit(
        f"Aqui está, fique a vontade.\
    \n[{query}]({r.json()['shorturl']})"
    )


@register(pattern=r"^\.scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    """ Just a small command to fake chat actions for fun !! """
    options = [
        "typing",
        "contact",
        "game",
        "location",
        "voice",
        "round",
        "video",
        "photo",
        "document",
        "cancel",
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:  # Let bot decide action and time
        scam_action = choice(options)
        scam_time = randint(30, 60)
    elif len(args) == 1:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:  # User decides both action and time
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("**Sintaxe inválida!**")
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@register(pattern=r"^\.type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("**Dê um texto para digitar!**")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)


CMD_HELP.update(
    {
        "memes": ".cowsay\
\nUso: vaca que diz coisas.\
\n\n.cp\
\nUso: Copypasta, o famoso meme\
\n\n.vapor\
\nUso: Vaporize tudo!\
\n\n.str\
\nUso: Estique o texto.\
\n\n.zal\
\nUso: Invoque a sensação de caos.\
\n\n.Oof\
\nUso: Ooooof\
\n\n.oof\
\nUso: ooooof\
\n\n.hi\
\nUso: Cumprimente a todos!\
\n\n.coinflip <heads/tails>\
\nUso: Jogue a moeda !!\
\n\n.owo\
\nUso: UwU\
\n\n.react\
\nUso: Faça seu userbot reagir a tudo.\
\n\n.slap\
\nUso: responda para esbofeteá-los com objetos aleatórios !!\
\n\n.cry\
\nUso: pq tu faz iss, eu chorr.\
\n\n.shg\
\nUso: Dê de ombros !!\
\n\n.run\
\nUso: Deixe-me correr, corra, RUNNN!\
\n\n.chase\
\nUso: É melhor você começar a correr\
\n\n.metoo\
\nUso: Haha sim\
\n\n.mock\
\nUso: Faça e encontre a verdadeira diversão.\
\n\n.clap\
\nUso: Elogie a pessoas!\
\n\n.f <emoji/character>\
\nUso: Preste Respeitos.\
\n\n.bt\
\nUso: Acredite em mim, você achará isso útil.\
\n\n.type\
\nUso: Basta um pequeno comando para fazer seu teclado se tornar uma máquina de escrever!\
\n\n.lfy <query>\
\nUso: Deixe-me pesquisar isso no Google bem rápido!!\
\n\n.decide [Alternativas: (.yes, .no, .maybe)]\
\nUso: Tome uma decisão rápida.\
\n\n.scam <açao> <Tempo>\
\n[Ações disponíveis: (typing, contact, game, location, voice, round, video, photo, document, cancel)]\
\nUso: Crie ações de chat falsas, para se divertir. (Ação padrão: typing)\
\n\n\nObrigada a 🅱️ottom🅱️ext🅱️ot (@NotAMemeBot) por alguns destes."
    }
)
