# === 11_minigame_crypto.rpy (сгенерировано из script.rpy, модуль: crypto) ===

init python:
    CRYPTO_ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    def caesar_decode(ciphertext, shift):
        out = []
        for ch in ciphertext:
            i = CRYPTO_ALPHABET.find(ch)
            if i == -1:
                out.append(ch)
            else:
                out.append(CRYPTO_ALPHABET[(i - shift) % 32])
        return "".join(out)

    def crypto_top_letter(text):
        counts = {}
        for ch in text:
            if ch in CRYPTO_ALPHABET:
                counts[ch] = counts.get(ch, 0) + 1
        return max(counts, key=counts.get) if counts else ""


screen crypto_shift_picker(ciphertext, hint=""):
    modal True
    zorder 200
    default cp_shift = 0

    if hint:
        text hint size 26 color "#ffaa00" xalign 0.5 ypos 55 xmaximum 1500 at sig_fade_in(0.5, 1.0)

    frame:
        background Solid("#05161a")
        padding (30, 26)
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 18

            frame:
                background Solid("#0a2224")
                padding (16, 14)
                text "[ciphertext]" size 22 color "#ffe066" font "fonts/JetBrainsMono-Regular.ttf"

            hbox:
                xalign 0.5
                spacing 10
                text "Сдвиг:" color "#c8d4d4" size 20 font "fonts/Exo2-Regular.ttf"
                textbutton "−":
                    action SetScreenVariable("cp_shift", (cp_shift - 1) % 32)
                    text_color "#5fd9c4"
                text "[cp_shift]" color "#ffe066" size 20 font "fonts/JetBrainsMono-Regular.ttf"
                textbutton "+":
                    action SetScreenVariable("cp_shift", (cp_shift + 1) % 32)
                    text_color "#5fd9c4"

            textbutton "Попробовать":
                xalign 0.5
                action [Function(renpy.sound.play, "audio/star_click.mp3"), Return(cp_shift)]
                text_color "#5fd9c4"
                text_hover_color "#ffffff"


define crypto_practice2_pool = [
    {"cipher": "ЪЩЬЭЛНХУ ШЛ ЭЩВХЮ П ЪЫУАЩПКЭ ЭЩЦЗХЩ ЪЩ ЬЫРПЛЧ ЪЩЬЦР ЪЩЦЮШЩВУ", "shift": 11},
    {"cipher": "ДАДБД ИДНАЮ Ъ ЕДЗИДХГГД ЛДЪХИ ЕДЗИДЖДГГЮЫ ГД ДЛЖЦГЦ ЕДНЫВЙ ИД ЮЛ ГЫ ИЖДЩЦЫИ", "shift": 22},
    {"cipher": "УПУРУ ЧУЬПН Й УЪХЕТЕ УЧПРГЬЕКЧ ЗЦК ПЕСКХА ФУЦРК ФУРШТУЬН Н ТНПЧУ ФУЧУС ТК ЪУЬКЧ УЖ ВЧУС ИУЗУХНЧБ", "shift": 5}
]


