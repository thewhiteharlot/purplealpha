# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for having some fun with people. """

import time
from asyncio import sleep
from collections import deque
from random import choice, getrandbits, randint
from re import sub

import requests
from cowpy import cow

from userbot import CMD_HELP, LOGS
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
        "̖",
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

IWIS = [
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

# Author: @Jisan7509
A = (
    "⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿\n"
    "⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿\n"
    "⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠻⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿\n"
    "⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿\n"
    "⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠸⣿⣿⣿\n"
    "⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠀⠤⠄⠀⠀⠉⠁⠀⠀⠀⢿⣿⣿\n"
    "⣿⣿⣿⣿⠀⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠠⣿⣿⣷⠀⣿⣿\n"
    "⣿⣿⣿⣿⡀⠀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠉⠉⠁⠀⣿⣿\n"
    "⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿\n"
    "⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿\n"
    "⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿\n"
    "⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿🅼🅰️ 🅺🅸 🅲🅷🆄⢸⣿⣿⣿⣿⣿⣿\n"
    "🅿️🅸🅺🅰️ 🅿️🅸🅺🅰️ 🅿️🅸🅺🅰️🅲🅷🆄\n"
)


B = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⡀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⠟⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠘⠻⣿⣷⣄⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⣴⣶⣿⡆⠀⠀⠉⠉⠀⠈⣶⡆⠀\n"
    "⠀⠀⠀⢠⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢻⣷⠀\n"
    "⠀⠀⠀⣼⣿⡿⠟⠀⠀⠀⠀⠀⠀⠀⣸⣿⡄\n"
    "⠀⠀⠀⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣷\n"
    "⠀⠀⠘⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⠏\n"
    "⠀⢠⣧⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠟⠁⠀\n"
    "⠀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ Ah\n shit, here we go again.\n"
)


C = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀\n"
    "⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀\n"
    "⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀\n"
    "⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀\n"
    "⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦\n"
    "⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟\n"
    "⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n"
    "⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇\n"
    "⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀\n"
    "⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀\n"
    "⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀\n"
    "⠄⠄⠄⠄⠄⠄⣠⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠄⠄⠄\n"
    "⠄⠄⣀⣤⣴⣾⣿⣷⣭⣭⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠄⠄\n"
    "⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣧⠄⠄\n"
    "⠄⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⡄⠄\n"
    "⠄⢸⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⡟⢛⢻⣷⢻⣿⣧⠄\n"
    "⠄⠄⣿⡏⣿⡟⡛⢻⣿⣿⣿⣿⠸⣿⣿⣿⣷⣬⣼⣿⢸⣿⣿⠄\n"
    "⠄⠄⣿⣧⢿⣧⣥⣾⣿⣿⣿⡟⣴⣝⠿⣿⣿⣿⠿⣫⣾⣿⣿⡆\n"
    "⠄⠄⢸⣿⣮⡻⠿⣿⠿⣟⣫⣾⣿⣿⣿⣷⣶⣾⣿⡏⣿⣿⣿⡇\n"
    "⠄⠄⢸⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⡇\n"
    "⠄⠄⢸⣿⣿⣿⡇⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠄\n"
    "⠄⠄⣼⣿⣿⣿⢃⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⡇⠄\n"
    "⠄⠄⠸⣿⣿⢣⢶⣟⣿⣖⣿⣷⣻⣮⡿⣽⣿⣻⣖⣶⣤⣭⡉⠄\n"
    "⠄⠄⠄⢹⠣⣛⣣⣭⣁⡛⠻⢽⣿⣿⣿⣿⢻⣿⣿⣿⣽⡧⡄⠄\n"
    "⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣶⣌⡛⢿⣽⢘⣿⣷⣿⡻⠏⣛⣀\n"
    "⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⡅⣿⠚⣡⣴⣿⣿⡆\n"
    "⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣱⣾⣿⣿⣿⣿⣿\n"
    "⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿\n"
    "⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⠿⣿⣿⣿\n"
    "⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⡟\n"
    "⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⠄⠄⢹⣿⣿⣿⣿⣿⣿⣿⡟\n"
    "⣸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠸⣿⣿⣿⣿⡿⢟⣣\n"
    "ɮǟȶǟʊ ȶɦǟʀӄɨօ ӄʏǟ ɦǟǟʟ ,ӄɛֆǟ ʟǟɢǟ\n"
)


D = (
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣧⣤⣤⠀⢠⣤⡄⢸⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿   ⠸⠿⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⠿⠷⣤⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡏⢀⣤⣤⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡇⠘⠿⠿⠃⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡿⠦⠤⠤⠴⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣧⣤⣤⣄⡀   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⡀   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠉⠉⢉⣉⣉⣉⣉⣉⣉⡉⠉⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⠻⠿⠿⠿⣿⡿⠿⠇⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⣤⣤⣤⣤⣾⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⢉⣩⣭⣭⣭⡄⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⣿⡟⠋⠉⠋⠁⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⣾⣿⣶⣶⣶⡆⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⣶⣶⣶⣶⣶⣶⣶⡆⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⣾⣏⠀⠀⣹⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⠘⠿⠿⠿⠟⠃⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
)


E = (
    "⠀⠀⠀⠀⢀⣀⣀⣀\n"
    "⠀⠀⠀⠰⡿⠿⠛⠛⠻⠿⣷\n"
    "⠀⠀⠀⠀⠀⠀⣀⣄⡀⠀⠀⠀⠀⢀⣀⣀⣤⣄⣀⡀\n"
    "⠀⠀⠀⠀⠀⢸⣿⣿⣷⠀⠀⠀⠀⠛⠛⣿⣿⣿⡛⠿⠷\n"
    "⠀⠀⠀⠀⠀⠘⠿⠿⠋⠀⠀⠀⠀⠀⠀⣿⣿⣿⠇\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁\n"
    "⠀\n"
    "⠀⠀⠀⠀⣿⣷⣄⠀⢶⣶⣷⣶⣶⣤⣀\n"
    "⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠈⠙⠻⠗\n"
    "⠀⠀⠀⣰⣿⣿⣿⠀⠀⠀⠀⢀⣀⣠⣤⣴⣶⡄\n"
    "⠀⣠⣾⣿⣿⣿⣥⣶⣶⣿⣿⣿⣿⣿⠿⠿⠛⠃\n"
    "⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄\n"
    "⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁\n"
    "⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁\n"
    "⠀⠀⠛⢿⣿⣿⣿⣿⣿⣿⡿⠟\n"
)


F = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠖⠲⢄\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠞⠁⠀⠀⠀⠀⢱\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⠀⠀⠀⠀⣸\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣄⠀⠀⠀⠀⢀⡠⠖⠁\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⠁⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣯⣿⣿⣿⣿⣿⠇⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⣻⣿⣿⣿⣿⣯⠏⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⣠⠾⣽⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀ ⠀⠀.⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⣴⣻⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⣠⢾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⣼⣷⣿⣿⣿⣿⣿⣿⣟⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⢸⢿⣿⣿⣿⣿⣿⣿⣿⣯⣻⡟⡆⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠸⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⡿⡇⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠹⣟⣿⣿⣿⣿⡿⣷⡿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠈⠛⠯⣿⡯⠟⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
)


