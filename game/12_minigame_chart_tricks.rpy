# === 12_minigame_chart_tricks.rpy (сгенерировано из script.rpy, модуль: chart_tricks) ===

screen chart_trick_zone_picker():
    button:
        xpos 582
        ypos 46
        xsize 756
        ysize 52
        background None
        action [Function(renpy.sound.play, "audio/star_click.mp3"), Return("title")]
        hover_background Solid("#ffe06633")

    button:
        xpos 430
        ypos 570
        xsize 1110
        ysize 35
        background None
        action [Function(renpy.sound.play, "audio/constellation_complete.mp3"), Return("xaxis")]
        hover_background Solid("#ffe06633")

    button:
        xpos 400
        ypos 160
        xsize 55
        ysize 415
        background None
        action [Function(renpy.sound.play, "audio/star_click.mp3"), Return("yaxis")]
        hover_background Solid("#ffe06633")


screen chart_trick_preset_picker(current):
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -40
        background Solid("#05161acc")
        padding (20, 14)

        hbox:
            spacing 14
            textbutton "3 месяца":
                action Return("3mo")
                text_color ("#ffe066" if current == "3mo" else "#5fd9c4")
                text_hover_color "#ffffff"
            textbutton "6 месяцев":
                action Return("6mo")
                text_color ("#ffe066" if current == "6mo" else "#5fd9c4")
                text_hover_color "#ffffff"
            textbutton "Год":
                action Return("12mo")
                text_color ("#ffe066" if current == "12mo" else "#5fd9c4")
                text_hover_color "#ffffff"
            textbutton "Готово, посмотрел достаточно":
                action Return("done")
                text_color "#ffffff"
                text_hover_color "#ff8888"


screen chart_trick_percent_picker():
    modal True
    zorder 200
    default pp_value = 0

    frame:
        background Solid("#05161acc")
        padding (30, 20)
        xalign 0.5
        yalign 1.0
        yoffset -40

        vbox:
            spacing 14
            text "На сколько процентов на самом деле изменился показатель за год?" color "#c8d4d4" size 20 font "fonts/Exo2-Regular.ttf"
            hbox:
                xalign 0.5
                spacing 10
                textbutton "−":
                    action SetScreenVariable("pp_value", pp_value - 5)
                    text_color "#5fd9c4"
                text "[pp_value]%" color "#ffe066" size 22 font "fonts/JetBrainsMono-Regular.ttf"
                textbutton "+":
                    action SetScreenVariable("pp_value", pp_value + 5)
                    text_color "#5fd9c4"
            textbutton "Готово":
                xalign 0.5
                action Return(pp_value)
                text_color "#5fd9c4"
                text_hover_color "#ffffff"


screen chart_trick_number_picker(question, start=0):
    modal True
    zorder 200
    default np_value = start

    frame:
        background Solid("#05161acc")
        padding (30, 20)
        xalign 0.5
        yalign 1.0
        yoffset -40

        vbox:
            spacing 14
            text question color "#c8d4d4" size 20 font "fonts/Exo2-Regular.ttf"
            hbox:
                xalign 0.5
                spacing 10
                textbutton "−":
                    action SetScreenVariable("np_value", np_value - 10)
                    text_color "#5fd9c4"
                text "[np_value]%" color "#ffe066" size 22 font "fonts/JetBrainsMono-Regular.ttf"
                textbutton "+":
                    action SetScreenVariable("np_value", np_value + 10)
                    text_color "#5fd9c4"
            textbutton "Готово":
                xalign 0.5
                action Return(np_value)
                text_color "#5fd9c4"
                text_hover_color "#ffffff"

# Экран рабочего стола с иконками

