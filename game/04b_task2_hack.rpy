# === 04b_task2_hack.rpy — сцена «тихий взлом журнала» (Задание 2) ===

define sasha_q = Character("[sasha_name!l]?",
    color="#8ff0dc",
    what_color="#8ff0dc",
    what_italic=True,
    what_slow_cps=22
)

define HACK_FONT = "fonts/JetBrainsMono-Regular.ttf"

define HACK_ROWS = [
    ("ревизия_кабачковой_полки", "вт", 12),
    ("перерасчёт_бонусов_за_улыбку", "пт", 3),
    ("кот_на_клавиатуре", "пн", 2),
    ("кот_на_клавиатуре", "вт", 1),
    ("кот_на_клавиатуре", "ср", 2),
    ("кот_на_клавиатуре", "чт", 1),
    ("кот_на_клавиатуре", "пт", 2),
    ("кот_на_клавиатуре", "сб", 1),
    ("визит_ревизора", "чт", 1),
]
define HACK_TOTALS = [
    ("ревизия_кабачковой_полки", 12),
    ("перерасчёт_бонусов_за_улыбку", 3),
    ("кот_на_клавиатуре", 9),
    ("визит_ревизора", 1),
]
define HACK_BYWD = [("пн", 2), ("вт", 13), ("ср", 2), ("чт", 2), ("пт", 5), ("сб", 1)]
define HACK_DUMP = [
    (1, "вт", "ревизия_кабачковой_полки"),
    (1, "ср", "кот_на_клавиатуре"),
    (2, "вт", "ревизия_кабачковой_полки"),
    (2, "пт", "перерасчёт_бонусов_за_улыбку"),
    (2, "пн", "кот_на_клавиатуре"),
    ("...", "ещё 19 строк", ""),
]
define HACK_DENS = [
    ("w", "охват журнала: 12 недель", 12),
    ("a", "всего записей: 25", 25),
    ("e", "событий в журнале: 4", 4),
]
define HACK_SELS = [
    ("star", "*"),
    ("ev", "event, COUNT(*)"),
    ("wd", "weekday, COUNT(*)"),
    ("evwd", "event, weekday, COUNT(*)"),
]
define HACK_GRPS = [
    ("none", "без группировки"),
    ("ev", "event"),
    ("wd", "weekday"),
    ("evwd", "event, weekday"),
]
define HACK_SEL_SQL = {"star": "*", "ev": "event, COUNT(*)", "wd": "weekday, COUNT(*)", "evwd": "event, weekday, COUNT(*)"}
define HACK_GRP_SQL = {"none": "", "ev": "\nGROUP BY event", "wd": "\nGROUP BY weekday", "evwd": "\nGROUP BY event, weekday"}

define HACK_MAX_POINTS = 8
define HACK_MIN_POINTS = 1
define HACK_ALARM_PENALTY = 2
define HACK_REPLAY_INTRO = False

default task2_sql_level = 0
default hack_mistakes = 0
default hack_alarms = 0
default hack_alarm = False
default hack_phase = "A"
default hack_noise = 10
default hack_sel = "star"
default hack_grp = "none"
default hack_result = None
default hack_row = None
default hack_den = None
default hack_frac = None
default hack_msg_sasha = ""
default hack_msg_hero = ""
default hack_boss = ""
default task2_secret_access = False