G = (
    "⠄⠄⠄⠄⠄⣀⣀⣤⣶⣿⣿⣶⣶⣶⣤⣄⣠⣴⣶⣿⣶⣦⣄⠄\n"
    "⠄⣠⣴⣾⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦\n"
    "⢠⠾⣋⣭⣄⡀⠄⠙⠻⣿⣿⡿⠛⠋⠉⠉⠉⠙⠛⠿⣿⣿⣿⣿\n"
    "⡎⡟⢻⣿⣷⠄⠄⠄⠄⡼⣡⣾⣿⣿⣦⠄⠄⠄⠄⠄⠈⠛⢿⣿\n"
    "⡇⣷⣾⣿⠟⠄⠄⠄⢰⠁⣿⣇⣸⣿⣿⠄⠄⠄⠄⠄⠄⠄⣠⣼\n"
    "⣦⣭⣭⣄⣤⣤⣴⣶⣿⣧⡘⠻⠛⠛⠁⠄⠄⠄⠄⣀⣴⣿⣿⣿\n"
    "⢉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿\n"
    "⡿⠛⠛⠛⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⡇⠄⠄⢀⣀⣀⠄⠄⠄⠄⠉⠉⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⠈⣆⠄⠄⢿⣿⣿⣷⣶⣶⣤⣤⣀⣀⡀⠄⠄⠉⢻⣿⣿⣿⣿⣿\n"
    "⠄⣿⡀⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠄⢠⣿⣿⣿⣿⣿\n"
    "⠄⣿⡇⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠄⢀⣼⣿⣿⣿⣿⣿\n"
    "⠄⣿⡇⠄⠠⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⣠⣾⣿⣿⣿⣿⣿⣿\n"
    "⠄⣿⠁⠄⠐⠛⠛⠛⠉⠉⠉⠉⠄⠄⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⠄⠻⣦⣀⣀⣀⣀⣀⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋\n"
)


H = (
    "⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣵⣿⣿⣿⠿⡟⣛⣧⣿⣯⣿⣝⡻⢿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⠋⠁⣴⣶⣿⣿⣿⣿⣿⣿⣿⣦⣍⢿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⢷⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢼⣿⣿⣿⣿\n"
    "⢹⣿⣿⢻⠎⠔⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿\n"
    "⢸⣿⣿⠇⡶⠄⣿⣿⠿⠟⡛⠛⠻⣿⡿⠿⠿⣿⣗⢣⣿⣿⣿⣿\n"
    "⠐⣿⣿⡿⣷⣾⣿⣿⣿⣾⣶⣶⣶⣿⣁⣔⣤⣀⣼⢲⣿⣿⣿⣿\n"
    "⠄⣿⣿⣿⣿⣾⣟⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⢟⣾⣿⣿⣿⣿\n"
    "⠄⣟⣿⣿⣿⡷⣿⣿⣿⣿⣿⣮⣽⠛⢻⣽⣿⡇⣾⣿⣿⣿⣿⣿\n"
    "⠄⢻⣿⣿⣿⡷⠻⢻⡻⣯⣝⢿⣟⣛⣛⣛⠝⢻⣿⣿⣿⣿⣿⣿\n"
    "⠄⠸⣿⣿⡟⣹⣦⠄⠋⠻⢿⣶⣶⣶⡾⠃⡂⢾⣿⣿⣿⣿⣿⣿\n"
    "⠄⠄⠟⠋⠄⢻⣿⣧⣲⡀⡀⠄⠉⠱⣠⣾⡇⠄⠉⠛⢿⣿⣿⣿\n"
    "⠄⠄⠄⠄⠄⠈⣿⣿⣿⣷⣿⣿⢾⣾⣿⣿⣇⠄⠄⠄⠄⠄⠉⠉\n"
    "⠄⠄⠄⠄⠄⠄⠸⣿⣿⠟⠃⠄⠄⢈⣻⣿⣿⠄⠄⠄⠄⠄⠄⠄\n"
    "⠄⠄⠄⠄⠄⠄⠄⢿⣿⣾⣷⡄⠄⢾⣿⣿⣿⡄⠄⠄⠄⠄⠄⠄\n"
    "⠄⠄⠄⠄⠄⠄⠄⠸⣿⣿⣿⠃⠄⠈⢿⣿⣿⠄⠄⠄⠄⠄⠄⠄\n"
)


I = (
    "⣿⣿⣿⡇⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⡇⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⡇⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⡇⠄⣿⣿⣿⡿⠋⣉⣉⣉⡙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⠃⠄⠹⠟⣡⣶⢟⣛⣛⡻⢿⣦⣩⣤⣬⡉⢻⣿⣿⣿⣿\n"
    "⣿⣿⣿⠄⢀⢤⣾⣿⣿⣿⡿⠿⠿⠿⢮⡃⣛⡻⢿⠈⣿⣿⣿⣿\n"
    "⣿⡟⢡⣴⣯⣿⣿⣿⠤⣤⣭⣶⣶⣶⣮⣔⡈⠛⢓⠦⠈⢻⣿⣿\n"
    "⠏⣠⣿⣿⣿⣿⣿⣿⣯⡪⢛⠿⢿⣿⣿⣿⡿⣼⣿⣿⣮⣄⠙⣿\n"
    "⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⡭⠴⣶⣶⣽⣽⣛⡿⠿⠿⠇⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣷⣝⣛⢛⢋⣥⣴⣿⣿\n"
    "⣿⣿⣿⣿⣿⢿⠱⣿⣛⠾⣭⣛⡿⢿⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿\n"
    "⠑⠽⡻⢿⣮⣽⣷⣶⣯⣽⣳⠮⣽⣟⣲⠯⢭⣿⣛⡇⣿⣿⣿⣿\n"
    "⠄⠄⠈⠑⠊⠉⠟⣻⠿⣿⣿⣿⣷⣾⣭⣿⠷⠶⠂⣴⣿⣿⣿⣿\n"
    "⠄⠄⠄⠄⠄⠄⠄⠁⠙⠒⠙⠯⠍⠙⢉⣡⣶⣿⣿⣿⣿⣿⣿⣿\n"
    "⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
)


J = (
    "⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⡉⣉⡛⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⡿⠋⠁⠄⠄⠄⠄⠄⢀⣸⣿⣿⡿⠿⡯⢙⠿⣿⣿⣿⣿\n"
    "⣿⣿⡿⠄⠄⠄⠄⠄⡀⡀⠄⢀⣀⣉⣉⣉⠁⠐⣶⣶⣿⣿⣿⣿\n"
    "⣿⣿⡇⠄⠄⠄⠄⠁⣿⣿⣀⠈⠿⢟⡛⠛⣿⠛⠛⣿⣿⣿⣿⣿\n"
    "⣿⣿⡆⠄⠄⠄⠄⠄⠈⠁⠰⣄⣴⡬⢵⣴⣿⣤⣽⣿⣿⣿⣿⣿\n"
    "⣿⣿⡇⠄⢀⢄⡀⠄⠄⠄⠄⡉⠻⣿⡿⠁⠘⠛⡿⣿⣿⣿⣿⣿\n"
    "⣿⡿⠃⠄⠄⠈⠻⠄⠄⠄⠄⢘⣧⣀⠾⠿⠶⠦⢳⣿⣿⣿⣿⣿\n"
    "⣿⣶⣤⡀⢀⡀⠄⠄⠄⠄⠄⠄⠻⢣⣶⡒⠶⢤⢾⣿⣿⣿⣿⣿\n"
    "⣿⡿⠋⠄⢘⣿⣦⡀⠄⠄⠄⠄⠄⠉⠛⠻⠻⠺⣼⣿⠟⠛⠿⣿\n"
    "⠋⠁⠄⠄⠄⢻⣿⣿⣶⣄⡀⠄⠄⠄⠄⢀⣤⣾⣿⡀⠄⠄⠄⢹\n"
    "⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣷⡤⠄⠰⡆⠄⠄⠈⠛⢦⣀⡀⡀⠄\n"
    "⠄⠄⠄⠄⠄⠄⠈⢿⣿⠟⡋⠄⠄⠄⢣⠄⠄⠄⠄⠄⠈⠹⣿⣀\n"
    "⠄⠄⠄⠄⠄⠄⠄⠘⣷⣿⣿⣷⠄⠄⢺⣇⠄⠄⠄⠄⠄⠄⠸⣿\n"
    "⠄⠄⠄⠄⠄⠄⠄⠄⠹⣿⣿⡇⠄⠄⠸⣿⡄⠄⠈⠁⠄⠄⠄⣿\n"
    "⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⡇⠄⠄⠄⢹⣧⠄⠄⠄⠄⠄⠄⠘\n"
)