label sasha_chart_tricks_intro:
    player "Откуда я вообще понимаю, как читать диаграммы? Откуда я знаю, что такое диаграмма? Почему я в курсе, что надо смотреть на подписи осей? Как набор цветных пикселей рождает во мне вывод?"
    player "Не то чтобы я жаловался. После той истории с выручкой и нагрузкой я как будто не могу отключить эту привычку — присматриваться."
    sasha "Тогда у меня для тебя хорошая и плохая новость. Плохая: это никогда не отключается. Хорошая: у меня как раз завалялась целая коллекция любопытных графиков."
    sasha "Таких, которые обманут кого угодно, но не аналитика."
    sasha "Интересует?"
    player "В смысле, желаю ли я проверить, действительно ли работает этот мой внутренний анализатор? Это как-то поможет мне понять, откуда и зачем я это всё знаю?"
    sasha "Наверное, нет. Но это поможет тебе принять себя, приятель. Ты аналитик, и ты всегда будешь аналитиком — даже когда смотришь рекламу зубной пасты."
    player "Что ж, давай тогда примем себя. Неси рекламы всех зубных паст мира."
    sasha "Всех не принесу, но оцени вот это."

    jump chart_trick_demo


label chart_trick_demo:
    sasha "Мне сегодня подсунули кусок незамутнённого маркетинга."
    show image "images/chart_trick_toothpaste_ad.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    "Рекламный график сулит небывалую белизну зубов."
    player "Ну, выглядит грозно. Даже я хочу побежать за этой пастой, хотя я-то вообще не уверен, что у меня есть зубы."
    "Ты пытаешься провести по ним языком, но теперь не уверен, что у тебя есть язык."

    sasha "На такую реакцию всё и рассчитано. Смотри, я в таких случаях всегда проверяю три места. Первое это заголовок."
    show image "images/chart_trick_highlight_title.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05

    player "Заголовок кричащий, не поспоришь. Но кричать не преступление, тут нет явного обмана."
    sasha "Согласен, идём дальше. Второе место — подписи по оси Х."

    hide image "images/chart_trick_highlight_title.png"
    show image "images/chart_trick_highlight_xaxis.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05

    player "«До» и «После» — тоже ничего криминального, это просто две точки во времени."
    sasha "Значит, остаётся третье место."

    hide image "images/chart_trick_highlight_xaxis.png"
    show image "images/chart_trick_highlight_yaxis.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05

    player "Погоди-погоди, дай я сам... Так. Шкала. Она начинается с семи, а не с нуля! Вот он, фокус!"
    sasha "О! Ты меня опередил."
    player "Ну конечно, столбики кажутся очень разными по высоте, если начинать считать с семи. Если достаточно поиграться со шкалой, можно как угодно исказить пропорции, даже сделать столбец «После» втрое выше «До»."
    player "А потребитель не будет вглядываться в абсолютные значения, потребитель автоматически считает пропорции."

    hide image "images/chart_trick_highlight_yaxis.png"
    show image "images/chart_trick_toothpaste_honest.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    sasha "Что ж, я вернул начало шкалы к нулю и..."
    sasha "Вот они, настоящие цифры. Разница меньше балла из десяти — а изначально нарисовали так, будто зубы пережили духовное перерождение."
    player "Потрясающе."
    player "Знаешь что — дай мне в следующий раз самому покрутить эту шкалу. Хочу своими руками пощупать обман, а не просто смотреть, как ты его разоблачаешь."
    sasha "Идёт. Следующий график — целиком твой: и подвох ищешь сам, и шкалу сам возвращаешь на место."

    hide image "images/chart_trick_toothpaste_honest.png"

    jump chart_trick_round1


label chart_trick_round1:
    hide image "images/chart_trick_toothpaste_ad.png"
    hide image "images/chart_trick_toothpaste_honest.png"
    hide image "images/chart_trick_highlight_title.png"
    hide image "images/chart_trick_highlight_xaxis.png"
    hide image "images/chart_trick_highlight_yaxis.png"

    show image "images/chart_trick_sales_3mo.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05

    sasha "Смотри. Заголовок, ось X, ось Y — обман где-то среди них. Найди его."

    $ round1_attempts = 0
    jump chart_trick_round1_pick


label chart_trick_round1_pick:
    $ round1_zone = renpy.call_screen("chart_trick_zone_picker")

    if round1_zone == "title":
        $ round1_attempts += 1
        if round1_attempts >= 2:
            jump chart_trick_round1_giveup
        jump chart_trick_round1_title_branch
    elif round1_zone == "yaxis":
        $ round1_attempts += 1
        if round1_attempts >= 2:
            jump chart_trick_round1_giveup
        jump chart_trick_round1_yaxis_branch
    else:
        jump chart_trick_round1_correct