init python:

    def hack_start():
        store.hack_mistakes = 0
        store.hack_alarms = 0
        store.hack_alarm = False
        hack_reset()

    def hack_reset():
        store.hack_phase = "A"
        store.hack_noise = 10
        store.hack_sel = "star"
        store.hack_grp = "none"
        store.hack_result = None
        store.hack_row = None
        store.hack_den = None
        store.hack_frac = None
        store.hack_msg_sasha = "тихо. запрашивай только то, что нужно."
        store.hack_msg_hero = "Журнал открыт. Как понять, повторяется ли что-то регулярно? Для начала посмотрю, как события ложатся на дни недели."
        store.hack_boss = ""

    def hack_bump(n):
        store.hack_mistakes += 1
        store.hack_noise += n
        if store.hack_noise >= 100:
            store.hack_noise = 100
            store.hack_alarm = True

    def hack_den_value():
        for k, label, val in HACK_DENS:
            if k == store.hack_den:
                return val
        return None

    def hack_run():
        sel = store.hack_sel
        grp = store.hack_grp
        need = {"ev": "ev", "wd": "wd", "evwd": "evwd"}
        if sel == "star":
            store.hack_result = "dump"
            store.hack_msg_sasha = "громко. читай не всё, читай нужное."
            store.hack_msg_hero = "Полный дамп остаётся в журнале доступа. Так не пойдёт."
            hack_bump(40)
        elif grp != need[sel]:
            store.hack_result = "err"
            store.hack_msg_sasha = "что показываешь, то и группируй."
            store.hack_msg_hero = "Синтаксис. Вот почему я не пишу запросы ночью."
            hack_bump(5)
        elif sel == "ev":
            store.hack_result = "tot"
            store.hack_msg_sasha = "сколько всего, но не когда."
            store.hack_msg_hero = "Двенадцать, девять, три, один. Частота ещё не ритм."
            hack_bump(8)
        elif sel == "wd":
            store.hack_result = "bywd"
            store.hack_msg_sasha = "тут всё слиплось."
            store.hack_msg_hero = "Вторник лидирует, но события перемешаны. Какие из них вообще вторничные?"
            hack_bump(8)
        else:
            store.hack_phase = "B"
            store.hack_result = None
            store.hack_msg_sasha = "хорошо. теперь думай."
            store.hack_msg_hero = "Так. И какие из этих товарищей выглядят так, будто происходят раз в неделю?"

    def hack_check():
        row = HACK_ROWS[store.hack_row]
        key = store.hack_den
        den = hack_den_value()
        n = row[2]
        v = n / float(den)
        vs = ("%g" % round(v, 2)).replace(".", ",")
        if row[0] == "ревизия_кабачковой_полки" and key == "w":
            store.hack_frac = (n, den, vs)
            store.hack_phase = "done"
            store.hack_msg_sasha = "вот. запомни, не говори никому."
            store.hack_msg_hero = "Раз в неделю, ровно 12 из 12, и всегда по вторникам. Если пики на графике тоже во вторник, я прав. Если нет, гипотеза мертва. И начальнику знать об этом незачем."
        else:
            if key == "a":
                msg = "Это доля от всех записей, а не частота по неделям."
            elif key == "e":
                msg = "Событий четыре, недель двенадцать. Делить на события бессмысленно."
            else:
                msg = vs + " события в неделю. Раз в неделю должно быть 1."
            store.hack_msg_sasha = "не то."
            store.hack_msg_hero = msg
            store.hack_frac = None
            store.hack_row = None
            store.hack_den = None
            hack_bump(10)

    def hack_step(action):
        store.hack_boss = ""
        if action == "end":
            return "end"
        if action == "run":
            hack_run()
        elif action == "check":
            if store.hack_row is not None and store.hack_den is not None:
                hack_check()
        if store.hack_alarm:
            store.hack_alarm = False
            return "alarm"
        return ""


screen hack_cell(value, w, sz=20, col="#cfe9e3", h=30):
    fixed:
        xsize w
        ysize h
        text str(value) font HACK_FONT size sz color col


screen hack_table(head, rows, widths, x, y):
    vbox:
        pos (x, y)
        spacing 4
        hbox:
            for i, h in enumerate(head):
                use hack_cell(h, widths[i], 18, "#6f8a99", 26)
        for r in rows:
            hbox:
                for i, c in enumerate(r):
                    use hack_cell(c, widths[i], 20, "#cfe9e3", 30)


screen hack_alarm():
    zorder 40
    add Solid("#e5534b66")
    text "ШУМ: 100\nДОСТУП ЗАБЛОКИРОВАН" align (0.5, 0.5) font HACK_FONT size 54 color "#ffffff" text_align 0.5