K = (
    "⣿⣿⣿⣿⠟⠋⢁⢁⢁⢁⢁⢁⢁⢁⠈⢻⢿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿⣿⣿\n"
    "⣿⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿⣿⣿\n"
    "⣿⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿⣿⣿\n"
    "⣿⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿⣿⣿\n"
    "⣿⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉⠙⠻\n"
    "⡿⠟⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄\n"
    "⠄⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄\n"
    "⠄⠄⠄⠄⠄⣸⣿⡷⡇⠄⣴⣾⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
    "⠄⠄⠄⠄⠄⣿⣿⠃⣦⣄⣿⣿⣿⠇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
    "⠄⠄⠄⠄⢸⣿⠗⢈⡶⣷⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
)


L = (
    "___________ \n"
    "　　　　　| \n"
    "　　　　　| \n"
    "　　　　　| \n"
    "　　　　　| \n"
    "　　　　　| \n"
    "　　　　　| \n"
    "　／￣￣＼| \n"
    "＜ ´･ 　　 |＼ \n"
    "　|　３　 | 丶＼ \n"
    "＜ 、･　　|　　＼ \n"
    "　＼＿＿／∪ _ ∪) \n"
    "　　　　　 Ｕ Ｕ\n"
)

M = r"_/﹋\_\n" "(҂`_´)\n" f"<,︻╦╤─ ҉ - - - 🤯\n" r"_/﹋\_\n"

N = (
    "▄███████▄\n"
    "█▄█████▄█\n"
    "█▼▼▼▼▼█\n"
    "██________█▌\n"
    "█▲▲▲▲▲█\n"
    "█████████\n"
    "_████\n"
)

O = (
    "┈┈┏━╮╭━┓┈╭━━━━╮\n"
    "┈┈┃┏┗┛┓┃╭┫ⓞⓘⓝⓚ┃\n"
    "┈┈╰┓▋▋┏╯╯╰━━━━╯\n"
    "┈╭━┻╮╲┗━━━━╮╭╮┈\n"
    "┈┃▎▎┃╲╲╲╲╲╲┣━╯┈\n"
    "┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n"
    "┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n"
    "┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈\n"
)

P = (
    "░▐█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄\n"
    "░███████████████████████ \n"
    "░▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓◤ \n"
    "░▀░▐▓▓▓▓▓▓▌▀█░░░█▀░\n"
    "░░░▓▓▓▓▓▓█▄▄▄▄▄█▀░░\n"
    "░░█▓▓▓▓▓▌░░░░░░░░░░\n"
    "░▐█▓▓▓▓▓░░░░░░░░░░░\n"
    "░▐██████▌░░░░░░░░░░\n"
)

Q = (
    "╥━━━━━━━━╭━━╮━━┳\n"
    "╢╭╮╭━━━━━┫┃▋▋━▅┣\n"
    "╢┃╰┫┈┈┈┈┈┃┃┈┈╰┫┣\n"
    "╢╰━┫┈┈┈┈┈╰╯╰┳━╯┣\n"
    "╢┊┊┃┏┳┳━━┓┏┳┫┊┊┣\n"
    "╨━━┗┛┗┛━━┗┛┗┛━━┻\n"
)
R = "╔┓┏╦━╦┓╔┓╔━━╗\n" "║┗┛║┗╣┃║┃║X X║\n" "║┏┓║┏╣┗╣┗╣╰╯║\n" "╚┛┗╩━╩━╩━╩━━╝\n"
S = (
    "▬▬▬.◙.▬▬▬ \n"
    "═▂▄▄▓▄▄▂ \n"
    "◢◤ █▀▀████▄▄▄▄◢◤ \n"
    "█▄ █ █▄ ███▀▀▀▀▀▀▀╬ \n"
    "◥█████◤ \n"
    "══╩══╩══ \n"
    "╬═╬ \n"
    "╬═╬ \n"
    "╬═╬ \n"
    "╬═╬ \n"
    "╬═╬ \n"
    "╬═╬ \n"
    "╬═╬ Olá, meu amigo :D \n"
    "╬═╬☻/ \n"
    "╬═╬/▌ \n"
    "╬═╬/ \\n"
)

T = (
    "┳┻┳┻╭━━━━╮╱▔▔▔╲\n"
    "┻┳┻┳┃╯╯╭━┫▏╰╰╰▕\n"
    "┳┻┳┻┃╯╯┃▔╰┓▔▂▔▕╮\n"
    "┻┳┻┳╰╮╯┃┈╰┫╰━╯┏╯\n"
    "┳┻┳┻┏╯╯┃╭━╯┳━┳╯\n"
    "┻┳┻┳╰━┳╯▔╲╱▔╭╮▔╲\n"
    "┳┻┳┻┳┻┃┈╲┈╲╱╭╯╮▕\n"
    "┻┳┻┳┻┳┃┈▕╲▂╱┈╭╯╱\n"
    "┳┻┳┻┳┻┃'''┈┃┈┃┈'''╰╯\n"
    "┻┳┻┳┻┏╯▔'''╰┓┣━┳┫\n"
    "┳┻┳┻┳╰┳┳┳'''╯┃┈┃┃\n"
    "┻┳┻┳┻┳┃┃┃┈'''┃┈┃┃\n"
    "┳┻┳┻┳┻┃┃┃'''┊┃┈┃┃\n"
    "┻┳┻┳┻┳┃┃┃┈'''┃┈┃┃.\n"
    "┳┻┳┻┳┻┣╋┫'''┊┣━╋┫\n"
    "┻┳┻┳┻╭╯╰╰-╭╯━╯.''╰╮\n"
    "**Eu te amo 💕** \n"
)

U = (
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡿⠋⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠀⣠⣾⣿⡿⠋⠀⠀⠉⠻⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⠃⠀⠀⣀⡀⠀⢹⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡄⠀⠙⠻⠋⠀⠀⣸⣿⣿⠀⠀⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⣰⣿⣿⠟⠀⢠⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡿⠛⠛⠒⠶⠾⢿⣿⣿⣷⣄⣾⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⢰⣿⣿⣷⣶⣦⣼⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡀⠀⠙⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⢿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⠀⠀⠀⠉⠉⠛⠛⠛⠶⢶⣤⣼⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣦⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠁⠀⣾⣿⣷⡄⠀⢼⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠀⢿⣿⣿⡿⠀⠈⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣇⠀⠀⠉⠋⠁⠀⢠⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠿⢷⣤⣀⣀⣀⣠⣾⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠉⠉⠛⢻⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣀⠀⠀⢸⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠹⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠙⠻⣀⣀⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠁⠀⣀⡀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⢸⣿⡇⠀⣷⡀⠘⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡄⠈⢻⡇⠀⡿⠃⠀⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣷⣄⢸⡇⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠉⠉⠑⠒⠲⠿⢿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣤⣄⣀⡀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⢺⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠀⠉⠉⠙⠋⠀⠀⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣤⣤⣀⣀⡀⠀⠀⣰⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣷⠀⢹⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⠉⠉⠀⠀⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣶⣤⣤⣀⣀⣀⣀⣰⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡟⠉⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⢀⣤⡄⠀⡀⠀⢹⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠀⢸⣿⡇⠀⣿⡄⠈⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡆⠀⢹⡇⠀⠟⠁⢀⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣦⣸⡇⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
)