label chart_trick_round1_giveup:
    sasha "Так. Ну ты это не серьёзно. Знаешь что, я так не играю."
    player "Погоди, погоди, дай ещё..."
    sasha "Нет. У меня тоже есть достоинство, хоть я и состою из вероятностей. Ответ был в оси X — идём дальше, пока ты не обвинил в обмане меня самого."
    player "Было бы, кстати, неплохое дело — тебя обвинить."
    sasha "В другой раз. Пока — следующий график."

    hide image "images/chart_trick_sales_3mo.png"
    jump chart_trick_round2_intro


label chart_trick_round1_title_branch:
    sasha "Заголовок? Ладно, отстаивай позицию — с чем конкретно тут не так?"
    player "С тоном! Восклицательный знак — это уже статистически недостоверно."
    sasha "Один восклицательный знак, вообще-то. Ты его утроил сам, у себя в голове, пока читал."
    player "Ну неважно. Само слово «растут» уже манипулятивное. Могли бы написать «немного шевельнулись», это честнее."
    sasha "Это было бы честнее, но с таким заголовком ни один корпоративный отчёт в природе не публикуют. Ты сейчас критикуешь не статистику, а жанр корпоративной радости."
    player "Может, жанр корпоративной радости и есть главная статистическая проблема человечества."
    "Ты чувствуешь себя так, будто только что выдал нечто чрезвычайно мудрое."
    sasha "Смело. Не уверен, что готов оформить это как научный вывод, но звучит, будто у тебя накопилось к отчётам «Изобилия»."
    player "Накопилось. Ладно, отзываю жалобу на заголовок — по существу тут не подкопаешься."
    sasha "Значит, где-то в другом месте. Но раз уж мы это заявление официально закрыли без обвинительного приговора — идём дальше?"
    player "Идём. Настоящий виновник пусть погуляет на свободе недолго."
    sasha "Ладно, свежим взглядом — где ещё поищешь?"

    jump chart_trick_round1_pick


label chart_trick_round1_yaxis_branch:
    sasha "Ось Y? Ладно, покажи, в чём проблема."
    player "Она же не с нуля начинается! Ты сам меня этому научил пять минут назад!"
    sasha "Слушай, я ценю твоё доверие, но не превращай шкалу ординат в свою новую религию!"
    player "То есть, ты меня специально проверял? Вроде как, пойду ли я по уже проторенной дорожке?"
    sasha "Есть немного. И, кажется, поймал: ты сейчас обвиняешь шкалу не за то, что она врёт, а за то, что она просто выглядит так же, как та, что действительно врала."
    player "Ладно, это... справедливо неприятно слышать. Но если я не могу с одного взгляда отличить честную нестандартную шкалу от нечестной — как вообще жить дальше?"
    sasha "Смотреть не на факт нестандартности, а на то, искажает ли она реальные пропорции. Тут — не искажает. Так что можешь выдохнуть, шкала невиновна."
    player "Ладно, ладно. Беру своё обвинение назад. Публично. Перед этой самой осью."
    sasha "Трогательно. Значит, дело не в шкале — но раз уж мы официально её оправдали, идём дальше?"
    player "Идём. Настоящий виновник пусть погуляет на свободе недолго."
    sasha "Ладно, свежим взглядом — где ещё поищешь?"

    jump chart_trick_round1_pick


label chart_trick_round1_correct:
    sasha "Вот как — ты ставишь не на заголовок, а на временную ленту. В чём твоя идея?"
    player "Попытки играть на бирже в своё время научили меня двум вещам: никто не знает правой части графика и никто не знает, за какой период смотреть на левую."
    $ hero_trading_backstory_known = True
    player "То, что кажется ростом на горизонте трёх дней — незаметная флуктуация на фоне недели и так далее."
    player "Меня смущает, что здесь заголовок как бы намекает на нечто положительное, но мы не знаем, что было ДО."
    sasha "Поэтому ты хочешь развернуть график... Понимаю."
    sasha "Прежде чем сделать это — у тебя есть версия, что там было раньше?"

    menu:
        "Наверное, показатели были ещё выше, потом была яма, а сейчас — просто отскок от дна.":
            $ round1_guess = "higher"
        "Примерно так же — тренд как тренд, ничего особенного.":
            $ round1_guess = "same"
        "Понятия не имею. Надо смотреть, а не гадать.":
            $ round1_guess = "unknown"

    player "Давай покрутим ползунки."

    $ round1_preset = "3mo"
    $ round1_viewed = ["3mo"]
    jump chart_trick_round1_explore