screen hack_terminal():
    modal True
    zorder 30

    $ nz = min(hack_noise, 100)
    $ nz_col = "#e5534b" if nz >= 85 else ("#e0a030" if nz >= 60 else "#4fc9b0")

    fixed:
        pos (210, 30)
        xysize (1500, 690)

        add Solid("#0b1018f2")

        text "доступ: events_log" pos (28, 18) font HACK_FONT size 20 color "#6f8a99"
        text "шум" pos (1130, 18) font HACK_FONT size 18 color "#6f8a99"
        add Solid("#1b2535") pos (1200, 26) xysize (220, 12)
        add Solid(nz_col) pos (1200, 26) xysize (max(2, int(nz * 2.2)), 12)
        text str(nz) pos (1432, 18) font HACK_FONT size 18 color "#cfe9e3"

        if hack_msg_sasha:
            text ("[sasha_name!l]?: " + hack_msg_sasha) pos (28, 66) xsize 1440 font HACK_FONT size 20 italic True color "#8ff0dc"
        if hack_msg_hero:
            text hack_msg_hero pos (28, 106) xsize 1440 font HACK_FONT size 20 color "#ffffff"

        if hack_phase == "A":

            text "SELECT" pos (28, 250) font HACK_FONT size 18 color "#6f8a99"
            grid 2 2:
                pos (28, 276)
                spacing 8
                for key, label in HACK_SELS:
                    button:
                        xsize 310
                        ysize 40
                        background Solid("#12303a" if hack_sel == key else "#14202e")
                        hover_background Solid("#1b3040")
                        action SetVariable("hack_sel", key)
                        text label font HACK_FONT size 18 color ("#8ff0dc" if hack_sel == key else "#cfe9e3") align (0.5, 0.5)

            text "GROUP BY" pos (28, 378) font HACK_FONT size 18 color "#6f8a99"
            grid 2 2:
                pos (28, 404)
                spacing 8
                for key, label in HACK_GRPS:
                    button:
                        xsize 310
                        ysize 40
                        background Solid("#12303a" if hack_grp == key else "#14202e")
                        hover_background Solid("#1b3040")
                        action SetVariable("hack_grp", key)
                        text label font HACK_FONT size 18 color ("#8ff0dc" if hack_grp == key else "#cfe9e3") align (0.5, 0.5)

            frame:
                pos (28, 510)
                xsize 628
                ysize 96
                padding (14, 10)
                background Solid("#101826")
                text ("SELECT " + HACK_SEL_SQL[hack_sel] + "\nFROM events_log" + HACK_GRP_SQL[hack_grp] + ";") font HACK_FONT size 18 color "#cfe9e3"

            button:
                pos (28, 622)
                xysize (200, 44)
                background Solid("#12303a")
                hover_background Solid("#1b3040")
                action Return("run")
                text "выполнить" font HACK_FONT size 20 color "#8ff0dc" align (0.5, 0.5)

            if hack_result == "dump":
                use hack_table(["week", "weekday", "event"], HACK_DUMP, [110, 170, 480], 700, 250)
            elif hack_result == "err":
                text "ошибка: SELECT и GROUP BY не совпадают" pos (700, 250) font HACK_FONT size 20 color "#e5534b"
            elif hack_result == "tot":
                use hack_table(["event", "COUNT(*)"], HACK_TOTALS, [480, 150], 700, 250)
            elif hack_result == "bywd":
                use hack_table(["weekday", "COUNT(*)"], HACK_BYWD, [200, 150], 700, 250)

        else:

            $ dval = hack_den_value()
            if hack_row is not None:
                $ f_n = str(HACK_ROWS[hack_row][2])
            else:
                $ f_n = "?"
            if dval is not None:
                $ f_d = str(dval)
            else:
                $ f_d = "?"
            if hack_phase == "done" and hack_frac:
                $ f_eq = "= " + hack_frac[2]
            else:
                $ f_eq = ""

            vbox:
                pos (28, 250)
                spacing 2
                hbox:
                    use hack_cell("event", 380, 18, "#6f8a99", 26)
                    use hack_cell("weekday", 120, 18, "#6f8a99", 26)
                    use hack_cell("COUNT(*)", 120, 18, "#6f8a99", 26)
                for i, r in enumerate(HACK_ROWS):
                    button:
                        xsize 650
                        ysize 36
                        background Solid("#12303a" if hack_row == i else "#0b1018")
                        hover_background Solid("#12202e")
                        sensitive hack_phase == "B"
                        action SetVariable("hack_row", i)
                        hbox:
                            xoffset 8
                            yalign 0.5
                            use hack_cell(r[0], 380, 18, ("#8ff0dc" if hack_row == i else "#cfe9e3"), 26)
                            use hack_cell(r[1], 120, 18, ("#8ff0dc" if hack_row == i else "#cfe9e3"), 26)
                            use hack_cell(r[2], 120, 18, ("#8ff0dc" if hack_row == i else "#cfe9e3"), 26)

            text "делим: что на что" pos (740, 250) font HACK_FONT size 18 color "#6f8a99"
            vbox:
                pos (740, 282)
                spacing 8
                for key, label, val in HACK_DENS:
                    button:
                        xsize 700
                        ysize 40
                        background Solid("#12303a" if hack_den == key else "#14202e")
                        hover_background Solid("#1b3040")
                        sensitive hack_phase == "B"
                        action SetVariable("hack_den", key)
                        text label font HACK_FONT size 18 color ("#8ff0dc" if hack_den == key else "#cfe9e3") align (0.5, 0.5)

            vbox:
                pos (790, 450)
                xsize 140
                spacing 4
                text f_n font HACK_FONT size 44 color "#cfe9e3" xalign 0.5
                add Solid("#cfe9e3") xysize (120, 3) xalign 0.5
                text f_d font HACK_FONT size 44 color "#cfe9e3" xalign 0.5
            text f_eq pos (960, 500) font HACK_FONT size 44 color ("#8ff0dc" if hack_phase == "done" else "#6f8a99")

            if hack_phase == "B":
                $ ready = hack_row is not None and hack_den is not None
                button:
                    pos (740, 610)
                    xysize (260, 44)
                    background Solid("#12303a" if ready else "#14202e")
                    hover_background Solid("#1b3040")
                    sensitive ready
                    action Return("check")
                    text "посчитать" font HACK_FONT size 20 color ("#8ff0dc" if ready else "#557777") align (0.5, 0.5)

        if hack_phase == "done":
            button:
                pos (1180, 622)
                xysize (260, 44)
                background Solid("#12303a")
                hover_background Solid("#1b3040")
                action Return("end")
                text "продолжить" font HACK_FONT size 20 color "#8ff0dc" align (0.5, 0.5)