V = (
    "⣿⣿⣿⣿⣿⣍⠀⠉⠻⠟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⠓⠀⠀⢒⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿\n"
    "⣿⡿⠋⠋⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⢿⣿⣿⡿⣿⣿⡟⠋⠀⢀⣩\n"
    "⣿⣿⡄⠀⠀⠀⠀⠀⠁⡀⠀⠀⠀⠀⠈⠉⠛⢷⣭⠉⠁⠀⠀⣿⣿\n"
    "⣇⣀. INDIA🇮🇳INDIA🇮🇳⠆⠠..⠘⢷⣿⣿⣛⠐⣶⣿⣿\n"
    "⣿⣄⠀⣰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢀⣠⣿⣿⣿⣾⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⠀⠀⡠⠀⠀⠀⠀⠀⢀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠄⠀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⣠⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⠀⠀⠂⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣇⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⡆⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "⣿⣿⣿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
    "**🇮🇳EU ODEIO SER INDIANO🇮🇳**\n"
)


W = (
    "───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───\n"
    "───█▒▒░░░░░░░░░▒▒█───\n"
    "────█░░█░░░░░█░░█────\n"
    "─▄▄──█░░░▀█▀░░░█──▄▄─\n"
    "█░░█─▀▄░░░░░░░▄▀─█░░█\n"
    "█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█\n"
    "█░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█\n"
    "█░░║║║╠─║─║─║║║║║╠─░░█\n"
    "█░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█\n"
    "█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█\n"
)

X = (
    "░░░░▓\n"
    "░░░▓▓\n"
    "░░█▓▓█\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░░░██▓▓██\n"
    "░░░░██▓▓██\n"
    "░░░██▓▓██\n"
    "░░██▓▓██\n"
    "░░██▓▓██\n"
    "░░██▓▓██\n"
    "░░██▓▓██\n"
    "░░██▓▓██\n"
    "░░██▓▓██\n"
    "░░░██▓▓███\n"
    "░░░░██▓▓████\n"
    "░░░░░██▓▓█████\n"
    "░░░░░░██▓▓██████\n"
    "░░░░░░███▓▓███████\n"
    "░░░░░████▓▓████████\n"
    "░░░░█████▓▓█████████\n"
    "░░░█████░░░█████●███\n"
    "░░████░░░░░░░███████\n"
    "░░███░░░░░░░░░██████\n"
    "░░██░Ab Mar Bsdk░████\n"
    "░░░░░░░░░░░░░░░░███\n"
    "░░░░░░░░░░░░░░░░░░░\n"
)


Y = (
    "────██──────▀▀▀██\n"
    "──▄▀█▄▄▄─────▄▀█▄▄▄\n"
    "▄▀──█▄▄──────█─█▄▄\n"
    "─▄▄▄▀──▀▄───▄▄▄▀──▀▄\n"
    "─▀───────▀▀─▀───────▀▀\n🚶🏻‍♂️🚶🏻‍♂️ɮʏɛ ʄʀɨɛռɖֆ.."
)

Z = (
    "╭━━━┳╮╱╱╭╮╱╭━━━┳━━━╮\n"
    "┃╭━╮┃┃╱╭╯╰╮┃╭━╮┃╭━╮┃\n"
    "┃╰━━┫╰━╋╮╭╯┃┃╱┃┃╰━━╮\n"
    "╰━━╮┃╭╮┣┫┃╱┃┃╱┃┣━━╮┃\n"
    "┃╰━╯┃┃┃┃┃╰╮┃╰━╯┃╰━╯┃\n"
    "╰━━━┻╯╰┻┻━╯╰━━━┻━━━╯\n"
)


AA = (
    "███████▄▄███████████▄\n"
    "▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n"
    "▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n"
    "▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n"
    "▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n"
    "▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n"
    "▓▓▓▓▓▓███░░░░░░░░░░░░█\n"
    "██████▀░░█░░░░██████▀\n"
    "░░░░░░░░░█░░░░█\n"
    "░░░░░░░░░░█░░░█\n"
    "░░░░░░░░░░░█░░█\n"
    "░░░░░░░░░░░█░░█\n"
    "░░░░░░░░░░░░▀▀\n"
)

# ===========================================


@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
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


@register(outgoing=True, pattern="^:/$", ignore_unsafe=True)
async def kek(keks):
    """ Check yourself ;)"""
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@register(outgoing=True, pattern=r"^.coinflip (.*)")
async def coin(event):
    r = choice(["heads", "tails"])
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r == "heads":
        if input_str == "heads":
            await event.edit("A moeda caiu em: **Cara**.\nVocê venceu.")
        elif input_str == "tails":
            await event.edit(
                "A moeda caiu em: **Cara**.\nVocê perdeu, tente de novo..."
            )
        else:
            await event.edit("A moeda caiu em: **Cara**.")
    elif r == "tails":
        if input_str == "tails":
            await event.edit("A moeda caiu em: **Coroa**.\nVocê venceu.")
        elif input_str == "heads":
            await event.edit(
                "A moeda caiu em: **Coroa**.\nVocê perdeu, tente de novo..."
            )
        else:
            await event.edit("A moeda caiu em: **Coroa**.")


@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
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
            "`Não posso dar um tapa nessa pessoa, preciso buscar alguns paus e pedras !!`"
        )


async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)
    where = choice(WHERE)

    caption = "..." + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw, where=where
    )

    return caption


@register(outgoing=True, pattern="^-_-$", ignore_unsafe=True)
async def emo(sigh):
    """Ok..."""
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        await sigh.edit(okay)


@register(outgoing=True, pattern="^.(yes|no|maybe|decide)$")
async def decide(event):
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id if event.reply_to_msg_id else None
    if decision != "decide":
        r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = requests.get(f"https://yesno.wtf/api").json()
    await event.delete()
    await event.client.send_message(
        event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"]
    )


@register(outgoing=True, pattern="^;_;$", ignore_unsafe=True)
async def fun(idk):
    t = ";_;"
    for j in range(10):
        t = t[:-1] + "_;"
        await idk.edit(t)


@register(outgoing=True, pattern="^.fp$")
async def facepalm(palm):
    """Facepalm  🤦‍♂"""
    await palm.edit("🤦‍♂")


@register(outgoing=True, pattern="^.cry$")
async def cry(cying):
    """y u du dis, i cry everytime !!"""
    await cying.edit(choice(CRI))


@register(outgoing=True, pattern="^.insult$")
async def insult(rude):
    """I make you cry !!"""
    await rude.edit(choice(INSULT_STRINGS))


@register(outgoing=True, pattern="^.cp(?: |$)(.*)")
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
            if bool(getrandbits(1)):
                reply_text += owo.upper()
            else:
                reply_text += owo.lower()
    reply_text += choice(EMOJIS)
    await cp_e.edit(reply_text)


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
async def vapor(vpr):
    """ Vaporize everything! """
    reply_text = list()
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


@register(outgoing=True, pattern="^.str(?: |$)(.*)")
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
        await stret.edit("`Meeeeeee ddddddáááááááá uuuuummmmm teeeexxxxttttooo!`")
        return

    count = randint(3, 10)
    reply_text = sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), message)
    await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    reply_text = list()
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "Me̷̛ ͝͞͠d҉͢͢á ̧u͝͡m ̕t̡e̸͟͠x̶̛͡t͠o ̀p̕͢r̕͟a҉ ̡̧̨eu ̨́͘d͢e̕͏i̷̡͝x́҉͘ar̸̡͡ ͢͟m̛èdon̶h́͝o͘"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(0, 3):
            textz = randint(0, 2)

            if textz == 0:
                charac = charac.strip() + choice(ZALG_LIST[0]).strip()
            elif textz == 1:
                charac = charac.strip() + choice(ZALG_LIST[1]).strip()
            else:
                charac = charac.strip() + choice(ZALG_LIST[2]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))