label chart_trick_round1_explore:
    hide image "images/chart_trick_sales_3mo.png"
    hide image "images/chart_trick_sales_6mo.png"
    hide image "images/chart_trick_sales_12mo.png"

    if round1_preset == "3mo":
        show image "images/chart_trick_sales_3mo.png" at Transform(fit="contain", size=(1920, 700)):
            xalign 0.5
            yalign 0.05
    elif round1_preset == "6mo":
        show image "images/chart_trick_sales_6mo.png" at Transform(fit="contain", size=(1920, 700)):
            xalign 0.5
            yalign 0.05
    else:
        show image "images/chart_trick_sales_12mo.png" at Transform(fit="contain", size=(1920, 700)):
            xalign 0.5
            yalign 0.05

    $ round1_choice = renpy.call_screen("chart_trick_preset_picker", current=round1_preset)

    if round1_choice == "done":
        if len(round1_viewed) < 2:
            sasha "Погоди — ты же ещё ничего толком не раздвинул. Глянь хотя бы на один период подальше, прежде чем решать, что всё понял."
            jump chart_trick_round1_explore
        else:
            jump chart_trick_round1_reveal
    else:
        $ round1_preset = round1_choice
        if round1_choice not in round1_viewed:
            $ round1_viewed.append(round1_choice)
        jump chart_trick_round1_explore


label chart_trick_round1_reveal:
    if round1_guess == "higher":
        sasha "Ты был прав ещё до того, как посмотрел цифры. Признавайся: на бирже ты заработал миллионы."
        player "Ну, однажды я закрыл сделку с феноменальным +367%. Но это было 367% к двум тысячам. Немного не хватило для FIRE."
        $ intuition += 2
    elif round1_guess == "same":
        player "Хм. Не «тренд как тренд». Год назад было заметно выше — то, что выглядело ростом, на самом деле хвост падения."
        sasha "Первая гипотеза не всегда верная. Но ты хотя бы её сформулировал, прежде чем смотреть — это уже полдела."
        $ accuracy += 1
    else:
        player "Ну и правильно, что не гадал — было бы стыдно облажаться с прогнозом."
        sasha "Осторожность — тоже позиция. Но у аналитика в итоге должна быть версия — иначе зачем вообще смотреть на данные?"

    sasha "Смотри — год назад было 130, сейчас 98. Ты уже видел это своими глазами. Если бы тебе надо было одной цифрой описать, что произошло на самом деле — что бы ты сказал?"

    jump chart_trick_round1_percent_prompt


label chart_trick_round1_percent_prompt:
    $ round1_estimate = renpy.call_screen("chart_trick_percent_picker")

    if round1_estimate > 0:
        sasha "Погоди. Ты только что своими глазами видел, что сейчас показатель ниже прошлогоднего пика. Как он тогда может оказаться в плюсе? Число обязано быть отрицательным, раз падение ещё не отыграно."
        player "Действительно... не туда знак поставил."
        jump chart_trick_round1_percent_prompt

    $ round1_real_pct = -25
    $ round1_diff = abs(round1_estimate - round1_real_pct)

    if round1_diff <= 3:
        player "Падение примерно на четверть. Не рост, а всё ещё яма, из которой не вылезли."
        sasha "Совпадает с тем, что я вижу. А ведь в заголовке было слово «растут»."
        $ accuracy += 2
        $ intuition += 2
    else:
        player "Хм, погоди, дай пересчитаю..."
        sasha "Не страшно, прикидки почти никогда не бьются с реальностью с первого раза — в этом весь смысл проверки, а не доверия на глаз. На самом деле — около минус двадцати пяти процентов."
        $ accuracy += 1

    hide image "images/chart_trick_sales_3mo.png"
    hide image "images/chart_trick_sales_6mo.png"
    hide image "images/chart_trick_sales_12mo.png"

    player "Кажется, я понял главное правило: прежде чем доверять тренду, нужно спросить не «что показано», а «что было ДО того, как график начался»."
    sasha "Именно поэтому у финансовых графиков всегда есть кнопки «1Д / 1М / 1Г» — не для красоты, а потому что один и тот же участок кривой может значить прямо противоположные вещи в зависимости от того, откуда его вырезали."

    jump chart_trick_round2_intro