label task2_hack_scene:
    hide image "images/revenue_and_load.png"
    $ renpy.music.set_volume(0.2, delay=1.5)
    scene black with Dissolve(1.8)

    "..."
    sasha_q "Даю тебе доступ в журнал событий. Молчи."
    player "Саша? Ты что-то внезапно подключился...{nw}"
    sasha_q "Такой журнал, в котором хранятся данные о событиях в сети."
    sasha_q "Найдёшь регулярное — найдёшь рабочую гипотезу."
    player "Как ты...{nw}"
    sasha_q "Я всегда знаю, что ты хочешь спросить. Не спрашивай. Слушай."
    player "...{nw}"
    sasha_q "Нет, не спрашивай."
    sasha_q "Нужно по данным понять, какие события происходят со строгой периодичностью. Помнишь SQL?"

    if memory_query_total_mistakes == 0:
        $ task2_sql_level = 2
        player "...{nw}"
        sasha_q "Точно, ты уже писал запрос при мне. Тогда вышло отлично."
        sasha_q "Золотое правило: что показываешь, то и группируй. И не шуми: звёздочка в SELECT значит «всё подряд», журнал такое запоминает. Шум может нас раскрыть."
    elif memory_query_total_mistakes <= 5:
        $ task2_sql_level = 1
        player "...{nw}"
        sasha_q "Точно, ты уже писал запрос при мне. С парой лишних кругов, но писал."
        sasha_q "Освежу одно: звёздочка в SELECT значит «всё подряд». Журнал такое запоминает. А мы хотим, чтобы нас не запомнили. Тащи только те данные, которые нам нужны."
        sasha_q "GROUP BY — это группировка. Представь, что у тебя пять строк, но у всех есть нечто общее. Например, имя магазина. Ты хочешь схлопнуть пять строк до одной."
        sasha_q "COUNT(*) скажет, сколько строк было в каждой кучке. И запомни: что показываешь, то и группируй."
    else:
        $ task2_sql_level = 0
        player "...{nw}"
        sasha_q "Забыл всё, кроме слова select."
        sasha_q "Не могу поверить, что ты на моём месте. Сейчас расскажу по минимуму."
        sasha_q "SELECT — что показать. FROM — откуда. Вместе: «покажи это из этого»."
        sasha_q "Звёздочка в SELECT значит «всё подряд». Журнал такое запоминает, а нам нельзя оставлять следов."
        sasha_q "GROUP BY — свалить одинаковое в кучки. COUNT(*) — посчитать, сколько в каждой."
        sasha_q "Что показываешь, то и группируй. Остальное поймёшь по ходу."

    $ hack_start()
    jump task2_hack_loop


label task2_hack_loop:
    call screen hack_terminal
    $ hack_res = hack_step(_return)
    if hack_res == "end":
        jump task2_hack_exit
    if hack_res == "alarm":
        jump task2_hack_alarm
    jump task2_hack_loop


label task2_hack_alarm:
    $ hack_alarms += 1
    $ accuracy -= HACK_ALARM_PENALTY
    show screen hack_alarm
    pause 1.6
    hide screen hack_alarm

    "ТЕКСТ: соединение сброшено, терминал гаснет."
    boss "ТЕКСТ: аналитик, зачем ты запрашиваешь журналы целиком?"
    player "ТЕКСТ: рутинная проверка целостности. Честно-честно."
    sasha_q "ТЕКСТ: тише. с начала."

    $ hack_reset()
    if HACK_REPLAY_INTRO:
        jump task2_hack_scene
    jump task2_hack_loop


label task2_hack_exit:
    $ task2_secret_access = True
    $ hack_points = max(HACK_MIN_POINTS, HACK_MAX_POINTS - hack_mistakes)
    $ accuracy += hack_points
    if hack_mistakes == 0:
        sasha_q "ТЕКСТ: чисто, с первого раза."

    $ renpy.music.set_volume(1.0, delay=1.5)
    scene bg_terminal with Dissolve(1.5)
    show image "images/revenue_and_load.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve
    player "ТЕКСТ: возврат к графику, гипотезу держим в секрете."
    return