@register(outgoing=True, pattern="^.hi$")
async def hoi(hello):
    """ Greet everyone! """
    await hello.edit(choice(HELLOSTR))


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
async def face(owo):
    """UwU"""
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU sem texto base! `")
        return

    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(UWUS)
    await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
async def react_meme(react):
    """ Make your userbot react to everything. """
    await react.edit(choice(FACEREACTS))


@register(outgoing=True, pattern="^.iwi(?: |$)(.*)")
async def faces(siwis):
    """ IwI """
    textx = await siwis.get_reply_message()
    message = siwis.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await siwis.edit("` IwI sem texto base! `")
        return

    reply_text = sub(r"(a|i|u|e|o)", "i", message)
    reply_text = sub(r"(A|I|U|E|O)", "I", reply_text)
    reply_text = sub(r"\!+", " " + choice(IWIS), reply_text)
    reply_text += " " + choice(IWIS)
    await siwis.edit(reply_text)


@register(outgoing=True, pattern="^.shg$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    await shg.edit(choice(SHGS))


@register(outgoing=True, pattern="^.chase$")
async def police(chase):
    """ Run boi run, i'm gonna catch you !! """
    await chase.edit(choice(CHASE_STR))


@register(outgoing=True, pattern="^.run$")
async def runner_lol(run):
    """ Run, run, RUNNN! """
    await run.edit(choice(RUNS_STR))


@register(outgoing=True, pattern="^.metoo$")
async def metoo(hahayes):
    """ Haha yes """
    await hahayes.edit(choice(METOOSTR))


@register(outgoing=True, pattern="^.iff$")
async def pressf(f):
    """Pays respects"""
    args = f.text.split()
    arg = (f.text.split(" ", 1))[1] if len(args) > 1 else None
    if len(args) == 1:
        r = randint(0, 3)
        LOGS.info(r)
        if r == 0:
            await f.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")
        elif r == 1:
            await f.edit("╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯")
        else:
            arg = "F"
    if arg is not None:
        out = ""
        F_LENGTHS = [5, 1, 1, 4, 1, 1, 1]
        for line in F_LENGTHS:
            c = max(round(line / len(arg)), 1)
            out += (arg * c) + "\n"
        await f.edit("`" + out + "`")


@register(outgoing=True, pattern="^Oof$")
async def Oof(woof):
    t = "Oof"
    for j in range(15):
        t = t[:-1] + "of"
        await woof.edit(t)


@register(outgoing=True, pattern="^.moon$")
async def moon(moone):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            await sleep(0.1)
            await moone.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.earth$")
async def earth(event):
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.clock$")
async def clock(event):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    reply_text = list()
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await mock.edit("`mE Da AlGo pRa zuAr!`")
        return

    for charac in message:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
async def claptext(memereview):
    """ Praise people! """
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await memereview.edit("`Hah, eu não bato palmas inutilmente!`")
        return
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@register(outgoing=True, pattern="^.bt$")
async def bluetext(bt_e):
    """ Believe me, you will find this useful. """
    if await bt_e.get_reply_message() and bt_e.is_group:
        await bt_e.edit(
            "/TEXTOAZUL /DEVO /CLICAR.\n"
            "/VOCe /E /UM /ANIMAL /ESTUPIDO /QUE /E /ATRAIDO /A /CORES?"
        )


@register(outgoing=True, pattern=r"^.f (.*)")
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


@register(outgoing=True, pattern="^.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"https://lmgtfy.app/?q={query_encoded}"
    payload = {"format": "json", "url": lfy_url}
    r = requests.get("http://is.gd/create.php", params=payload)
    await lmgtfy_q.edit(
        f"Aqui está, sirva-se.\
    \n[{query}]({r.json()['shorturl']})"
    )


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
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
        await event.edit("`Sintaxe inválida !!`")
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("`Dê um texto para digitar!`")
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


@register(outgoing=True, pattern="^.fail$")
async def fail(faill):
    if not faill.text[0].isalpha() and faill.text[0] not in ("/", "#", "@", "!"):
        await faill.edit(
            "`\n▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ `"
            "`\n████▌▄▌▄▐▐▌█████ `"
            "`\n████▌▄▌▄▐▐▌▀████ `"
            "`\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ `"
        )


@register(outgoing=True, pattern="^.lol$")
async def lol(lel):
    if not lel.text[0].isalpha() and lel.text[0] not in ("/", "#", "@", "!"):
        await lel.edit(
            "`\n╱┏┓╱╱╱╭━━━╮┏┓╱╱╱╱ `"
            "`\n╱┃┃╱╱╱┃╭━╮┃┃┃╱╱╱╱ `"
            "`\n╱┃┗━━┓┃╰━╯┃┃┗━━┓╱ `"
            "`\n╱┗━━━┛╰━━━╯┗━━━┛╱ `"
        )


@register(outgoing=True, pattern="^.lool$")
async def lool(lul):
    if not lul.text[0].isalpha() and lul.text[0] not in ("/", "#", "@", "!"):
        await lul.edit(
            "`\n╭╭━━━╮╮┈┈┈┈┈┈┈┈┈┈\n┈┃╭━━╯┈┈┈┈▕╲▂▂╱▏┈\n┈┃┃╱▔▔▔▔▔▔▔▏╱▋▋╮┈`"
            "`\n┈┃╰▏┃╱╭╮┃╱╱▏╱╱▆┃┈\n┈╰━▏┗━╰╯┗━╱╱╱╰┻┫┈\n┈┈┈▏┏┳━━━━▏┏┳━━╯┈`"
            "`\n┈┈┈▏┃┃┈┈┈┈▏┃┃┈┈┈┈ `"
        )


@register(outgoing=True, pattern="^.stfu$")
async def stfu(shutup):
    if not shutup.text[0].isalpha() and shutup.text[0] not in ("/", "#", "@", "!"):
        await shutup.edit(
            "`\n█████████████████████████████████`"
            "`\n██▀▀▀▀████▀▀▀▀████▀▀▀▀▀███▀▀██▀▀█`"
            "`\n█──────██──────██───────██──██──█`"
            "`\n█──██▄▄████──████──███▄▄██──██──█`"
            "`\n█▄────▀████──████────█████──██──█`"
            "`\n█▀▀██──████──████──███████──██──█`"
            "`\n█──────████──████──███████──────█`"
            "`\n██▄▄▄▄█████▄▄████▄▄████████▄▄▄▄██`"
            "`\n█████████████████████████████████`"
        )


@register(outgoing=True, pattern="^.gtfo$")
async def gtfo(getout):
    if not getout.text[0].isalpha() and getout.text[0] not in ("/", "#", "@", "!"):
        await getout.edit(
            "`\n███████████████████████████████ `"
            "`\n█▀▀▀▀▀▀▀█▀▀▀▀▀▀█▀▀▀▀▀▀▀█▀▀▀▀▀▀█ `"
            "`\n█───────█──────█───────█──────█ `"
            "`\n█──███──███──███──███▄▄█──██──█ `"
            "`\n█──███▄▄███──███─────███──██──█ `"
            "`\n█──██───███──███──██████──██──█ `"
            "`\n█──▀▀▀──███──███──██████──────█ `"
            "`\n█▄▄▄▄▄▄▄███▄▄███▄▄██████▄▄▄▄▄▄█ `"
            "`\n███████████████████████████████ `"
        )


@register(outgoing=True, pattern="^.nih$")
async def nih(rose):
    if not rose.text[0].isalpha() and rose.text[0] not in ("/", "#", "@", "!"):
        await rose.edit(
            r"`(\_/)`"
            "`\n(●_●)`"
            "`\n />🌹 *tome`"
            "\n\n"
            r"`(\_/)`"
            "`\n(●_●)\n`"
            r"`🌹<\  *me devolve`"
        )


@register(outgoing=True, pattern="^.fag$")
async def ugay(faggot):
    if not faggot.text[0].isalpha() and faggot.text[0] not in ("/", "#", "@", "!"):
        await faggot.edit(
            "`\n█████████`"
            "`\n█▄█████▄█`"
            "`\n█▼▼▼▼▼`"
            "`\n█       STFU TROXA`"
            "`\n█▲▲▲▲▲`"
            "`\n█████████`"
            "`\n ██   ██`"
        )


@register(outgoing=True, pattern="^.taco$")
async def taco(tacoo):
    if not tacoo.text[0].isalpha() and tacoo.text[0] not in ("/", "#", "@", "!"):
        await tacoo.edit(r"\n{\__/}" "\n(●_●)" "\n( >🌮 Quer um taco?")


@register(outgoing=True, pattern="^.paw$")
async def paw(pawed):
    if not pawed.text[0].isalpha() and pawed.text[0] not in ("/", "#", "@", "!"):
        await pawed.edit("`(=ↀωↀ=)")