label chart_trick_round2_intro:
    sasha "Раз уж мы аналитики — обязан предупредить: сейчас будет круговая диаграмма."
    "Это было больно."
    player "О нет."
    sasha "Именно. Ты же знаешь, как аналитики относятся к круговым диаграммам."
    player "Как к криптовалюте, которую подарила бабушка на день рождения. Вроде подарок, но лучше бы деньгами. Бабуля и её любовь к MLM..."
    sasha "... У тебя особые отношения с собой бабулей. Моя версия: круговая диаграмма — это способ показать данные так, чтобы никто не смог на глаз сравнить, насколько один сектор реально больше другого. А эта — особенная, даже по меркам круговых диаграмм."

    show image "images/chart_trick_survey_pie.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05

    sasha "Опрос клиентов «Изобилия»: почему выбирают нас. Глазами — что-нибудь смущает?"

    menu:
        "Секторы выглядят примерно поровну, ничего критичного.":
            player "Да, на глаз всё чисто. Ни один сектор не выглядит подозрительно большим или маленьким."
        "Цвета слишком яркие, для отчёта аляповато.":
            player "Хотя нет, цвета — не статистика. Раздражает глаз, но к обману отношения не имеет."
        "Непривычная форма — обычно круговые рисуют иначе.":
            player "Хотя нет, форма стандартная. Просто цепляюсь к мелочам от безысходности."

    sasha "Вот именно — на глаз тут не за что зацепиться."
    player "Иногда обман не в форме, а в цифрах, которые с этой формой не дружат."
    player "Тогда остаётся одно — посчитать самому."

    jump chart_trick_round2_sum


label chart_trick_round2_sum:
    sasha "Ты меня заинтриговал."

    $ round2_sum = renpy.call_screen("chart_trick_number_picker", question="Сумма всех процентов на диаграмме:", start=102)
    $ round2_sum_diff = abs(round2_sum - 142)

    if round2_sum_diff <= 2:
        player "142. Это... не сто. Это далеко не сто."
        sasha "Действительно не сто. И при этом диаграмма выглядела абсолютно нормальной."
        $ accuracy += 2
        jump chart_trick_round2_mechanism
    else:
        player "Хм, дай пересчитаю ещё раз повнимательнее."
        sasha "Не спеши — сложи каждое число по отдельности, а не на глаз."
        jump chart_trick_round2_sum