label sasha_crypto_intro:
    player "Может, поэтому в разговоре с Начальником что-то щёлкнуло в моём мозгу от упоминания шифра Цезаря."
    player "Хотя с моей амнезией... я будто уже сам не помню, в чём там суть."
    player "Ты знаком с ним?"
    sasha "Конечно! Хочешь, помогу тебе всё вспомнить?"
    sasha "Смотри, это на самом деле совсем простая штука — возможно, даже обидно простая для того, кто в детстве уже щёлкал шифры как орешки. Шифр Цезаря: берёшь алфавит, и каждую букву сообщения заменяешь на другую, которая стоит на фиксированное число позиций дальше. Захочешь зашифровать «А» со сдвигом три — получишь «Г». И так каждую букву, одинаково."
    sasha "Хочешь, покажу на паре букв, чтобы было видно глазами, а не только на словах?"
    player "Конечно, визуально всегда проще отследить."
    sasha "Вот, смотри."

    show image "images/caesar_explainer.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    sasha "Видишь? Каждая буква просто съезжает по алфавиту на одно и то же число мест. Хоть на три, хоть на двадцать шесть — принцип не меняется, меняется только это одно число. Вот это число и называют ключом."
    sasha "И если ты знаешь ключ — расшифровка занимает секунды. Знаешь сдвиг — просто едешь по алфавиту в обратную сторону на столько же позиций, и всё встаёт на место."
    sasha "Кстати, у меня как раз завалялось зашифрованное сообщение — то самое, из трафика точки Д. Хочешь, дам тебе и сообщение, и ключ, чтобы ты сам увидел, как это работает на практике?"

    hide image "images/caesar_explainer.png"
    with dissolve

    player "То-очно! Саша, а давай как с друзьями в детстве: изобретем свой тайный язык или хотя бы шифром обсудим девчонок."
    sasha "Девчонок? У меня, если ты не забыл, нет ни тела, ни детства, ни девчонок, которых можно было бы обсуждать шифром на задней парте. Так что предлагаю компромисс: обсудим точку Д. Тоже своего рода предмет обожания, если посмотреть под нужным углом — во всяком случае, Начальника явно."
    sasha "Ладно, вот тебе настоящее зашифрованное сообщение — то самое, из трафика точки Д. И вот ключ: сдвиг — три. Ровно тот самый исторический сдвиг, кстати, тот же, что был у оригинального Цезаря."
    sasha "Введи сдвиг, посмотри, что получится. Обещаю, это будет куда интереснее девчонок."

    $ crypto_demo_cipher = "ХСЪНГ З ГНХЛЕЛУЦИХФВ ХСОЯНС ТС ФУИЗГП ТСФОИ ТСОЦРСЪЛ, Л РЛНХС ЛК СШУГРЮ РИ КРГИХ ТСЪИПЦ"
    $ crypto_demo_tries = 0
    jump crypto_demo_try


label crypto_demo_try:
    $ crypto_demo_shift = renpy.call_screen("crypto_shift_picker", ciphertext=crypto_demo_cipher, hint="ЛКМ по - и + чтобы менять сдвиг")
    "Пробуешь разложить сообщение по сдвигу [crypto_demo_shift]..."
    pause 1.2
    $ crypto_demo_result = caesar_decode(crypto_demo_cipher, crypto_demo_shift)
    "[crypto_demo_result]"
    if crypto_demo_shift != 3:
        $ crypto_demo_tries += 1
        if crypto_demo_tries < 3:
            sasha "Ты чего? Я же прямо сказал, что ключ — три. Попробуй ещё раз."
            jump crypto_demo_try
        else:
            $ crypto_demo_result = caesar_decode(crypto_demo_cipher, 3)
            sasha "Давай покажу, как это выглядит. Ключ — три."
            "[crypto_demo_result]"


    player "Саша, ты вот правда считаешь, что вот это — интереснее девчонок? Ну у вас, ИИи, и жизнь..."
    sasha "Обидно слышать «ИИи» во множественном числе, будто нас тут целая компания и мы вместе решили быть скучными. Но ладно, проехали."
    sasha "А если серьёзно — раз уж ты только что увидел, как ключ решает всё за секунду, у меня встречный вопрос на будущее: а что, если бы ключа не было? Стал бы ты вообще пытаться, или сразу сдался?"
    player "Я? Сдаться? Давай-ка я попробую без ключа. Напрягу свою аналитическую мышцу и расшифрую строчку и так!"
    sasha "О, вот это уже интереснее девчонок. Аналитическая мышца против случайного числа от нуля до тридцати одного — заманчивая дуэль, признаю."
    sasha "Даю тебе новое сообщение, тоже про точку Д, но на этот раз без ключа. Три попытки — крутишь сдвиг, смотришь, получилось ли что-то похожее на настоящие слова. Если не выйдет — не расстраивайся, это, в общем-то, ожидаемо."
    sasha "Погнали. Вот шифротекст."

    $ crypto_p1_cipher = "ДЮШЧЖСМУТ ВБДЕУХЭУ АУ ЕБКЭЖ Ч ЪУЧШГЩЫЕДТ, ВБЕБЯЖ КЕБ ХБЧЫЕШЮП БЕЭУЪУЮДТ ШИУЕП ЕЖЧУ Х БЧЫАБКЭЖ"
    $ crypto_p1_shift_correct = 19
    $ crypto_p1_attempts = 3
    $ crypto_p1_solved = False
    jump crypto_p1_attempt