@register(outgoing=True, pattern="^.tf$")
async def tf(focc):
    if not focc.text[0].isalpha() and focc.text[0] not in ("/", "#", "@", "!"):
        await focc.edit("(̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄  ")


@register(outgoing=True, pattern="^.gey$")
async def gey(gai):
    if not gai.text[0].isalpha() and gai.text[0] not in ("/", "#", "@", "!"):
        await gai.edit(
            "`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
            "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
            "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈NIGGA U GEY`"
            "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈"
        )


@register(outgoing=True, pattern="^.gay$")
async def gay(ugay):
    if not ugay.text[0].isalpha() and ugay.text[0] not in ("/", "#", "@", "!"):
        await ugay.edit(
            "`\n┈┈┈╭━━━━━╮┈┈┈┈┈\n┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈`"
            "`\n┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n┈┈╭┻┊┊╰━┻━╮┈┈┈┈`"
            "`\n┈┈╰┳┊╭━━━┳╯┈┈┈┈\n┈┈┈┃┊┃╰━━┫┈BRUH U GAY`"
            "\n┈┈┈┈┈┈┏━┓┈┈┈┈┈┈"
        )


@register(outgoing=True, pattern="^.bot$")
async def bot(robot):
    if not robot.text[0].isalpha() and robot.text[0] not in ("/", "#", "@", "!"):
        await robot.edit(
            "` \n   ╲╲╭━━━━╮ \n╭╮┃▆┈┈▆┃╭╮ \n┃╰┫▽▽▽┣╯┃ \n╰━┫△△△┣━╯`"
            "`\n╲╲┃┈┈┈┈┃  \n╲╲┃┈┏┓┈┃ `"
        )


@register(outgoing=True, pattern="^.hey$")
async def hey(heyo):
    if not heyo.text[0].isalpha() and heyo.text[0] not in ("/", "#", "@", "!"):
        await heyo.edit(
            "\n┈┈┈╱▔▔▔▔╲┈╭━━━━━\n┈┈▕▂▂▂▂▂▂▏┃HEY!┊😀`"
            "`\n┈┈▕▔▇▔▔┳▔▏╰┳╮HEY!┊\n┈┈▕╭━╰╯━╮▏━╯╰━━━\n╱▔▔▏▅▅▅▅▕▔▔╲┈┈┈┈`"
            "`\n▏┈┈╲▂▂▂▂╱┈┈┈▏┈┈┈`"
        )


@register(outgoing=True, pattern="^.nou$")
async def nou(noway):
    if not noway.text[0].isalpha() and noway.text[0] not in ("/", "#", "@", "!"):
        await noway.edit(
            "`\n┈╭╮╭╮\n┈┃┃┃┃\n╭┻┗┻┗╮`"
            "`\n┃┈▋┈▋┃\n┃┈╭▋━╮━╮\n┃┈┈╭╰╯╰╯╮`"
            "`\n┫┈┈  NoU\n┃┈╰╰━━━━╯`"
            "`\n┗━━┻━┛`"
        )


# Author: @Kraken_The_BadASS


@register(outgoing=True, pattern="^.alone$")
async def alone(event):
    await event.edit("O")
    await sleep(0.7)
    await event.edit("O d")
    await sleep(0.7)
    await event.edit("O di")
    await sleep(0.7)
    await event.edit("O dia")
    await sleep(0.7)
    await event.edit("O dia q")
    await sleep(0.7)
    await event.edit("O dia qu")
    await sleep(0.7)
    await event.edit("O dia que")
    await sleep(0.7)
    await event.edit("O dia que e")
    await sleep(0.7)
    await event.edit("O dia que eu")
    await sleep(0.7)
    await event.edit("O dia que eu a")
    await sleep(0.7)
    await event.edit("O dia que eu ap")
    await sleep(0.7)
    await event.edit("O dia que eu apr")
    await sleep(0.7)
    await event.edit("O dia que eu apre")
    await sleep(0.7)
    await event.edit("O dia que eu apren")
    await sleep(0.7)
    await event.edit("O dia que eu aprend")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a v")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a vi")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viv")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a vive")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver s")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver so")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver soz")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozi")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinh")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nT")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTu")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTud")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo f")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo fi")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo fic")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo fico")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou m")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou ma")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mai")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais b")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais bo")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais bon")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais boni")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais bonit")
    await sleep(0.7)
    await event.edit("O dia que eu aprendi a viver sozinho \nTudo ficou mais bonito.")
    await sleep(0.7)
    await event.edit(
        "**O dia que eu aprendi a viver sozinho \nTudo ficou mais bonito.**ðŸ™‚"
    )


# Author: sawan(@veryhelpful)


@register(outgoing=True, pattern="^.mst$")
async def mst(event):
    await event.edit("MST hu bbro ")
    await sleep(1)
    await event.edit("╔═╦═╗╔══╗╔══╗\n║║║║║║══╣╚╗╔╝\n║║║║║╠══║─║║─\n╚╩═╩╝╚══╝─╚╝─")


@register(outgoing=True, pattern="^.gm$")
async def gm(event):
    await event.edit("Bom Dia ")
    await sleep(1)
    await event.edit("╔══╗╔═╦═╗\n║╔═╣║║║║║\n║╚╗║║║║║║\n╚══╝╚╩═╩╝")


@register(outgoing=True, pattern="^.good$")
async def good(event):
    await event.edit("╔══╗╔═╗╔═╗╔══╗\n║╔═╣║║║║║║╚╗╗║\n║╚╗║║║║║║║╔╩╝║\n╚══╝╚═╝╚═╝╚══╝")


@register(outgoing=True, pattern="^.hhlo$")
async def hhlo(event):
    await event.edit("Hello, como você está")
    await sleep(1)
    await event.edit("╔╗╔╗╔╗─╔═╗\n║╚╝║║║─║║║\n║╔╗║║╚╗║║║\n╚╝╚╝╚═╝╚═╝")


@register(outgoing=True, pattern="^.sry$")
async def sry(event):
    await event.edit("Eu sinto Muito")
    await sleep(1)
    await event.edit("Ultima vez,me perdoe")
    await sleep(1)
    await event.edit(
        "╔══╗╔═╗╔═╗╔═╗╔═╦╗\n║══╣║║║║╬║║╬║╚╗║║\n╠══║║║║║╗╣║╗╣╔╩╗║\n╚══╝╚═╝╚╩╝╚╩╝╚══╝"
    )


@register(outgoing=True, pattern="^.thnq$")
async def thnq(event):
    await event.edit("Obrigado pela ajuda")
    await sleep(1)
    await event.edit(
        "╔══╗╔╗╔╗╔══╗╔═╦╗╔╦╗╔══╗\n╚╗╔╝║╚╝║║╔╗║║║║║║╔╝║══╣\n─║║─║╔╗║║╠╣║║║║║║╚╗╠══║\n─╚╝─╚╝╚╝╚╝╚╝╚╩═╝╚╩╝╚══╝"
    )