label chart_trick_round2_mechanism:
    sasha "Так почему у нас сто сорок два процента вместо ста?"
    sasha "Вот, кстати, как это вообще собирали."
    sasha "Опрос шёл на кассах «Изобилия» весь март: покупателю показывали список из этих четырёх пунктов и просили отметить галочками все подходящие."
    sasha "Заполнили анкету около двух тысяч человек."

    menu:
        "Люди могли отмечать несколько вариантов сразу.":
            player "Логично — вопрос ведь не «выберите один», а «почему вы выбираете нас», да ещё и явно разрешили отмечать несколько галочек. Кто-то наверняка отметил сразу и «низкие цены», и «удобное расположение» — это совершенно нормальная реакция на такую анкету."
            sasha "Именно так это обычно и работает. Если из двух тысяч человек треть отметила по два пункта, а часть — даже по три, сумма процентов неизбежно уходит выше ста."
            player "Опрос был честным, а вот диаграмма — нет: она молча предположила, что каждый поставил ровно одну галочку."
            $ accuracy += 2

        "Где-то ошиблись при вводе данных.":
            player "Может, кто-то в таблице продублировал строку или перепутал цифры при выгрузке из двух тысяч анкет."
            sasha "Смотри внимательнее: ошибка ввода на паре анкет из двух тысяч дала бы сдвиг на десятые доли процента, не больше — и задела бы одну случайную категорию, а не все четыре разом."
            sasha "А тут проблема ровно того же порядка во всех категориях одновременно. Единичный сбой так не работает — он либо точечный, либо его сразу видно на фоне остальных чисел."
            player "То есть подозрительно не число, а сама системность перебора."
            sasha "Именно. Если ошибка размазана ровно по всем категориям — это не ошибка, это особенность вопроса."
            player "Значит, дело не в сбое, а в самом устройстве вопроса. Так... сколько галочек вообще разрешали ставить?"
            sasha "А ты подумай — сама формулировка допускала один ответ или сколько угодно?"
            player "Сколько угодно. Точно — значит, кто-то отмечал не один пункт, а сразу несколько, вот сумма и поехала выше ста."
            sasha "Опрос был честным. Диаграмма — нет: она молча предположила, что каждый поставил ровно одну галочку."

        "Это ошибка округления.":
            player "Может, каждую цифру из двух тысяч анкет немного округлили в большую сторону при подсчёте, вот и набежало."
            sasha "Округление на выборке в две тысячи человек даёт погрешность в районе одного процента на категорию, максимум пары — это доли процентного пункта на брата. У нас разрыв в сорок два процентных пункта. Округление даже теоретически не может столько объяснить."
            player "Тогда не округление. Но откуда систематический разрыв сразу по всем категориям?"
            sasha "Вспомни формулировку вопроса — сколько галочек можно было поставить?"
            player "Сколько угодно... Ну конечно. Люди отмечали не один пункт, а несколько — вот сумма и не сходится."
            sasha "Именно. Опрос был честным, диаграмма — нет."

    sasha "Раз уж это последний график за сегодня — как бы ты сам это исправил, чтобы было честно?"

    menu:
        "Показать как столбчатую диаграмму — каждый ответ сам по себе.":
            hide image "images/chart_trick_survey_pie.png"
            show image "images/chart_trick_survey_bar_honest.png" at Transform(fit="contain", size=(1920, 700)):
                xalign 0.5
                yalign 0.05
            with dissolve
            player "Вот так. Никто не притворяется, что это доли одного целого — каждый процент сам по себе."
            sasha "Скучнее для презентации. Зато не приходится потом краснеть, когда кто-то сложит цифры в столбик."
            $ accuracy += 2
            $ intuition += 1

        "Пропорционально уменьшить каждую цифру, чтобы сумма стала ровно 100%%.":
            player "Пересчитаем: возьмём долю каждого варианта от общей суммы — и получим что-то вроде 30%, 27%, 25%, 19%. Сумма ровно сто."
            sasha "Арифметически сходится. Только смысл  умер. Ты только что сделал вид, будто ни один человек не отмечал два варианта сразу — а на самом деле почти половина отмечала. Красивая сумма ценой выдуманных чисел."
            player "То есть я не исправил обман, а просто сделал его аккуратнее."
            sasha "Именно. Обман с ровными краями всё равно обман."

        "Просто переименовать диаграмму, не трогая цифры.":
            player "Назовём её как-то вроде «упоминания в ответах», без слова «доли»."
            sasha "Честнее по названию, но график всё ещё выглядит как обычная круговая диаграмма — а её форма сама по себе обещает зрителю «сумма равна ста». Название не отменяет визуальное обещание формы."

    hide image "images/chart_trick_survey_pie.png"
    hide image "images/chart_trick_survey_bar_honest.png"

    sasha "Что ж. Три графика, три способа соврать — не считая заголовков, которые тоже иногда просто корпоративно ликуют, без злого умысла."
    player "Кажется, я теперь буду с подозрением смотреть на каждую диаграмму до конца жизни."
    sasha "Это, между прочим, профессиональная деформация в хорошем смысле. Поздравляю с приобретением."

    $ unlock_achievement("stoprocentny_skeptik")
    $ news_list.extend([
        "«Изобилие» отозвала внутренний отчёт по итогам опроса клиентов после того, как кто-то в бухгалтерии наконец решил проверить, сходится ли сумма процентов."
    ])
    $ unread_news = True
    $ graph_trick_done = True

    jump chat_with_sasha_menu