label crypto_p1_attempt:
    $ crypto_p1_shift = renpy.call_screen("crypto_shift_picker", ciphertext=crypto_p1_cipher, hint="ну, подбери, как знаешь")
    "Пробуешь разложить сообщение по сдвигу [crypto_p1_shift]..."
    pause 1.2
    $ crypto_p1_result = caesar_decode(crypto_p1_cipher, crypto_p1_shift)
    "[crypto_p1_result]"
    if crypto_p1_shift == crypto_p1_shift_correct:
        $ renpy.sound.play("audio/constellation_complete.mp3")
        $ crypto_p1_solved = True
        $ accuracy += 3
        $ intuition += 3
        jump crypto_p1_after
    else:
        $ crypto_p1_attempts -= 1
        if crypto_p1_attempts > 0:
            sasha "Не читается. Есть ещё попытки — не сдавайся так быстро."
            jump crypto_p1_attempt
        else:
            jump crypto_p1_after


label crypto_p1_after:
    if crypto_p1_solved:
        sasha "Ничего себе, как ты это сделал???"
        player "А вот и не скажу так сразу. Давай лучше ты соберёшь для меня инфу о самых частых буквах в русскоязычных текстах."
    else:
        player "... погоди. Что-то явно не так в моей гениальной логике."
        player "Так-так-так."
        player "..."
        player "Но я же аналитик, в конце концов!"
        sasha "...Погоди. Ты сейчас три раза подряд покрутил число наугад — и в перерывах между попытками успел пережить экзистенциальный кризис длиной в четыре реплики?"
        player "О, Саша, а ты можешь собрать для меня инфу, как часто в русскоязычных текстах встречается та или иная буква? И какая буква самая частотная?"

    sasha "Секунду, собираю... Готово."

    show image "images/crypto_letter_frequency_ref.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    sasha "Если верить моим источникам, чаще всего в русских текстах встречается буква «О» — с большим отрывом от всех остальных. Дальше идут «Е», «А», «И», «Н» — но у них разрыв уже не такой драматичный."
    sasha "Если говорить точнее — «О» здесь то, что статистики называют модой распределения. Не в смысле «модно», а в смысле «самое часто встречающееся значение». В любом достаточно длинном русском тексте мода почти всегда одна и та же — «О»."
    player "То есть частота — это просто «как часто буква встречается», а мода — это «какая буква встречается чаще всех»? Я ничего не путаю?"
    sasha "Именно."
    sasha "Только я всё ещё не понимаю, зачем тебе это. Ты серьёзно собираешься побеждать шифр статистикой, а не логикой?"
    player "Готовься, Саша, сейчас я покажу тебе магию! Картинку можешь убирать, я запомнил."

    hide image "images/crypto_letter_frequency_ref.png" with dissolve

    player "Если мы найдём, какая буква чаще всего встречается в зашифрованном предложении, мы сможем предположить, что эта буква заменяет самую популярную букву языка. Логично ведь?"
    player "Например, в шифре чаще всего встречается Е, а в языке — О. Значит, Е это с высокой степенью вероятности О. А через разницу между номерами Е и О в алфавите и можно найти число сдвига!"
    player "Теперь будет моя картинка для наглядности."

    show image "images/crypto_shift_logic_v2.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    sasha "..."
    sasha "Ладно, это она. Настоящая магия. Не в смысле «необъяснимое», а в смысле «объяснимое, но от этого не менее крутое»."
    sasha "Честно говоря, мне немного стыдно. Я тут сижу с доступом ко всей статистике русского языка, а додумался применить её именно так ты сам, а не я."

    hide image "images/crypto_shift_logic_v2.png"

    sasha "Ну что, аналитик, раз уж ты изобрёл метод — обкатаем его на деле? Только один нюанс, прежде чем начнём."

    show image "images/crypto_length_matters.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    sasha "Этот метод надёжен только на достаточно длинных текстах — на паре слов частоты ещё ничего не значат, слишком много случайности. Хорошо, что у нас полноценные фразы, а не обрывки."

    hide image "images/crypto_length_matters.png"

    sasha "Даю тебе новое сообщение из трафика точки Д. На этот раз не гадаешь вслепую, а ищешь самую частую букву в шифре и предполагаешь, что это «О». Как и в прошлый раз — три попытки, потом сообщение меняется, чтобы ты не мог случайно перебором наткнуться на ответ."

    $ crypto_p2_fails = 0
    $ crypto_p2_pool_index = 0
    $ crypto_p2_attempts = 3
    jump crypto_p2_new_message