@register(outgoing=True, pattern="^.ok$")
async def ok(event):
    await event.edit("▒▐█▀▀█▌▒▐█▒▐▀\n▒▐█▄▒█▌▒▐██▌░\n▒▐██▄█▌▒▐█▒▐▄")


@register(outgoing=True, pattern="^.smile$")
async def smile(event):
    await event.edit("Que triste ")
    await sleep(1)
    await event.edit(
        "╔══╗╔═╦═╗╔══╗╔╗─╔═╗\n║══╣║║║║║╚║║╝║║─║╦╝\n╠══║║║║║║╔║║╗║╚╗║╩╗\n╚══╝╚╩═╩╝╚══╝╚═╝╚═╝"
    )


@register(outgoing=True, pattern="^.lal$")
async def lal(event):
    await event.edit("╔╗─╔═╗╔╗─\n║╚╗║╬║║╚╗\n╚═╝╚═╝╚═╝")


# Author: @helloji123bot


@register(outgoing=True, pattern="^.tanimate (.*)")
async def tanimate(event):
    name = event.pattern_match.group(1)
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(189)
    animation_chars = [
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n??💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
        f"❤️🧡💛💚💙💜🖤\n {name} 💜💙💚\n❤️🧡💛💚💙💜🖤\n",
        f"🧡💛💚💙💜🖤❤️\n💙{name}💚💜\n🧡💛💚💙💜🖤❤️\n",
        f"💛💚💙💜🖤❤️🧡\n💜💚{name}💙\n💛💚💙💜🖤❤️🧡\n",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await event.edit(animation_chars[i % 189])


# Author: @The_Avengers_leader


@register(outgoing=True, pattern="^.call$")
async def call(event):
    if event.fwd_from:
        return
    animation_interval = 3
    animation_ttl = range(0, 18)
    await event.edit("Ligando...")
    animation_chars = [
        "`Conectando-se à sede do Telegram...`",
        "`Chamada conectada`",
        "`Telegram: Olá, aqui é o HQ do Telegram. Quem é?`",
        "`Eu: Ei, aqui é` @[Purple](t.me/Rewrite4),`Por favor, conecte-me ao meu irmão idiota 【ANDRIEL】,`",
        "`Autorizado pelo usuário`",
        "`Ligar para Pavel Durov`ʻAT +916969696969` ",
        "`Chamada privada conectada... `",
        "`Eu: Olá, senhor, bana esta conta do telegram` ",
        "`Pavel: Posso saber quem é este? `",
        "`Eu: Olá, sou eu ` @[Andrieeel](t.me/AndrielFR),",
        "`Pavel: Muito tempo sem te ver, irmão, eae...\nVou garantir que a conta do cara seja bloqueada em 24 horas.`",
        "`Eu: Obrigado, vejo você mais tarde bruh.`",
        "`Pavel: Por favor, não agradeça irmão, o Telegram é nosso. Apenas me ligue quando você estiver livre.`",
        "`Eu: Existe algum problema/emergência???`",
        "`Pavel: Sim, claro, há um bug no Telegram v69.6.9.\nEu não sou capaz de consertar isso. Se possível, Usome ajude a corrigir o bug.`",
        "`Eu: Envie-me o aplicativo na minha conta do Telegram, eu corrigirei o bug e enviarei para você.`",
        "`Pavel: Claro sir \nTC Bye Bye :)`",
        "`Chamada privada desconectada.`",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await event.edit(animation_chars[i % 18])


# Author: @HELLBOY_OP


@register(outgoing=True, pattern="^.tghack$")
async def tghack(event):
    if event.fwd_from:
        return
    animation_interval = 2
    animation_ttl = range(0, 16)
    animation_chars = [
        " Iniciando ataque com Bruteforce  ",
        " Checando status do MetaSploit/Hashcat  ",
        " Conectando MetaSploit! Começando ataque Bruteforce",
        "Hackeando... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Procurando Port aberta...`\n",
        "Hackeando... 12.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Local Port 36662 encontrada...`\n",
        "Hackeando... 23.63%\n[███░░░░░░░░░░░░░░░░░]\n`Obtendo informações da conta do usuário`\n",
        "Hackeando... 37.92%\n[█████░░░░░░░░░░░░░░░]\n`Iniciando Hashcat`\n",
        "Hackeando... 44.17%\n[███████░░░░░░░░░░░░░]\n`Tentativa 1/60 de descompilar a senha`\n",
        "Hackeando... 59.30%\n[█████████░░░░░░░░░░░]\n`Senha de Usuário[encriptada]:dej234hgfj12fgj45k6y73asdfgg21`\n",
        "Hackeando... 63.86%\n[███████████░░░░░░░░░]\n`Quebrando criptografia`\n",
        "Hackeando... 75.02%\n[█████████████░░░░░░░]\n`Quebrando criptografia`\n",
        "Hackeando... 83.21%\n[███████████████░░░░░]\n`Descriptografia concluída!!`\n",
        "Hackeando... 92.50%\n[█████████████████░░░]\n`Enviando dados de usuário para localhost`\n",
        "Hackeando... 100%\n[████████████████████]\n`Escaneando arquivos...`\n",
        "Hack concluído!\nEnviando dados de usuário para Server Port[36662]...",
        "Conta alvo hackeada...!\n\n ✅ Os dados foram enviados com sucesso para server Port[36662].\nFerramenta de acesso remoto disponível \n",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await event.edit(animation_chars[i % 16])


# Author: @Jisan7509


@register(outgoing=True, pattern="^.flower$")
async def flower(event):
    await event.edit(
        ".........▒▒▒▒▒▒▒▒▒\n      ▒▒▒▒▒▒▒▒▒▒▒▒\n  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒\n▒▒▒▒▒▓▓▓▓▓▓▓▒▒▒▒▒\n▒▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒\n▒▒▒▒▒▓▓▓▓▓▓▓▒▒▒▒▒\n  ▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒\n    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\n       ▒▒▒▒▒▒▒▒▒▒▒▒▒\n         ▒▒▒▒▒▒▒▒▒▒\n              ▒▒▒▒▒▒\n                     ▓\n     ▓▓▓       ▓\n ▓▓▓▓▓▓  ▓\n▓▓            ▓▓\n ▓                 ▓     ▓▓▓▓▓\n ▓                 ▓     ▓▓▓▓▓\n                     ▓   ▓▓▓▓▓▓\n                     ▓▓           ▓▓\n                     ▓               ▓\n                     ▓\n     ████████████\n         █████████\n            ███████\n             ██████\n.................███..............\n"
    )


@register(outgoing=True, pattern="^.vheart$")
async def vheart(event):
    await event.edit(
        "..........###########\n......##############\n....################\n..##################.............########\n...##################.......#############\n....##################.....##############\n.....#################...################\n.......#################################\n.........###############################\n...........#############################\n..............##########################\n................########################\n...................#####################\n.....................##################\n.......................###############\n........................#############\n..........................##########\n...........................########\n............................######\n.............................#####\n..............................###\n...............................#"
    )


@register(outgoing=True, pattern="^.luvart$")
async def luvart(event):
    await event.edit(
        " 📺📺📺📺📺📺📺📺📺📺📺📺📺\n 📺📺📺💖💖💖💖💖💖💖📺📺📺\n 📺📺📺📺📺💖💖💖📺📺📺📺📺\n 📺📺📺📺📺💖💖💖📺📺📺📺📺\n 📺📺📺📺📺💖💖💖📺📺📺📺📺\n 📺📺📺📺📺💖💖💖📺📺📺📺📺\n 📺📺📺💖💖💖💖💖💖💖📺📺📺\n 📺📺📺📺📺📺📺📺📺📺📺📺📺\n 💖💖💖💖💖💖💖💖💖💖💖💖💖\n 💖💖📺📺📺💖💖💖📺📺📺💖💖\n 💖📺📺📺📺📺💖📺📺📺📺📺💖\n 💖📺📺📺📺📺📺📺📺📺📺📺💖\n 💖💖📺📺📺📺📺📺📺📺📺💖💖\n 💖💖💖📺📺📺📺📺📺📺💖💖💖\n 💖💖💖💖📺📺📺📺📺💖💖💖💖\n 💖💖💖💖💖📺📺📺💖💖💖💖💖\n 💖💖💖💖💖💖📺💖💖💖💖💖💖\n 💖💖💖💖💖💖💖💖💖💖💖💖💖\n 📺📺📺📺📺📺📺📺📺📺📺📺📺\n 📺📺💖💖📺📺📺📺📺💖💖📺📺\n 📺📺💖💖📺📺📺📺📺💖💖📺📺\n 📺📺💖💖📺📺📺📺📺💖💖📺📺\n 📺📺💖💖📺📺📺📺📺💖💖📺📺\n 📺📺💖💖💖📺📺📺💖💖💖📺📺\n 📺📺💖💖💖💖💖💖💖💖💖📺📺\n 📺📺📺💖💖💖💖💖💖💖📺📺📺\n 📺📺📺📺📺📺📺📺📺📺📺📺📺\n"
    )


@register(outgoing=True, pattern="^.spika$")
async def kakashi(pikachu):
    await pikachu.edit(A)


@register(outgoing=True, pattern="^.sshit$")
async def kakashi(shit):
    await shit.edit(B)


@register(outgoing=True, pattern="^.sxx$")
async def kakashi(saxy):
    await saxy.edit(C)


@register(outgoing=True, pattern="^.sporn$")
async def kakashi(pornhub):
    await pornhub.edit(D)


@register(outgoing=True, pattern="^.sthink")
async def kakashi(think):
    await think.edit(E)


@register(outgoing=True, pattern="^.sdick")
async def kakashi(dick):
    await dick.edit(F)


@register(outgoing=True, pattern="^.sfrog")
async def kakashi(frog):
    await frog.edit(G)


@register(outgoing=True, pattern="^.sputin")
async def kakashi(putin):
    await putin.edit(H)


@register(outgoing=True, pattern="^.sdead")
async def kakashi(dead):
    await dead.edit(I)


@register(outgoing=True, pattern="^.strump")
async def kakashi(trump):
    await trump.edit(J)


@register(outgoing=True, pattern="^.schina")
async def kakashi(china):
    await china.edit(K)


@register(outgoing=True, pattern="^.india")
async def kakashi(india):
    await india.edit(L)


@register(outgoing=True, pattern="^.monster")
async def bluedevilmonster(monster):
    await monster.edit(N)


@register(outgoing=True, pattern="^.pig")
async def bluedevilpig(pig):
    await pig.edit(O)


@register(outgoing=True, pattern="^.killer")
async def bluedevilkiller(killer):
    await killer.edit(M)


@register(outgoing=True, pattern="^.gun")
async def bluedevilgun(gun):
    await gun.edit(P)


@register(outgoing=True, pattern="^.dog")
async def bluedevildog(dog):
    await dog.edit(Q)


@register(outgoing=True, pattern="^.hello")
async def bluedevilhello(hello):
    await hello.edit(R)


@register(outgoing=True, pattern="^.hmf")
async def bluedevilhmf(hmf):
    await hmf.edit(S)


@register(outgoing=True, pattern="^.couple")
async def bluedevilcouple(couple):
    await couple.edit(T)


@register(outgoing=True, pattern="^.sup")
async def bluedevilsupreme(supreme):
    await supreme.edit(U)


@register(outgoing=True, pattern="^.india2")
async def bluedevilindia(india2):
    await india2.edit(J)


@register(outgoing=True, pattern="^.wc")
async def bluedevilwelcome(welcome):
    await welcome.edit(W)


@register(outgoing=True, pattern="^.snk")
async def bluedevilsnake(snake):
    await snake.edit(X)


@register(outgoing=True, pattern="^.ded")
async def bluedevilded(ded):
    await ded.edit(L)


@register(outgoing=True, pattern="^.bye")
async def bluedevilbye(bye):
    await bye.edit(Y)


@register(outgoing=True, pattern="^.shitos")
async def bluedevilshitos(shitos):
    await shitos.edit(Z)


@register(outgoing=True, pattern="^.dislike")
async def bluedevildislike(dislike):
    await dislike.edit(AA)


CMD_HELP.update(
    {
        "memes": ".cowsay\
\nUso: vaca que diz coisas.\
\n\n:/\
\nUso: Veja você mesmo ;)\
\n\n-_-\
\nUso: Ok...\
\n\n;_;\
\nUso: Igual `-_-` só que chorando.\
\n\n.cp\
\nUso: Transforme um texto em copypasta\
\n\n.vapor\
\nUso: Vaporize tudo!\
\n\n.str\
\nUso: Estique tudo.\
\n\n.zal\
\nUso: Invoque o sentimento de caos.\
\n\nOof\
\nUso: Ooooof\
\n\n.moon\
\nUso: Animação de lua.\
\n\n.clock\
\nUso: Animação de relógio.\
\n\n.hi\
\nUso: Cumprimente a todos!\
\n\n.coinflip <heads/tails>\
\nUso: Jogue a moeda !!\
\n\n.owo\
\nUso: UwU\
\n\n.react\
\nUso: Faça seu userbot reagir a tudo.\
\n\n.slap\
\nUso: responda para bater neles com objetos aleatórios !!\
\n\n.cry\
\nUsoe: pq vc faz isso, eu choro.\
\n\n.shg\
\nUso: Dê de ombros !!\
\n\n.run\
\nUso: Deixe-me correr, correr, CORRER!\
\n\n.chase\
\nUso: É melhor você começar a correr!\
\n\n.metoo\
\nUso: Haha sim\
\n\n.mock\
\nUso: Faça e encontre a verdadeira diversão.\
\n\n.clap\
\nUso: Elogie as pessoas!\
\n\n.f <emoji/caractere>\
\nUso: Preste respeitos.\
\n\n.bt\
\nUso: Acredite em mim, você achará isso útil.\
\n\n.type\
\nUso: Só um pequeno comando para fazer seu teclado se tornar uma máquina de escrever!\
\n\n.lfy <consulta>\
\nUso: Deixe-me pesquisar isso no Google pra você bem rápido !!\
\n\n.decide [Alternativas: (.yes, .no, .maybe)]\
\nUso: Faz uma decisão rápida.\
\n\n.alone\
\nUso: Manda um texto 'triste'.\
\n\n.tanimate <nome>\
\nUso: Envia um nome em torno de vários corações\
\n\n.scam <ação> <tempo>\
\n[Ações disponíveis: (typing, contact, game, location, voice, round, video, photo, document, cancel)]\
\nUso: Crie ações de chat falsas para se divertir. (Ação padrão: typing)\
\n\nE muito mais\
\n.nou ; .bot ; .gey ; .gey ; .tf ; .paw ; .taco ; .nih ;\
\n.fag ; .gtfo ; .stfu ; .lol ; .lool ; .fail ; .earth ; .iwi\
\n.mst ; .gm ; .good ; .hhlo ; .sry ; .thnq ; .ok ; .smile\
\n.lal ; .call ; .tghack ; .flower ; .vheart ; .luvart ; .spika\
\n.sshit ; .sxx ; .sporn ; .sthink ; .sdick ; .sfrog ; .sputin\
\n.sdead ; .strump ; .schina ; .india ; .monster ; .killer\
\n.pig ; .gun ; .dog ; .hello ; .hmf ; .couple ; .india2\
\n.sup ; .wc ; .snk ; .ded ; .bye ; .shitos ; .dislike\
\n\n\nObrigada a 🅱️ottom🅱️ext🅱️ot (@NotAMemeBot) por alguns desses."
    }
)