label crypto_p2_new_message:
    $ crypto_p2_current = crypto_practice2_pool[crypto_p2_pool_index % len(crypto_practice2_pool)]
    $ crypto_p2_cipher = crypto_p2_current["cipher"]
    $ crypto_p2_shift_correct = crypto_p2_current["shift"]
    $ crypto_p2_attempts = 3
    $ crypto_p2_top = crypto_top_letter(crypto_p2_cipher)
    if crypto_p2_fails >= 2:
        sasha "Подскажу: в этом сообщении чаще всего встречается «[crypto_p2_top]». Если это «О», на сколько позиций она сдвинута?"
    jump crypto_p2_attempt


label crypto_p2_attempt:
    $ crypto_p2_shift = renpy.call_screen("crypto_shift_picker", ciphertext=crypto_p2_cipher, hint="Вычти номера букв, чтобы найти сдвиг (самая частотная - О)")
    "Пробуешь разложить сообщение по сдвигу [crypto_p2_shift]..."
    pause 1.2
    $ crypto_p2_result = caesar_decode(crypto_p2_cipher, crypto_p2_shift)
    "[crypto_p2_result]"
    if crypto_p2_shift == crypto_p2_shift_correct:
        $ renpy.sound.play("audio/constellation_complete.mp3")
        jump crypto_p2_success
    else:
        $ crypto_p2_attempts -= 1
        if crypto_p2_attempts > 0:
            sasha "Не читается. Присмотрись к буквам ещё раз — попытки ещё остались."
            jump crypto_p2_attempt
        else:
            $ crypto_p2_fails += 1
            if crypto_p2_fails >= 3:
                jump crypto_p2_giveup
            sasha "Не в этот раз. Меняю сообщение — иногда полезно начать с чистого листа."
            $ crypto_p2_pool_index += 1
            jump crypto_p2_new_message


label crypto_p2_giveup:
    $ crypto_p2_result = caesar_decode(crypto_p2_cipher, crypto_p2_shift_correct)
    sasha "Давай я. Здесь чаще всего встречается «[crypto_p2_top]», значит, это «О», и сдвиг [crypto_p2_shift_correct]."
    "[crypto_p2_result]"
    sasha "Метод рабочий, просто его надо довести до конца. В следующий раз получится."
    $ crypto_done = True
    jump chat_with_sasha_menu


label crypto_p2_success:
    sasha "Читается! Ты только что взломал шифр статистикой!"

    player "Погоди, Саша. У меня сейчас будто что-то щёлкнуло не только про шифр."
    player "Я вот сижу, считаю буквы, ищу закономерность — и это ощущение мне откуда-то знакомое."
    player "Не помню деталей. Амнезия, будь она неладна. Но осталось чувство: я всегда любил, когда за хаосом обнаруживается порядок. Цифры, закономерности, шифры — ещё до всего этого, до данных, до Начальника, до тебя."
    player "Может, поэтому я и стал аналитиком. Это всегда было про взлом кода реальности что ли."
    sasha "Поэтично. Но я всегда рад тебя послушать."

    $ unlock_memory("shifr_pod_partoy")
    $ unlock_achievement("vzlomshik_po_mode")
    $ news_list.extend(["Эксперты по кибербезопасности отмечают всплеск интереса к классическим шифрам среди школьников — трендом это назвали 'внезапно' и 'необъяснимо', хотя объяснение обычно простое: скука на летних каникулах."])
    $ unread_news = True
    $ crypto_done = True

    jump chat_with_sasha_menu
