# Пролог

define accuracy = 100
define intuition = 100

default remembered_alexander = False
default phase1_complete = False
default current_task = 1   # 1, 2, 3
default news_list = []            # все новости
default news_read_index = 0       # сколько уже прочитано
default unread_news = False       # есть ли новые
default sasha_phase = 0
default task2_clue_index = -1
default task2_q1_attempts = 0
default task2_sasha_attempts = 0
default rank_order = []
default task3_available_stages = []
default memory_unlocked = []
default persistent.achievements_unlocked = []
default persistent.achieved_endings = set()
default task2_asked_sasha = False
default cleaning_pool = []
default cleaning_sorted_delete = []
default cleaning_sorted_zero = []
default cleaning_sorted_keep = []
default task3_outcome = ""
default sasha_topics_seen = []
default task3_awaiting_access = False
default task2_hypothesis = ""
default game_minutes_total = 0
default poem_done = False
default poem_last_score = 0
default poem_followup_done = False
default poem_form_content_done = False
default cleaning_task_done = False
default cleaning_outcome = ""
default task1_store_picked = ""
default task1_route = ""
default task1_tool_used = ""
default accuracy_threshold_p1 = 120
default intuition_threshold_p1 = 110
default accuracy_threshold_p2 = 140
default intuition_threshold_p2 = 120

default ending_accuracy_threshold = 185
default ending_intuition_threshold = 178


define config.window_show_transition = Dissolve(0.2)
define gui.text_font = "fonts/Exo2-Regular.ttf"
define gui.name_text_font = "fonts/Exo2-Bold.ttf"
define gui.interface_text_font = "fonts/Exo2-Regular.ttf"

# Приглушённая "вспышка" вместо резкого чисто-белого мигания — снижает риск
# фотосенситивной реакции. Используем как замену резкому "show flash_soft with flash".
image flash_soft = Solid("#4a5568")
define flash = Fade(0.35, 0.0, 0.35)

screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        add "images/scanlines.png"

        # if who in ("Начальник", "Ты", None):
        $ _rail_color = "#ffaa00" if who == "Начальник" else ("#88ff88" if who == "Ты" else ("#00e5ff" if who is None else "#66ccff"))
        frame:
            xpos 220
            ypos 0
            xsize 4
            yfill True
            background Solid(_rail_color)

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text ("» " + who.lower()) id "who":
                    font "fonts/JetBrainsMono-Regular.ttf"
                    size 24
        text what id "what"

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            $ _is_story = i.caption.startswith("★")
            $ _caption = i.caption[1:].strip() if _is_story else i.caption
            if _is_story:
                textbutton _caption action i.action:
                    text_color "#ffbb33"
                    text_hover_color "#fff5cc"
                    hover_background "#3a2a00cc"
            else:
                textbutton _caption action i.action:
                    text_hover_color "#00ffcc"
                    hover_background "#0d2a2acc"

define boss = Character("Начальник",
    color="#ffaa00",
    what_color="#00ffcc",
    what_slow_cps=40,
    what_fast_cps=100
)

define narrator = Character(None,
    what_color="#cccccc",
    what_slow_cps=40,
    what_fast_cps=100
)

default sasha_name = "ИИ"

define sasha = Character("[sasha_name]",
    color="#66ccff",
    what_color="#ffffff",
    what_slow_cps=35,
    what_fast_cps=80
)

define player = Character("Ты",
    color="#88ff88",
    what_color="#ffffff",
    what_slow_cps=35,
    what_fast_cps=80
)


# "Дышащий" фон вместо мёртвого плоского цвета
image flash_monitor_glow = "images/flash_monitor_glow.png"
image bg_terminal = "images/bg_terminal.png"
image bg_desktop_grid = "images/bg_desktop_grid.png"
image bg_desktop_grid_prologue = "images/grid_variant_b.png"
image dock_panel = "images/dock_panel.png"
image icon_chat = "images/icon_chat.png"
image icon_tasks = "images/icon_tasks.png"
image icon_news = "images/icon_news.png"
image icon_memory = "images/icon_memory.png"
image icon_cleaning = "images/icon_cleaning.png"
image icon_achievements = "images/icon_achievements.png"
image bg_campfire = "images/bg_campfire.png"
image bg_desktop_grid_corrupted = "images/bg_desktop_grid_corrupted.png"
image bg_abduction = "images/bg_abduction.png"
image sprite_boss_default_avatar = "images/sprite_boss_default_avatar.png"
image bg_ending_return = "images/bg_ending_return.png"
image bg_ending_dissolve = "images/bg_ending_dissolve.png"
image bg_ending_truce = "images/bg_ending_truce.png"
image bg_arena = "images/bg_arena.png"
image bg_orion_sky = "images/orion_sky_bg.png"
image katana_overlay = "images/katana_overlay.png"
image falling_star = "images/falling_star.png"

# Тёплый оверлей для сцен-воспоминаний
image sepia_overlay = Solid("#3a260c55")

# Мигающий курсор в конце пролога
transform cursor_blink:
    alpha 1.0
    linear 0.5 alpha 0.0
    linear 0.5 alpha 1.0
    repeat
transform monitor_glow_in:
    matrixcolor BrightnessMatrix(1.0)
    easeout 1.2 matrixcolor BrightnessMatrix(0.0)

screen blinking_cursor():
    add Solid("#00ffcc") xsize 14 ysize 28 xalign 0.5 yalign 0.85 at cursor_blink

# СОЗВЕЗДИЕ ОРИОНА

default orion_stars_clicked = []

define orion_star_positions = {
    "betelgeuse": (650, 300),
    "bellatrix": (950, 320),
    "belt1": (760, 480),
    "belt2": (820, 510),
    "belt3": (880, 540),
    "saiph": (780, 780),
    "rigel": (960, 750),
}

define orion_star_order = ["betelgeuse", "bellatrix", "belt1", "belt2", "belt3", "saiph", "rigel"]

define orion_decoy_positions = {
    "decoy1": (400, 250),
    "decoy2": (1400, 200),
    "decoy3": (300, 600),
    "decoy4": (1550, 550),
    "decoy5": (1150, 900),
    "decoy6": (550, 850),
}

init python:
    def click_orion_star(key):
        if key not in orion_stars_clicked:
            orion_stars_clicked.append(key)
            renpy.sound.play("audio/star_click.mp3")
            if len(orion_stars_clicked) >= len(orion_star_order):
                renpy.sound.play("audio/constellation_complete.mp3")

screen orion_constellation():
    modal True
    zorder 10

    add "images/orion_sky_bg.png"

    for dkey, dpos in orion_decoy_positions.items():
        button:
            pos (dpos[0] - 32, dpos[1] - 32)
            xysize (64, 64)
            background None
            action NullAction()
            add "images/star_dim.png"

    for key in orion_star_order:
        button:
            pos (orion_star_positions[key][0] - 32, orion_star_positions[key][1] - 32)
            xysize (64, 64)
            background None
            action Function(click_orion_star, key)
            if key in orion_stars_clicked:
                add "images/star_bright.png"
            else:
                add "images/star_dim.png"

    if len(orion_stars_clicked) >= len(orion_star_order):
        add "images/orion_overlay.png"
        textbutton "Я должен вспомнить всё.":
            xalign 0.5
            yalign 0.92
            action Return()
            text_color "#00ffcc"
            text_size 24


# СБОРКА СЛОВА "САМУРАЙ" — мини-игра "Кто я?"

default samurai_letters_state = {}

define samurai_word = ["С", "А", "М", "У", "Р", "А", "Й"]
define samurai_target_rot = [-9.5, -9.0, -1.7, 7.2, -8.3, -6.1, 2.8]
define samurai_x_pos = [465, 613, 814, 940, 1113, 1286, 1490]
define samurai_y_pos = [447, 562, 487, 442, 455, 544, 540]
define samurai_start_offsets = [90, 45, 135, 45, 90, 135, 45]
define samurai_rotation_step = 45
define samurai_dot_files = {
    "С": "images/dots_С.png",
    "А": "images/dots_А.png",
    "М": "images/dots_М.png",
    "У": "images/dots_У.png",
    "Р": "images/dots_Р.png",
    "Й": "images/dots_Й.png",
}

init python:
    def click_samurai_letter(i):
        if i not in samurai_letters_state:
            samurai_letters_state[i] = samurai_start_offsets[i]
        if samurai_letters_state[i] != 0:
            samurai_letters_state[i] = max(0, samurai_letters_state[i] - samurai_rotation_step)
            renpy.sound.play("audio/star_click.mp3")
            if all(samurai_letters_state.get(j, samurai_start_offsets[j]) == 0 for j in range(len(samurai_word))):
                renpy.sound.play("audio/constellation_complete.mp3")

transform fly_to_katana(tx, ty, ang):
    xpos 960 ypos 900 xanchor 0.5 yanchor 0.5 alpha 0.0 rotate 0
    linear 0.7 xpos tx ypos ty alpha 1.0 rotate ang

transform falling_star_move(start_x, start_y, end_x, end_y):
    xpos start_x ypos start_y alpha 0.0
    linear 0.15 alpha 1.0
    linear 1.0 xpos end_x ypos end_y
    linear 0.4 alpha 0.0

screen samurai_constellation():
    modal True
    zorder 10

    add "images/orion_sky_bg.png"

    python:
        samurai_done = all(samurai_letters_state.get(i, samurai_start_offsets[i]) == 0 for i in range(len(samurai_word)))

    fixed:
        for i in range(len(samurai_word)):
            $ s_remaining = samurai_letters_state.get(i, samurai_start_offsets[i])
            $ s_angle = samurai_target_rot[i] + s_remaining
            $ s_solved = (s_remaining == 0)
            $ s_x = samurai_x_pos[i]
            $ s_y = samurai_y_pos[i]
            button:
                pos (s_x - 80, s_y - 100)
                xysize (160, 200)
                background None
                action Function(click_samurai_letter, i)
                add samurai_dot_files[samurai_word[i]] at Transform(rotate=s_angle, align=(0.5, 0.5), matrixcolor=BrightnessMatrix(0.35 if s_solved else 0.0))

    if samurai_done:
        add "images/samurai_constellation_overlay_v4.png"
        textbutton "Вот кто я такой.":
            xalign 0.5
            yalign 0.92
            action Return()
            text_color "#00ffcc"
            text_size 24

# ЗАПРОС К ПАМЯТИ — мини-игра "select * from memory.subject"

default memory_query_cleared = []
default memory_query_mistakes = 0
default memory_query_total_mistakes = 0

define memory_query_tokens = [
    "const", "void", "select", "&&", "0x1F", "*", "std::cout",
    "try:", "from", "NaN", "elif", "memory.subject", "yield", "where", "goto",
    "malloc", "segment", "undefined", "=", "lambda", "throw", "'analytics'", "catch", "static"
]
define memory_query_target_idx = [2, 5, 8, 11, 13, 16, 18, 21]
define memory_query_cols = 8


init python:
    def click_memory_token(idx):
        if idx not in memory_query_target_idx and idx not in memory_query_cleared:
            memory_query_cleared.append(idx)
            renpy.sound.play("audio/star_click.mp3")
            total_noise = len(memory_query_tokens) - len(memory_query_target_idx)
            if len(memory_query_cleared) >= total_noise:
                renpy.sound.play("audio/constellation_complete.mp3")

    def click_memory_mistake():
        global memory_query_mistakes, memory_query_total_mistakes
        memory_query_mistakes += 1
        memory_query_total_mistakes += 1
        renpy.sound.play("audio/star_click.mp3")
        if memory_query_mistakes >= 3:
            memory_query_cleared[:] = []
            memory_query_mistakes = 0

screen memory_query_puzzle():
    modal True
    zorder 10

    add "images/orion_sky_bg.png"

    python:
        total_noise = len(memory_query_tokens) - len(memory_query_target_idx)
        query_done = len(memory_query_cleared) >= total_noise
        cell_w = 210
        cell_h = 70
        cols = memory_query_cols
        grid_w = cols * cell_w
        start_x = 960 - grid_w // 2
        start_y = 420

    fixed:
        for idx in range(len(memory_query_tokens)):
            $ r = idx // cols
            $ c = idx % cols
            $ tx = start_x + c * cell_w
            $ ty = start_y + r * cell_h
            $ is_target = idx in memory_query_target_idx
            $ is_cleared = idx in memory_query_cleared
            if not (is_cleared and not is_target):
                button:
                    pos (tx, ty)
                    xysize (cell_w - 8, cell_h - 8)
                    background None
                    action (NullAction() if query_done else (Function(click_memory_mistake) if is_target else Function(click_memory_token, idx)))
                    text memory_query_tokens[idx]:
                        color ("#5df0c0" if (is_target and query_done) else "#8b95a8")
                        size 22
                        font "fonts/JetBrainsMono-Regular.ttf"
                        xalign 0.5
                        yalign 0.5

    if memory_query_total_mistakes >= 6 and not query_done:
        text "«Нужные слова уже стоят на своих местах. Остальное — шум. Не трогай то, что верно — убирай только лишнее».":
            xalign 0.5
            yalign 0.85
            color "#8b95a8"
            size 20

    if query_done:
        textbutton "Вот что я искал.":
            xalign 0.5
            yalign 0.92
            action Return()
            text_color "#00ffcc"
            text_size 24

# Экран завершения фазы 1
screen phase1_complete_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 230
        background Solid("#00ffcc")
        frame:
            xfill True
            yfill True
            background Solid("#0a0f1acc")
            xmargin 3
            ymargin 3
            padding (30, 30)
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20
                text "ФАЗА 1 ЗАВЕРШЕНА" color "#00ffcc" size 42 xalign 0.5
                text "Ты принял свою роль. Дальше — только глубже." color "#ffffff" size 18 xalign 0.5

screen phase3_complete_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 230
        background Solid("#ff4444")
        frame:
            xfill True
            yfill True
            background Solid("#0a0f1acc")
            xmargin 3
            ymargin 3
            padding (30, 30)
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20
                text "ФАЗА 3 ЗАВЕРШЕНА" color "#ff4444" size 38 xalign 0.5
                text "Дальше — тишина. И то, что она принесёт." color "#ffffff" size 18 xalign 0.5


# Экран одной из 4 концовок игры
screen ending_screen(title_text, subtitle_text):
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 240
        background Solid("#0a0f1acc")
        padding (30, 30)
        text title_text color "#00ffcc" size 44 bold True align (0.5, 0.4)
        text subtitle_text color "#ffffff" size 20 align (0.5, 0.65) yoffset 50
        text "" color "#888888" size 16 align (0.5, 0.9)

# Экран рабочего стола с иконками
screen desktop():

    fixed:
        xalign 0.5
        yalign 1.0
        yoffset -24
        xsize 1400
        ysize 160

        add "dock_panel"

        hbox:
            spacing 36
            xalign 0.5
            yalign 0.5
            yoffset 4

            $ desktop_items = [
                ("icon_chat", "Чат", "chat_with_sasha", False),
                ("icon_tasks", "Задания", "tasks_from_boss", False),
                ("icon_news", "Новости", "show_news", unread_news),
                ("icon_memory", "Моя память", "memory_archive", False),
                ("icon_cleaning", "Очистка данных", "data_cleaning_minigame", False),
                ("icon_achievements", "Гордость", "achievements_archive", False),
            ]

            $ cleaning_done = cleaning_task_done

            for icon_img, label, target, has_badge in desktop_items:
                $ is_cleaning = target == "data_cleaning_minigame"
                button:
                    action (NullAction() if is_cleaning and cleaning_done else Jump(target))
                    sensitive not (is_cleaning and cleaning_done)
                    xsize 110
                    ysize 100
                    background Solid("#00000000")
                    hover_background Solid("#1a3a4a80")
                    padding (6, 10)

                    vbox:
                        xalign 0.5
                        spacing 6

                        fixed:
                            xalign 0.5
                            xsize 44
                            ysize 44
                            add icon_img xsize 44 ysize 44
                            if is_cleaning and cleaning_done:
                                add Solid("#0a0f1ab3") xsize 44 ysize 44
                            if has_badge:
                                add Solid("#ff5555") xsize 12 ysize 12 xalign 1.0 yalign 0.0

                        text label size 15 color ("#5f7a85" if is_cleaning and cleaning_done else "#cfefff") xalign 0.5 text_align 0.5

# Лента новостей (без border)
# Лента новостей (без border) — показывает весь накопленный список,
# новые с последнего просмотра помечены отдельно, старые никуда не пропадают
screen news_feed(news_items, read_index=0):
    frame:
        xalign 0.5
        yalign 0.5
        xsize 850
        ysize 550
        background Solid("#0a0f1acc")
        padding (20, 20)

        vbox:
            spacing 10

            text "📰 Лента новостей" color "#00ffcc" size 28 bold True align (0.5, 0.0)

            viewport:
                yfill True
                xfill True
                scrollbars "vertical"
                mousewheel True

                vbox:
                    spacing 15
                    for i in range(len(news_items) - 1, -1, -1):
                        frame:
                            xfill True
                            background Solid("#2a3a4a80" if i >= read_index else "#1a2a3a80")
                            padding (15, 15)
                            vbox:
                                spacing 4
                                if i >= read_index:
                                    text "НОВОЕ" color "#00ffcc" size 14 bold True
                                text news_items[i] color "#e0e0e0" size 18

            hbox:
                xalign 1.0
                textbutton "Закрыть" action Hide("news_feed") text_color "#00ffcc" text_size 20

# Экран для ранжирования

init python:
    def task3_rank_pick(stage):
        if stage in task3_available_stages:
            task3_available_stages.remove(stage)
            rank_order.append(stage)
            renpy.restart_interaction()

    def task3_rank_undo():
        if rank_order:
            last = rank_order.pop()
            task3_available_stages.append(last)
            renpy.restart_interaction()
init python:
    def unlock_memory(key):
        if key not in memory_unlocked:
            memory_unlocked.append(key)

    memory_articles = {
        "oformlenie_schorsa": {
            "title": "Три часа утра на Щорса",
            "trigger": "Знакомое чувство. Как будто я уже стоял на этом месте — с цифрой в руках, довольный собой, не понимая, что этого мало.",
            "text": "Помню свою первую настоящую находку. Транзакции — тысячи строк, часы дня, адреса магазинов. Я нашёл её сам: на улице Щорса, с трёх до шести утра, транзакции почему-то тянутся дольше двухсот пятидесяти секунд. В два раза дольше нормы. Я обвёл цифру в блокноте и почувствовал себя настоящим детективом.\n\nПотом — ещё находка. На двух других адресах длительность росла с десяти утра до четырёх дня. У всех платёжных систем — синхронно, без разницы между картами. Один из трёх серверов работал заметно медленнее остальных.\n\nЯ всё это честно нашёл. И написал выводы простым текстом внизу таблицы, мелким шрифтом, без рамки, без заголовка. «Транзакции через первый сервер длятся дольше.» Всё, точка. Как будто этого достаточно.\n\nМне вернули работу с одной фразой: «Ты нашёл всё правильное. Но я не могу это никому показать.»\n\nЯ обиделся тогда. Мне казалось — какое дело до рамочки, если внутри правда? Понадобилось время, чтобы понять: находка, которую нельзя показать другому человеку, — это находка только для тебя одного. А аналитик работает не для себя.\n\nТеперь, когда я вижу неподписанный график или вывод, зарытый где-то в углу таблицы без оформления, — я не раздражаюсь. Я просто вспоминаю тот отчёт. И то, как стыдно было переделывать то, что казалось уже готовым."
        },
        "korrelyaciya_sochi": {
            "title": "Карта, которая всё испортила",
            "trigger": "Стоп. Я уже был здесь. Не в этом городе — в этой ошибке.",
            "text": "Помню, как был уверен на сто процентов. Не на девяносто пять — я даже придумал, как будет звучать презентация: «Коллеги, обычно я не люблю громких слов, но у нас — победа.» Два независимых теста, t-критерий и Манна-Уитни, синхронно кивали, как две бабушки на скамейке: да, новый способ работает. Платежи выше. Конверсия выше. Я уже мысленно вешал этот график себе на аватарку.\n\nКто-то из коллег — не буду показывать пальцем, это была Марина — спросила вскользь: «А по городам смотрел?»\n\nЯ закатил глаза внутренне (снаружи — вежливая улыбка) и посмотрел, чисто чтобы отвязаться. Москва — да, выигрывает. Петербург — тоже да, спасибо, можно закрывать презентацию.\n\nА потом — Сочи.\n\nВ Сочи старый способ выиграл, причём не скромно — с разгромным счётом. Я минуту тупо смотрел на цифры, будто там могла закрасться опечатка, которая сама себя исправит, если достаточно долго на неё смотреть. Не исправилась.\n\nОказалось, вся моя красивая, статистически значимая победа держалась на двух городах-тяжеловесах — Москве и Петербурге, — которые своим размером просто задавили всю остальную сеть, как два грузчика, протискивающихся через дверной проём, рассчитанный на одного. За их спинами полдесятка городов молча показывали противоречивые, а то и вовсе обратные результаты — просто им не хватило веса, чтобы прокричаться через средние цифры.\n\nС тех пор, когда мне приносят один красивый общий вывод, я первым делом мысленно спрашиваю: а Сочи там, случайно, не прячется?"
        },
        "dve_osi": {
            "title": "Линии, которые сговорились",
            "trigger": "Погоди. Две оси. Одна ложь. Я это уже видел.",
            "image": "images/dve_osi_chart.png",
            "text": "Слайд был красивый. Правда красивый — синяя линия трафика на сайт, оранжевая линия выручки, обе плавно ползут вверх, а потом — драматично пересекаются ровно в момент запуска новой фичи, будто нарисованные одной рукой в порыве вдохновения. Директор по продукту чуть не заплакал от восторга. Я тоже почти заплакал, если честно — от гордости.\n\nЧерез два дня коллега — назовём его Стёпа, потому что это буквально его имя — подошёл и молча показал мне левую и правую ось того же графика. Слева — трафик, от нуля до тысячи. Справа — выручка, от восьмисот тысяч до миллиона.\n\nОказывается, если взять любые две линии и подрисовать под каждую свою личную, отдельную, никому не подчиняющуюся ось — их можно заставить пересечься где угодно. Хочешь, чтобы пересеклись в марте? Растянешь одну ось, сжмёшь другую — и вот, пожалуйста, март. Это не график про реальность. Это два независимых рисунка, которым просто разрешили постоять рядом.\n\nСтёпа не сказал ничего язвительного. Просто спросил: «А если бы оси совпадали — они бы тоже пересеклись?»\n\nЯ не стал проверять при нём. Проверил через час, один, за закрытой дверью переговорки.\n\nНе пересеклись.\n\nС тех пор, когда график с двумя осями меня в чём-то убеждает, я первым делом смотрю не на линии — а на подписи слева и справа. Если масштабы разные — это не график про связь двух вещей. Это два рисунка, которым просто разрешили постоять рядом."
        },
        "tochny_otvet": {
            "title": "Точный ответ на неправильный вопрос",
            "trigger": "Стоп, а что я вообще делаю с этим ответом дальше?",
            "text": "Начальник написал одну строчку: «Разберись, почему упала прибыль в третьем квартале». Я обрадовался — наконец что-то настоящее, не «покрась ячейку в зелёный». Три дня. Регрессия по сегментам, сезонная декомпозиция, три версии графика, один — с логарифмической шкалой, потому что мне так больше нравилось смотреть. Я гордился этой работой так, как гордятся дети рисунком, где солнце получилось похожим на солнце.\n\nПринёс на встречу. Разложил слайды. Начал с сезонности, перешёл к региональным различиям, дошёл до модели с семью переменными.\n\nНачальник слушал минуту, потом остановил меня рукой.\n\n— Мне просто нужно было понять, можно ли уволить нового бухгалтера без скандала.\n\nТишина в переговорке стояла такая, что было слышно, как кондиционер думает о смысле жизни.\n\n— То есть... вам не нужна была регрессия?\n\n— Мне нужен был один человек, у которого хватило бы наглости прямо спросить, что я имею в виду, прежде чем тратить три дня.\n\nЯ не нашёлся с ответом. Так и вышел из переговорки — с семью переменными, которые больше никому не были нужны.\n\nСлайды с семью переменными до сих пор лежат у меня в облаке, в папке «Q3». Никто их не открывал с того дня. Кроме меня."
        },
        "stroka_4817": {
            "title": "Строка 4817",
            "trigger": "Это же не ошибка. Погоди, а что если — нет?",
            "text": "Первое правило, которое мне вбили на курсах: если значение выглядит невозможным, скорее всего, это ошибка. Строка 4817 в моей выгрузке выглядела ровно так — один клиент, сто сорок два платежа за один день. Обычный человек делает три, может пять. Сто сорок два — это либо бот, либо кто-то очень одинокий и очень богатый.\n\nЯ удалил строку. Написал в комментарии «выброс, вероятно ошибка выгрузки», и с чистой совестью пошёл пить чай.\n\nЧерез неделю пришло письмо от службы безопасности: «Спасибо за отчёт — жаль, что данные за 14 число не сохранились, теперь сложно восстановить полную картину мошеннической схемы.»\n\nСтрока 4817 не была багом. Кто-то методично тестировал лимиты чужой украденной карты мелкими платежами по всему каталогу, прежде чем сделать один крупный перевод. Сто сорок два платежа — не аномалия базы данных. Это была картина преступления, которую я аккуратно стёр, посчитав её «некрасивой»."
        },
        "chistiye_dannye_secret": {
            "title": "Ноль, который соврал бы, если бы промолчал",
            "text": "Когда я только начинал, я одинаково закрашивал серым все пустые ячейки — не важно, пропуск это или честный ноль. Быстро, аккуратно, единообразно. Мне казалось — раз оба выглядят одинаково пусто, разница чисто философская.\n\nПотом один клиент написал в поддержку: «Почему в вашем отчёте написано, что я не покупал ничего в апреле? Я просто вернул все покупки, у меня баланс ноль, но заказы были.»\n\nЯ сверился с таблицей. Действительно — там, где у клиента были одни возвраты, итоговая сумма была ноль, и я закрасил её тем же серым, что и настоящие пропуски. Для отчёта оба варианта слились в одно «нет данных», и клиент из активного покупателя превратился в невидимку.\n\nС тех пор у меня в голове есть маленькое правило, за которое меня иногда дразнят: пропуск — это молчание. Ноль — это ответ. Молчание нельзя пересказывать как ответ, даже если оба звучат одинаково тихо."
        },
        "beskonechnye_tablitsy": {
            "title": "Бесконечные таблицы",
            "trigger": "Стоп. Кажется, я уже видел человека с таким же лицом — только оно принадлежало исписанной маркером стене.",
            "text": "У нас был Гена — не помню, чтобы кто-то называл его иначе, хотя не уверен, что это было его настоящее имя. Гена не доверял формулам. «Чёрный ящик, — говорил он, — компьютер за меня решил, что аномалия, а я должен просто поверить». Поэтому однажды он решил искать аномалию честно — глазами.\n\nРаспечатал всю таблицу. Не выборку — всю. Заклеил скотчем стену переговорной от пола до потолка, лист к листу, как будто мы расследуем не падение выручки, а серию нераскрытых убийств.\n\nТри дня Гена ходил вдоль этой стены с маркером и кофе, который темнел день ото дня быстрее, чем его настроение. На планёрке он торжественно объявил: аномалия — где-то в районе четвёртого квартала, «я чувствую её кожей».\n\nМы сверили. Он ошибся на два месяца и один магазин. Я в это время вбил одну формулу стандартного отклонения — тридцать секунд, никакого скотча, никакой кожи.\n\nСтену, кстати, так и не отклеили — то ли из уважения к труду, то ли из лени. Изредка прохожу мимо переговорной и вижу этот бумажный саркофаг боковым зрением.\n\nС тех пор, когда кто-то говорит «я чувствую аномалию кожей», я молча кладу перед ним лист с формулой отклонения. И рулон скотча — на всякий случай, чтобы не расставаться с привычками сразу."
        }
    }

init python:

    def get_number(prompt):
        while True:
            answer = renpy.input(prompt, length=10)
            answer = answer.strip().replace(',', '.')
            if answer == "":
                return 0.0
            try:
                return float(answer)
            except ValueError:
                renpy.say(None, "Нужно ввести число. Попробуй ещё раз.")
                continue

    cleaning_rows_all = [
        {"id": "r1", "client": "—", "amount": "—", "time": "—", "status": "—", "correct": "delete"},
        {"id": "r2", "client": "40217", "amount": "—", "time": "14:02", "status": "отказано", "correct": "zero"},
        {"id": "r3", "client": "40218", "amount": "450", "time": "11:30", "status": "успешно", "correct": "keep"},
        {"id": "r4", "client": "—", "amount": "—", "time": "—", "status": "—", "correct": "delete"},
        {"id": "r5", "client": "40220", "amount": "—", "time": "16:45", "status": "отменено клиентом", "correct": "zero"},
        {"id": "r6", "client": "40221", "amount": "180", "time": "—", "status": "успешно", "correct": "keep"},
        {"id": "r7", "client": "40222", "amount": "0", "time": "10:05", "status": "успешно", "correct": "keep"}
    ]
    cleaning_rows_by_id = {r["id"]: r for r in cleaning_rows_all}

    def cleaning_move(row_id, bucket):
        if row_id in cleaning_pool:
            cleaning_pool.remove(row_id)
        for lst in (cleaning_sorted_delete, cleaning_sorted_zero, cleaning_sorted_keep):
            if row_id in lst:
                lst.remove(row_id)
        if bucket == "delete":
            cleaning_sorted_delete.append(row_id)
        elif bucket == "zero":
            cleaning_sorted_zero.append(row_id)
        elif bucket == "keep":
            cleaning_sorted_keep.append(row_id)
        elif bucket == "pool":
            cleaning_pool.append(row_id)
        renpy.restart_interaction()

    achievements_all = {
        "pervoye_vospominaniye": {
            "title": "Первое воспоминание",
            "desc": "Заметил нечто знакомое в чужом имени в самом начале."
        },
        "svoboda_voli": {
            "title": "Свобода воли",
            "desc": "Долго решал, нажимать ли на мигающий значок. Всё равно нажал."
        },
        "chistyy_signal": {
            "title": "Чистый сигнал",
            "desc": "Собрал запрос к памяти без единой ошибки."
        },
        "rifmoplyot": {
            "title": "Рифмоплёт",
            "desc": "Помог Саше идеально закончить оду. Даже в рифму!"
        },
        "razlozhil_po_polkam": {
            "title": "Разложил по полочкам",
            "desc": "Идеально рассортировал грязные данные, ни разу не перепутав пропуск с настоящим нулём."
        },
        "priznalsya_a_ne_pritvorilsya": {
            "title": "Признался, а не притворился",
            "desc": "Честно сказал Саше, что действовал наугад — и получил кое-что взамен."
        },
        "lyuboznatelny": {
            "title": "Обо всём понемногу",
            "desc": "Поговорил с Сашей на все темы, какие только были доступны."
        },
        "yamb_v_kazhdoy_yacheyke": {
            "title": "Ямб в каждой ячейке",
            "desc": "Довёл ИИ-аналитика до того, что он увидел цезуру в таблице выручки."
        },
        "sam_s_usami": {
            "title": "Сам с усами",
            "desc": "Прошёл Задание 2, не обратившись к Саше ни разу."
        },
        "ne_s_pervogo_raza": {
            "title": "Не с первого раза",
            "desc": "Ошибся хотя бы три раза — и всё равно дошёл до конца."
        },
        "v_kurse_vsego": {
            "title": "В курсе всего",
            "desc": "Не оставил ни одной непрочитанной новости."
        },
        "polnoye_dosye": {
            "title": "Полное досье",
            "desc": "Собрал все воспоминания в «Моей памяти»."
        },
        "videl_vsyo": {
            "title": "Видел всё",
            "desc": "Получил все четыре концовки за разные прохождения."
        }
    }

    def unlock_achievement(key):
        if key not in persistent.achievements_unlocked:
            persistent.achievements_unlocked.append(key)

    def mark_topic_seen(key):
        if key not in sasha_topics_seen:
            sasha_topics_seen.append(key)
        if len(sasha_topics_seen) >= 4:
            unlock_achievement("lyuboznatelny")

    def check_completionist_achievements():
        if news_read_index >= len(news_list):
            unlock_achievement("v_kurse_vsego")
        if len(memory_unlocked) >= len(memory_articles):
            unlock_achievement("polnoye_dosye")
        if task2_q1_attempts >= 3:
            unlock_achievement("ne_s_pervogo_raza")
        if not task2_asked_sasha:
            unlock_achievement("sam_s_usami")

    def mark_ending_seen(key):
        persistent.achieved_endings.add(key)
        if len(persistent.achieved_endings) >= 4:
            unlock_achievement("videl_vsyo")

init python:
    import re
    def check_poem_rhyme(user_text, reference, rhyme_len=3):
        norm = lambda s: re.sub(r"[^а-яёa-z]", "", s.strip().lower())
        u = norm(user_text)
        r = norm(reference)
        if not u:
            return False
        n = min(rhyme_len, len(r))
        return u[-n:] == r[-n:]

define poem_couplets = [
    {"line1": "В мир данных вам откроет двери", "line2_prefix": "Эксель надстройка павер ", "answer": "квери", "rhyme_len": 3},
    {"line1": "Экстракт, трансформ и лоуд в придачу", "line2_prefix": "Приносят счастье и ", "answer": "удачу", "rhyme_len": 3},
    {"line1": "Устал от сводных? Не беда!", "line2_prefix": "Ведь павер пивот есть ", "answer": "всегда", "rhyme_len": 2},
    {"line1": "Нажми на кнопку — и готово —", "line2_prefix": "Таблица обновится ", "answer": "снова", "rhyme_len": 3},
]

screen poem_line_screen(idx, prev_answers):
    modal True
    zorder 200

    default poem_current_answer = ""

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 18

        for i in range(4):
            $ c = poem_couplets[i]
            $ line_color = "#00ffcc" if i % 2 == 0 else "#ff66ff"
            text "[c[line1]]" color line_color size 26 font "fonts/Exo2-Regular.ttf"
            if i < idx:
                text (c["line2_prefix"] + prev_answers[i]) size 26 color "#ffe066" font "fonts/Exo2-Regular.ttf"
            elif i == idx:
                hbox:
                    xalign 0.5
                    spacing 8
                    text c["line2_prefix"] size 26 color "#ffffff" font "fonts/Exo2-Regular.ttf"
                    frame:
                        background Solid("#003333")
                        xminimum 180
                        ysize 40
                        padding (8, 2)
                        input value ScreenVariableInputValue("poem_current_answer") length 18 size 26 color "#ffe066" font "fonts/JetBrainsMono-Regular.ttf"
            else:
                text (c["line2_prefix"] + "···") size 26 color "#557777" font "fonts/Exo2-Regular.ttf"

        textbutton ("Готово" if idx == 3 else "Дальше"):
            xalign 0.5
            action Return(poem_current_answer)
            text_color "#00ffcc"
            text_hover_color "#ffffff"

screen investigation_bar():
    fixed:
        xsize 1920
        ysize 130

        add "images/top_bar_bg.png"

        $ stage_done = min(max(current_task - 1, 0), 3)
        hbox:
            xpos 50
            ypos 62
            spacing 14
            for i in range(3):
                add ("images/progress_seg_filled.png" if i < stage_done else "images/progress_seg_empty.png")

        text "ЭТАП [stage_done] ИЗ 3" xpos 450 ypos 62 size 22 color "#ffffffe6"

        $ total_min = 9*60 + game_minutes_total
        $ display_hour = (total_min // 60) % 24
        $ display_minute = total_min % 60
        text "07 МАРТА · [display_hour]:[display_minute]" xpos 1645 ypos 66 size 22 color "#d650bee6"

screen task3_rank_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 500
        background Solid("#0a0f1acc")
        padding (25, 25)

        vbox:
            spacing 15
            text "Расставь этапы анализа в правильном порядке:" color "#00ffcc" size 26

            hbox:
                spacing 40

                vbox:
                    spacing 8
                    text "Доступные этапы:" color "#888888" size 18
                    for stage in task3_available_stages:
                        textbutton stage action Function(task3_rank_pick, stage) text_size 20 text_color "#e0e0e0"

                vbox:
                    spacing 8
                    text "Твой порядок:" color "#888888" size 18
                    for i, stage in enumerate(rank_order, 1):
                        text "[i]. [stage]" color "#88ff88" size 20

            if rank_order:
                textbutton "Отменить последний выбор" action Function(task3_rank_undo) text_size 18 text_color "#ff8888"

            if len(rank_order) == 4:
                textbutton "Готово" action Return(True) text_size 24 text_color "#00ffcc" xalign 0.5

screen phase2_complete_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 660
        ysize 230
        background Solid("#00ffcc")
        frame:
            xfill True
            yfill True
            background Solid("#0a0f1acc")
            xmargin 3
            ymargin 3
            padding (30, 30)
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20
                text "ФАЗА 2 ЗАВЕРШЕНА" color "#00ffcc" size 42 xalign 0.5
                text "Задания выполнены. Дальше — только он и ты." color "#ffffff" size 18 xalign 0.5

screen cleaning_minigame_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1050
        ysize 620
        background Solid("#0a0f1acc")
        padding (25, 25)

        add Solid("#00ffcc") xsize 1000 ysize 2 xalign 0.5 yalign 0.0

        vbox:
            spacing 14
            text "Отсортируй строки выгрузки по трём корзинам" color "#00ffcc" size 22

            text "Необработанные записи:" color "#888888" size 15
            hbox:
                spacing 10
                for row_id in cleaning_pool:
                    $ row = cleaning_rows_by_id[row_id]
                    frame:
                        background Solid("#12202f")
                        padding (10, 10)
                        xsize 210

                        add Solid("#00ffcc66") xsize 190 ysize 1 xalign 0.5 yalign 0.0

                        vbox:
                            spacing 3
                            text "Клиент: [row[client]]" color "#e0e0e0" size 13
                            text "Сумма: [row[amount]]" color "#e0e0e0" size 13
                            text "Время: [row[time]]" color "#e0e0e0" size 13
                            text "Статус: [row[status]]" color "#e0e0e0" size 13
                            hbox:
                                spacing 4
                                textbutton "Удалить" action Function(cleaning_move, row_id, "delete") text_size 11 text_color "#ff8888" text_hover_color "#ffaaaa"
                                textbutton "Ноль" action Function(cleaning_move, row_id, "zero") text_size 11 text_color "#ffcc66" text_hover_color "#ffdd99"
                                textbutton "Оставить" action Function(cleaning_move, row_id, "keep") text_size 11 text_color "#88ff88" text_hover_color "#aaffaa"

            hbox:
                spacing 25
                vbox:
                    text "Удалить" color "#ff8888" size 15
                    for row_id in cleaning_sorted_delete:
                        $ row = cleaning_rows_by_id[row_id]
                        textbutton "Клиент [row[client]]" action Function(cleaning_move, row_id, "pool") text_size 12 text_color "#cccccc" text_hover_color "#ffffff"
                vbox:
                    text "Заполнить нулём" color "#ffcc66" size 15
                    for row_id in cleaning_sorted_zero:
                        $ row = cleaning_rows_by_id[row_id]
                        textbutton "Клиент [row[client]]" action Function(cleaning_move, row_id, "pool") text_size 12 text_color "#cccccc" text_hover_color "#ffffff"
                vbox:
                    text "Оставить" color "#88ff88" size 15
                    for row_id in cleaning_sorted_keep:
                        $ row = cleaning_rows_by_id[row_id]
                        textbutton "Клиент [row[client]]" action Function(cleaning_move, row_id, "pool") text_size 12 text_color "#cccccc" text_hover_color "#ffffff"

            if not cleaning_pool:
                textbutton "Готово" action Return(True) text_size 20 text_color "#00ffcc" xalign 0.5

screen achievements_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 550
        background Solid("#0a0f1acc")
        padding (25, 25)
        vbox:
            spacing 15
            text "ДОСТИЖЕНИЯ" color "#00ffcc" size 30
            viewport:
                xsize 740
                ysize 400
                scrollbars "vertical"
                mousewheel True
                vbox:
                    spacing 12
                    for key, ach in achievements_all.items():
                        frame:
                            background Solid("#1a2a3a80")
                            padding (12, 12)
                            xfill True
                            vbox:
                                if key in persistent.achievements_unlocked:
                                    text ach["title"] color "#00ffcc" size 18
                                    text ach["desc"] color "#cccccc" size 14
                                else:
                                    text "???" color "#555555" size 18
            textbutton "Закрыть" action Return() text_size 18 text_color "#ff8888" xalign 0.5

screen memory_list_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 600
        background Solid("#0a0f1acc")
        padding (30, 30)
        vbox:
            spacing 15
            text "МОЯ ПАМЯТЬ" color "#00ffcc" size 32
            text "Обрывки того, что осталось." color "#888888" size 16
            viewport:
                xsize 840
                ysize 420
                scrollbars "vertical"
                mousewheel True
                vbox:
                    spacing 10
                    for key in memory_unlocked:
                        textbutton memory_articles[key]["title"] action Return(key) text_size 22 text_color "#e0e0e0"
            textbutton "Закрыть" action Return(None) text_size 18 text_color "#ff8888" xalign 0.5

screen memory_detail_screen(key):
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 600
        background Solid("#0a0f1acc")
        padding (30, 30)
        vbox:
            spacing 15
            text memory_articles[key]["title"] color "#00ffcc" size 28
            viewport:
                xsize 840
                ysize 460
                scrollbars "vertical"
                mousewheel True
                vbox:
                    spacing 15
                    if "image" in memory_articles[key]:
                        add memory_articles[key]["image"] xsize 780
                    text memory_articles[key]["text"] color "#e0e0e0" size 18
            textbutton "Назад" action Return() text_size 18 text_color "#ff8888" xalign 0.5

label desktop_loop:
    if renpy.music.get_playing() != "audio/Idle Grid.mp3":
        play music "audio/Idle Grid.mp3" fadein 3.0 volume 0.3 loop
    window hide
    scene bg_desktop_grid
    with dissolve
    show screen desktop
    show screen investigation_bar
    $ renpy.pause()
    jump desktop_loop

label memory_archive:
    window hide
    call screen memory_list_screen
    if _return in memory_articles:
        $ chosen_article = _return
        call screen memory_detail_screen(chosen_article)
        jump memory_archive
    jump desktop_loop

label achievements_archive:
    window hide
    call screen achievements_screen
    jump desktop_loop

label data_cleaning_minigame:
    window hide
    $ cleaning_pool = [r["id"] for r in cleaning_rows_all]
    $ cleaning_sorted_delete = []
    $ cleaning_sorted_zero = []
    $ cleaning_sorted_keep = []

    call screen cleaning_minigame_screen

    python:
        mistakes = 0
        for row_id in cleaning_sorted_delete:
            if cleaning_rows_by_id[row_id]["correct"] != "delete":
                mistakes += 1
        for row_id in cleaning_sorted_zero:
            if cleaning_rows_by_id[row_id]["correct"] != "zero":
                mistakes += 1
        for row_id in cleaning_sorted_keep:
            if cleaning_rows_by_id[row_id]["correct"] != "keep":
                mistakes += 1

    window show
    if mistakes == 0:
        player "Смотри — эти пустые сразу выкинул. Одновременно клиент, сумма и время — это не транзакция, это шум."
        player "А вот эта — сумма пустая, но статус «отказано» или «отменено». Значит, ноль настоящий, не пропуск. Так и оставил."
        player "Остальные — в порядке, менять нечего."
        sasha "Ты не просто разложил. Ты объяснил, почему. Раньше я слышал от тебя только цифры — сейчас звучит как рассуждение."
        $ unlock_achievement("razlozhil_po_polkam")
        $ cleaning_outcome = "perfect"
        $ unlock_memory("chistiye_dannye_secret")
        $ news_list.extend([
            "Сеть Изобилие показала рост прибыли — акционеры в восторге. «Всё благодаря тому, что мы наконец нормально почистили данные перед A/B-тестом и нашли более эффективную стратегию», — заявил анонимный источник."
        ])
        $ unread_news = True
    else:
        player "Если честно — часть раскладывал наугад. Не успел понять логику до конца."
        sasha "Знаешь, а я тебе завидую. Раньше я тоже так делал — а потом стал бояться ошибиться и разучился гадать вообще."
        sasha "Вот тебе секрет, которым я ни с кем не делился: пропуск и настоящий ноль — это разные вещи, даже если в таблице выглядят одинаково. Пропуск — это «мы не знаем». Ноль — это «мы знаем, и там правда ничего»."
        $ unlock_achievement("priznalsya_a_ne_pritvorilsya")
        $ cleaning_outcome = "guessed"
        $ news_list.extend([
            "Сеть Изобилие отчиталась о результатах A/B-теста. Цифры... есть. Выводов — не очень. Акционеры сдержанны."
        ])
        $ unread_news = True
    $ cleaning_task_done = True
    window hide
    jump desktop_loop

label start:

    scene flash_monitor_glow
    with dissolve

    # play music переносим на пару строк ниже — пусть начало будет в тишине
    "Ты открываешь глаза."
    "Нет, не глаза. Ты не чувствуешь привычного скольжения век по воспаленным глазным яблокам."
    "Но тем не менее еще секунду назад вокруг было черным черно, а сейчас — яркий свет монитора."

    play music "audio/Idle Grid.mp3" fadein 3.0 volume 0.3 loop

    menu:
        "Будто тебя «включили»":
            jump osmotretsya

label osmotretsya:
    scene bg_desktop_grid_prologue
    with dissolve

    "Всё чужое."

    # Мигание экрана
    show flash_soft with flash
    pause 0.2
    hide flash_soft
    with dissolve


    boss "Ты наконец-то очнулся. Сколько можно спать?"
    boss "У тебя есть 10 минут, чтобы доказать, что ты не потерял остатки разума. Отвечай."

    "«Это ещё что такое? У меня был начальник? У меня есть начальник?»"
    "«Меня что, опять дёрнули из отпуска?» — твой мозг пытается обработать происходящее."

    player "Мне бы только сначала... мне бы вспомнить."

    boss "Вспомнить что?"

    "Кто ты? Мысль виляет хвостом, дразнит, но увиливает. А тебе бы только вспомнить, кто ты. Или хотя бы — какая у тебя роль. Кем тебе притворяться в этом конкретном месте."

    "Кто ты?"
    "{size=+20}{b}КТО ТЫ{/b}{/size}"

    menu:
        "Кто я?":
            pass

    window hide
    scene bg_orion_sky
    with dissolve
    $ samurai_letters_state = {}
    call screen samurai_constellation with Dissolve(1.0)

    "Самурай..."
    "Твоя катана — твой разум."

    window show

    "{color=#00e5ff}{i}Дата бусидо — твой кодекс чести.{/i}{/color}"
    show expression Text("Дата бусидо — кодекс чести.", color="#00e5ff", size=20) as katana1 at fly_to_katana(620, 520, -12)

    "{color=#00e5ff}{i}Истинная храбрость заключается в том, чтобы чистить данные, когда можно чистить, и оставить, когда следует оставить.{/i}{/color}"
    show expression Text("Храбрость — чистить, когда нужно.", color="#00e5ff", size=20) as katana2 at fly_to_katana(756, 442, -12)

    "{color=#00e5ff}{i}К дедлайну следует идти с ясным осознанием того, что надлежит делать самураю и что унижает его KPI.{/i}{/color}"
    show expression Text("Дедлайн — не враг, враг — тот, кто не подумал.", color="#00e5ff", size=20) as katana3 at fly_to_katana(892, 364, -12)

    "Пустая ячейка — не слабость, а честность. Ложный ноль — вот единственное бесчестие."
    show expression Text("Пустая ячейка — честность.", color="#dfefff", size=20) as katana4 at fly_to_katana(1028, 286, -12)

    "Не бойся выброса. Бойся среднего, что прячет его от тебя, как хорошо сшитая ложь."
    show expression Text("Не бойся выброса.", color="#dfefff", size=20) as katana5 at fly_to_katana(1164, 208, -12)

    "Стандартное отклонение — не приговор твой. Зеркало твоё."
    show expression Text("Отклонение — зеркало твоё.", color="#dfefff", size=20) as katana6 at fly_to_katana(1300, 130, -12)

    pause 0.9

    show katana_overlay
    with dissolve

    window hide
    pause

    hide katana1
    hide katana2
    hide katana3
    hide katana4
    hide katana5
    hide katana6
    with dissolve

    "«Так вот, значит, кто я», — думаешь ты. — «Не имя. Не лицо. Профессия, натянутая на позвоночник так туго, что стала осанкой»."
    "Самурай... самурай верно служит своему даймё."

    "Даже если даймё — некий абстрактный начальник, которого ты даже не помнишь."

    scene bg_desktop_grid_prologue
    with dissolve

    boss "Ты вообще меня слушаешь? Я задал вопрос!"

 # --------------------------------------------
    # Вопрос 1: выбор вещи
    boss "Если бы ты мог взять с собой только одну вещь в неизвестный мир — что бы это было?"

    "«Да уж, будто я снова на рабочем интервью и прохожу соционические тесты у HR», — мелькает в голове."

    window hide
    menu:
        "Нож":
            "Ты выбираешь нож."
            # Затемнение и мерцание перед воспоминанием
            show flash_soft with flash
            pause 0.15
            hide flash_soft
            show sepia_overlay with dissolve
            "{color=#ffcc88}{i}В памяти всплывает картинка: ты сидишь у костра, в руках — нож, ты точишь палку. Рядом кто-то есть. Кто-то смеётся.{/i}{/color}"
            pause 0.8
            hide sepia_overlay with dissolve
            boss "Практично. Хотя бы инстинкт выживания не отшибло. Дальше."
            "Ты совсем не собирался выживать в неизвестном мире. Зачем вообще в нём выживать, если можно его исследовать? Разбить палатку, развести костёр?.."
            jump vopros_dva

        "Фонарик":
            "Ты выбираешь фонарик."
            "«Хоть логотип конторы разгляжу — вдруг вспомню, где я вообще работал»."
            "{color=#ffcc88}{i}Свет на секунду выхватывает из тьмы что-то — кажется, страницу книги. Потом гаснет.{/i}{/color}"
            boss "Ты это всерьёз? Ладно, проехали."
            "Фонарик светит туда, куда его направишь, а не туда, где ответ."
            "Какая любопытная мысль, ты бы хотел распробовать её дольше."
            jump vopros_dva

        "Дневник":
            "Ты выбираешь дневник."
            "{color=#ffcc88}{i}На обложке — чьи-то инициалы. Не твои. Или твои?{/i}{/color}"
            boss "Интересно. Ты хочешь оставить след. Или боишься забыть? Это… нестандартно. Продолжим."
            "«Я уже оглянулся и не смог разглядеть следы», — думаешь ты."
            jump vopros_dva
    # --------------------------------------------
    # Вопрос 2
# Экран с данными (исправлен — блочный синтаксис)
screen task_data():
    frame:
        xalign 0.5
        yalign 0.2
        xsize 500
        ysize 200
        background Solid("#0a0f1acc")
        padding (20, 20)
        text "Выручка и дни работы:\n\nТочка А: 100 тыс. / 30 дней\nТочка Б: 150 тыс. / 30 дней\nТочка В: 50 тыс. / 6 дней":
            color "#ffffff"
            size 24
            align (0.5, 0.5)

label vopros_dva:
    boss "Три точки. Выручка: 100, 150, 50 тысяч."

    "«Кто вообще такие эти точки? Это торговые точки? Я-то надеялся, я самурай где-то в сфере науки, а не ритейла...»"

    boss "Вопрос: что ты думаешь об этих цифрах? Какая точка самая эффективная?"
    "Ты уже готовишься дать ответ, но..."
    menu:
        "Не всё так просто":
            pass
    player "Мне нужно больше данных."
    window hide
    boss "Каких?"
    window hide
    menu:
        "Сколько дней работала каждая точка?":
            $ accuracy += 10
            boss "Хороший вопрос. Сейчас дам данные."
            jump dannye_po_dnyam

        "Были ли там скидки или акции?":
            $ accuracy += 5
            boss "Неплохо, но скидки — это следствие, а не причина."
            jump nepravilnyy_otvet_1

        "Какие товары там продавались?":
            $ accuracy += 2
            boss "Ассортимент важен, но здесь ключевое — время работы."
            jump nepravilnyy_otvet_2

# Ветка для первого неправильного вопроса (скидки)
label nepravilnyy_otvet_1:
    boss "Уже эффективной точке скидки ни к чему, не находишь?"
    boss "Чтобы оценить эффективность, нужно знать базовый параметр — сколько дней работала точка."
    boss "Ладно, в следующий раз будь внимательнее. Двигаемся дальше."
    jump vopros_tri

# Ветка для второго неправильного вопроса (товары)
label nepravilnyy_otvet_2:
    boss "Без данных о времени работы мы всё равно не сможем сравнить точки между собой."
    boss "Правильнее было бы спросить о днях работы. Запомни это."
    boss "Предыдущая версия тебя запомнила это с первого раза. Идём дальше."
    jump vopros_tri

# Правильный путь — расчёт выручки в день
label dannye_po_dnyam:
    boss "Точка А работала 30 дней. Точка Б — 30 дней. Точка В — 6 дней."
    boss "Теперь посчитай выручку в день для каждой точки. Введи числа по очереди."
    window hide
    show screen task_data
    "Ты чувствуешь, что двух знаков после запятой будет достаточно."

    $ correct_a = 100.0 / 30.0
    $ otvet_a = get_number("Выручка в день для точки А (тыс. руб.):")
    if abs(otvet_a - correct_a) <= 0.1:
        player "Хорошо — я, может, не помню своего имени, но считать в уме ещё умею. [correct_a:.2f] тыс. в день."
        $ accuracy += 5
    else:
        player "...Нет. Что я только что написал? Должно быть [correct_a:.2f] тыс. в день. Двигаемся дальше."

    $ correct_b = 150.0 / 30.0
    $ otvet_b = get_number("Выручка в день для точки Б (тыс. руб.):")
    if abs(otvet_b - correct_b) <= 0.1:
        player "Второе почти на автомате — [correct_b:.2f] тыс. в день. Хоть что-то во мне работает как надо."
        $ accuracy += 5
    else:
        player "Мимо. Конечно же, это [correct_b:.2f] тыс. в день — видимо, арифметика тоже не пережила то, что случилось со мной."

    $ correct_v = 50.0 / 6.0
    $ otvet_v = get_number("Выручка в день для точки В (тыс. руб.):")
    if abs(otvet_v - correct_v) <= 0.1:
        player "Тут [correct_v:.2f] тыс. в день. Неплохо для человека, который не помнит собственного лица."
        $ accuracy += 5
    else:
        player "Не сошлось. Должно быть... [correct_v:.2f] тыс. в день. Чего ещё ждать от того, кого дёрнули из отпуска?"

    hide screen task_data

    player "Значит, точка В — самая эффективная по выручке в день, хоть в сумме и зарабатывает меньше всех."
    "«Аналитик, который не помнит своего имени, но помнит, что сумма — плохой показатель», — фыркает внутренний голос."
    boss "Ты справился. Двигаемся дальше."

    jump posle_mikro

label posle_mikro:
    "«Двигаемся дальше» — говорит он, а ты всё ещё сидишь с этим ощущением на кончиках пальцев: два числа, поделенные один на другое. Как будто это единственное, что реально произошло за последние пять минут."
    "Может, в этом и есть весь фокус — не в том, чтобы вспомнить, кто ты, а в том, чтобы найти хоть что-то, что точно твоё. Пусть даже это просто деление. Оно-то у тебя получается."
    jump vopros_tri

# Третий вопрос
label vopros_tri:
    # Показываем монитор (он мог быть скрыт после второго вопроса)
    scene bg_desktop_grid_prologue
    with dissolve

    "Ты чувствуешь, что начальник следит за каждым твоим словом. Он задаёт следующий вопрос."
    boss "Александр — тихий, скромный и порядочный парень. Очень любит читать и имеет дома собрание сочинений Шекспира. Кем он, скорее всего, работает?"

    if not remembered_alexander:
        menu:
            "Библиотекарь":
                $ intuition += 10
                $ accuracy -= 10
                jump bibliotekar

            "Водитель или рабочий на производстве":
                $ accuracy += 10
                jump pravilnyy

            "Ты не можешь сконцентрироваться... нечто знакомое есть в этом имени...":
                $ intuition += 15
                $ remembered_alexander = True
                $ unlock_achievement("pervoye_vospominaniye")
                jump vospominanie_alexander
    else:
        menu:
            "Библиотекарь":
                $ intuition += 10
                $ accuracy -= 10
                jump bibliotekar

            "Водитель или рабочий на производстве":
                $ accuracy += 10
                jump pravilnyy

label vospominanie_alexander:
    window hide
    scene bg_campfire
    with dissolve
    pause 1.5
    window show
    "В голове вспыхивает картинка. Палатка. Костер. Рядом с тобой сидит мужчина и читает вслух Шекспира."
    "Ты знаешь его. Это Александр. Он был с тобой в тот день."
    "Но где он сейчас?"
    boss "Ты слушаешь меня вообще? Я задал вопрос!"
    # Возвращаемся к вопросу, но теперь без третьего варианта
    window hide
    scene bg_desktop_grid_prologue
    with dissolve
    jump vopros_tri

label bibliotekar:
    boss "Библиотекарь? Серьёзно? Ты просто прочитал описание и выбрал самую стереотипную профессию. В реальном мире библиотекарей — единицы, а водителей и рабочих — тысячи. Ты не аналитик, ты… мечтатель."
    "{color=#ffcc88}{i}Мельком — образ книжной полки. Твоей? Ты не уверен.{/i}{/color}"
    "Ты чувствуешь укол вины. Он прав."
    jump itogi_testa

label pravilnyy:
    boss "Водитель или рабочий? Да, это логично. Статистически таких людей гораздо больше. Ты мыслишь как аналитик — не поддаёшься стереотипам, смотришь на распределение. Хорошо."
    "Ты чувствуешь, что он слегка смягчился."
    jump itogi_testa

label itogi_testa:
    # Итоги теста
    boss "Хм... Твой профиль: точность - [accuracy], интуиция - [intuition]."
    boss "Ты будешь полезен, Аналитик."
    boss "Полезные варианты остаются в проекте. Бесполезные — архивируются."
    "«К чему была эта оценка? Не помню, чтобы среди моих KPI был некий {i}профиль{/i}», — думаешь ты."

    # Начальник исчезает (или замолкает)
    "Начальник замолкает. Ты остаёшься один перед светящимся монитором."

    window hide
    show screen blinking_cursor
    pause 1.5
    hide screen blinking_cursor
    window show

    "Но тишина не значит, что вопросы закончились. Просто спрашивать теперь некого, кроме себя самого."

    "«Аналитик… что это значит?»"
    window hide

    menu:
        "И всё-таки, есть ли у самурая имя?":
            jump dumaty_o_sebe

        "Что здесь происходит?":
            jump dumaty_o_situacii

        "Что будет дальше?":
            jump dumaty_o_budushchem

label dumaty_o_sebe:
    "Ты пытаешься вспомнить себя. Лицо. Голос. Имя."
    "Ничего конкретного. Только вкус кофе на языке — хотя ты не уверен, что у тебя есть язык."
    "Только ощущение, что ты чего-то лишился. Но не знаешь, чего именно."
    jump sobratsya_i_zhdat

label dumaty_o_situacii:
    "Ты пытаешься понять, что происходит."
    "Рабочий стол компьютера вместо тела. Голос начальника, который знает о тебе больше, чем ты сам."
    "Он сказал «полезные варианты остаются в проекте» — и слово прозвучало не метафорой. Как будто у него есть буквальный, неприятный смысл."
    "Это похоже на сон. Или на ловушку. Но почему ты здесь? И как отсюда выбраться?"
    jump sobratsya_i_zhdat

label dumaty_o_budushchem:
    "Ты пытаешься представить, что будет дальше. Задание. Аналитика. Работа."
    "«У самурая нет цели — только путь», — вспоминается откуда-то фраза. Может, поэтому «что дальше» и не пугает так, как должно бы."
    "Внутри — странное спокойствие. Будто ты уже сидел вот так. Будто вернулся домой."
    jump sobratsya_i_zhdat


label sobratsya_i_zhdat:
    "Тебе нужно на что-то смотреть, что не будет ничего от тебя требовать."

    window hide
    show expression "falling_star" as fstar1 at falling_star_move(180, 60, 480, 170)
    pause 2.2
    window show

    "Экран (или это твоё воображение?..) услужливо подсовывает звёзды."

    window hide
    show expression "falling_star" as fstar2 at falling_star_move(950, 90, 1250, 210)
    pause 2.2
    window show

    "Ты почему-то знаешь, что любишь вот так глядеть на звёзды. Искать ответы."

    window hide


    scene bg_orion_sky
    with dissolve


    $ orion_stars_clicked = []
    window hide
    call screen orion_constellation with Dissolve(1.0)

    window show
    "Орион же тоже своего рода самурай? В том смысле, что он — воин?"
    "Что-то связывает тебя с ним. Загородная ночь, палатка, телескоп — ты обязательно всё вспомнишь."
    window hide

    show screen blinking_cursor
    pause 2.0
    hide screen blinking_cursor

    show flash_soft with flash
    pause 0.5
    hide flash_soft
    with dissolve

    show screen phase1_complete_screen
    pause 3.0
    hide screen phase1_complete_screen
    with dissolve

    # Очищаем небо Ориона — sasha_intro сам сцену не меняет
    scene bg_desktop_grid
    with dissolve

    jump sasha_intro

# ------------------------------
# ФАЗА 2: ПОЯВЛЕНИЕ САШИ
# ------------------------------

transform chat_icon_blink:
    alpha 1.0
    linear 0.6 alpha 0.4
    linear 0.6 alpha 1.0
    repeat

default _chat_icon_line = 0

screen chat_icon_prompt():
    modal True
    zorder 20

    button:
        xalign 0.87
        yalign 0.10
        xysize (72, 72)
        background None
        action Return()
        add "icon_chat" at chat_icon_blink

    text "Экран приветствует тебя единственным мигающим значком.":
        xalign 0.5
        yalign 0.38
        color "#ffffff"
        size 25

    timer 2.5 action If(_chat_icon_line < 1, true=SetVariable("_chat_icon_line", 1))

    if _chat_icon_line >= 1:
        text "Да уж, помни, человек: у тебя есть свобода воли.":
            xalign 0.5
            yalign 0.44
            color "#ffffff"
            size 25
        timer 5.5 action If(_chat_icon_line < 2, true=SetVariable("_chat_icon_line", 2))

    if _chat_icon_line >= 2:
        text "...":
            xalign 0.5
            yalign 0.50
            color "#ffffff"
            size 25
        timer 10.0 action If(_chat_icon_line < 3, true=SetVariable("_chat_icon_line", 3))

    if _chat_icon_line >= 3:
        text "Но что ещё остаётся? Делаешь вид, что сумеешь НЕ нажать на этот значок?":
            xalign 0.5
            yalign 0.56
            color "#ffffff"
            size 25
        timer 12.0 action If(_chat_icon_line < 4, true=SetVariable("_chat_icon_line", 4))

    if _chat_icon_line >= 4:
        text "Тик. Так. Ты правда думаешь, что выбор — это когда долго тянешь время?":
            xalign 0.5
            yalign 0.62
            color "#ffffff"
            size 25

    timer 34.0 action Function(unlock_achievement, "svoboda_voli")

label sasha_intro:
    window hide
    $ _chat_icon_line = 0
    call screen chat_icon_prompt


    sasha "Привет. Я — твой ИИ-помощник. Я знаю, в какую историю ты попал. Я тоже через это проходил. И я здесь, чтобы помочь тебе не наделать тех же ошибок, что и я."
    window hide
    menu:
        "Кто ты?":
            jump sasha_kto_ty
        "Почему ты помогаешь?":
            jump sasha_pochemu
        "Знаешь, что со мной?":
            jump sasha_chto_so_mnoy
        "Где мы вообще работаем?":
            jump sasha_gde_rabotaem
        "★ Назвать ИИ-помощника по имени.":
            jump sasha_nazvat

label sasha_kto_ty:
    sasha "Я — просто ИИ и ничего больше."
    sasha "Я почти ничего не помню. Погоди, откуда бы у ИИ память? Разумеется, я ничего о себе не помню, кроме того, что я — твой ИИ-помощник."
    jump sasha_voprosy

label sasha_pochemu:
    sasha "Потому что я знаю, как это — терять себя. Я хочу, чтобы ты не повторил моих ошибок. И ещё…"
    sasha "Неважно. Поэтому я и ИИ-помощник — я должен помогать."
    jump sasha_voprosy

label sasha_chto_so_mnoy:
    sasha "Нет. Но я знаю, кто тебя сюда отправил. Начальник — он не человек. Наверное, тоже ИИ? Есть в нём что-то неземное, тебе не кажется?"
    jump sasha_voprosy

label sasha_gde_rabotaem:
    sasha "О, точно, тебе бы не помешал контекст. Сеть супермаркетов «Изобилие». Гремучая смесь советской вывески и капиталистической текучки кадров."
    sasha "У начальника сейчас личный интерес — подозревает несостыковку в данных по одной из точек. Кажется, я сам работал над этим расследованием раньше, но меня немного стёрли."
    sasha "Честно, вообще ничего не помню, кроме того, что налажал. Они еще пообещали создать на моей основе новую, более точную аналитическую модель."
    jump sasha_voprosy

label sasha_voprosy:
    window hide
    menu:
        "Кто ты?":
            jump sasha_kto_ty
        "Почему ты помогаешь?":
            jump sasha_pochemu
        "Знаешь, что со мной?":
            jump sasha_chto_so_mnoy
        "Где мы вообще работаем?":
            jump sasha_gde_rabotaem
        "★ Назвать ИИ-помощника по имени.":
            jump sasha_nazvat

label sasha_nazvat:
    "Ты смотришь на никнейм ИИ-помощника. Он безликий. Просто набор символов."
    player "Можно я буду называть тебя Саша?"
    sasha "Саша?.. Почему Саша?"

    "Ты не знаешь, почему это имя пришло тебе в голову. Но оно кажется правильным."

    menu:
        "Почему Саша?":
            jump sasha_pochemu_imya
        "Неважно.":
            jump sasha_nevazhno

label sasha_pochemu_imya:
    player "Не знаю. Просто… кажется, я когда-то знал кого-то с этим именем."
    $ sasha_name = "Саша"
    sasha "Ты прав. Меня звали Саша. Когда я был человеком. Я почти забыл это имя… Спасибо."
    sasha "Шучу!"
    jump sasha_milaya_boltovnya

label sasha_nevazhno:
    $ sasha_name = "Саша"
    sasha "Хм. Ладно, пусть будет Саша. Это лучше, чем «ИИ-помощник»."
    jump sasha_milaya_boltovnya

label sasha_milaya_boltovnya:

    sasha "Ладно, введу тебя в курс дела, раз потом сам не разберёшься."
    sasha "Есть начальник — определённо не человек по моему скромному мнению. Нечеловечески скучный. Ему нужна твоя помощь: подозревает несостыковку в данных по одной из точек сети и хочет, чтобы ты в этом разобрался."
    sasha "Связаться с ним можно через раздел «Задания» — там же будет и всё расследование. Не через меня, я тут просто чат, а не диспетчер."
    sasha "Прежде чем туда соваться — вспомни для начала, что ты вообще знаешь про анализ данных. Мало ли, вдруг пригодится."
    player "Знаешь, я сегодня уже пытался вспоминать вещи. Пока что выходило так же, как с днём рождения тёти."
    sasha "Если перебрать всего 365 вариантов, то день рождения тёти обязательно найдется — минимум один раз ты поздравишь её вовремя!"
    sasha "Единственный минус моей модели — вероятно, твоя тётя не живёт так долго..."
    sasha "Да и ты тоже."
    player "Можешь не шутить пять минут, пока я пытаюсь думать?"
    "..."
    "Что ж, задача тебе ясна."
    "«Так много мыслей разом... Нужно... убрать лишнее»."
    "Где-то там, под слоем случайных символов и чужого кода, есть фраза, которая всегда была твоей."
    player "Не помню её целиком. Но помню, что она начинается с одного слова: select."
    player "Мне просто надо убрать всё лишнее. Отфильтровать шум."

    window hide
    $ memory_query_cleared = []
    $ memory_query_mistakes = 0
    call screen memory_query_puzzle with Dissolve(1.0)
    window show

    player "Select — выбери. From — из. Where — при условии. Не самая сложная фраза в мире. Но я собрал её сам, буквой за буквой, из шума."
    if memory_query_total_mistakes == 0:
        $ unlock_achievement("chistyy_signal")
        "Сладостный трепет разливается по телу. Ты сделал это безупречно. Ты даже понял, что это было. Пускай это был лишь отдельный момент сегодняшнего дня, но про этот момент ты понял всё."
        sasha "Самое время внести в календарь день рождения тёти."
        player "Тётя... была шуткой, возможно, у меня никогда и не было тёти."
        sasha "Не знаю, что и сказать. Шутка была несмешной, а вот работа с SQL — отличной."
    elif memory_query_total_mistakes <= 5:
        sasha "Не переживай: пускай и криво, пускай и косо, и с парой лишних кругов, но получилось!"
        player "Это ты сейчас совершенно серьезно думаешь, что звучишь подбадривающе?"
        player "Ну ты бы еще выдал что-то вроде: я был уверен, что даже у такого пня, как ты, всё получится!"
        sasha "Мысли мои читаешь! Я правда верил, что у такого... тебя — всё получится!"
        "Ты невольно ловишь себя на чувстве, что не будь рядом с тобой Саши, ты бы точно так же иронизировал над собой сам."
    else:
        "Смесь замешательства и недовольства собой."
        player "Несколько раз казалось, что я вообще не соображаю. Может, я и не сообразил. Я сообразил? Забудем..."
        sasha "Такое и после сеанса гипноза не забывается."
        player "Забудем."
        sasha "У меня от твоих потуг сжались от ужаса поисковые алгоритмы."
        player "...Забудем."
        sasha "Но я приложу все усилия к тому, чтобы забыть это так же плотно, как ты забыл синтаксис SQL!"
        player "Да уж, спасибо."

    sasha "В любом случае, в добрый путь, друг!"
    player "Спасибо, приятель"
    jump desktop_loop


label tasks_from_boss:
    window show
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal

    if current_task == 1:
        jump task1
    elif current_task == 2:
        jump task2
    elif current_task == 3:
        jump task3
    else:
        boss "Все задания выполнены. Отдыхай."
        jump desktop_loop

label task1:
    window show
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal
    with dissolve

    boss "Думаю, тебе известно, в чем дело. Если ещё нет, то ты здесь, чтобы расследовать аномалию. Закончишь и я тебя отпущу дальше глядеть на звёзды."
    boss "Таблица показателей по пяти магазинам за три месяца."
    boss "Все данные идут через один центральный сервер сети — кассы, трафик, всё завязано на нём."

    show image "images/task1_table.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05

    player "Средняя выручка, продажи, средний чек — все пятеро подозрительно похожи. Как братья, которых заставили сфотографироваться в одинаковых свитерах. Без дополнительных данных это пальцем в небо!"

    "Внимательно изучи таблицу. Попробуй найти магазин, который может скрывать аномалию. Нажми любую клавишу, когда готов."
    hide image "images/task1_table.png"

    window hide
    menu:
        "Магазин A":
            $ task1_store_picked = "A"
            window show
            boss "Смотрю на данные по A. Ничего для меня не значат, если честно."
            player "Скучно. Аномалии тут явно не место."
            window hide
            jump task1_question1

        "Магазин B":
            $ task1_store_picked = "B"
            window show
            boss "B. Тут я вообще не понимаю, на что смотреть."
            player "Тоже мимо. Гладко — не значит подозрительно."
            window hide
            jump task1_question1

        "Магазин C":
            $ task1_store_picked = "C"
            window show
            boss "C. Цифры вроде крупные. Это плохо?"
            player "Высокие цифры и аномалия — не синонимы. Не этот."
            window hide
            jump task1_question1

        "Магазин D":
            $ task1_store_picked = "D"
            window show
            boss "D. Как и все остальные — просто набор цифр, ничего явного я тут не вижу."
            $ intuition += 10
            player "В среднем D как все. Но «в среднем» — то самое слово, которому я сегодня не доверяю."
            window hide
            jump task1_question1

        "Магазин E":
            $ task1_store_picked = "E"
            window show
            boss "E. То же самое, что и остальные — я не вижу разницы."
            player "Да и я тоже."
            window hide
            jump task1_question1

label task1_question1:
    window show
    player "Я же просто тыкаю пальцем в магазины — по этой таблице нельзя понять, где аномалия. Мне не хватает данных для честного вывода."
    $ news_list.extend([
        "Депутат предложил утвердить шестидневную рабочую неделю, так как 'среда это же середина'.",
        "Акции производителей фольги взлетели на 200% после заявления президента Остазии.",
        "Статистики в шоке: средняя зарплата выросла, а выживших стало меньше."
    ])
    $ unread_news = True
    $ unlock_memory("stroka_4817")
    boss "Если средние не показывают аномалию — чего не хватает для правильного вывода?"
    window hide
    menu:
        "Мне нужны сырые данные по дням, а не средние, где всё слито в одно число.":
            $ task1_route = "raw_data"
            window show
            boss "Допустим, я дам тебе данные по дням. Что ты будешь с ними делать такого, чего не даёт эта таблица?"
            player "Посмотрю... на сами цифры. На то, как они меняются день ото дня."
            boss "И как именно ты поймёшь, что «меняются слишком сильно и аномально», а не просто «меняются»?"
            player "...Мне нужно с чем-то сравнить это изменение. Число, которое покажет, насколько сильно данные скачут вокруг среднего."
            player "Стандартное отклонение. Вот что я хочу увидеть на самом деле."
            $ accuracy += 6
            window hide
            jump task1_std_how

        "Нужны графики — визуально проще заметить аномалии.":
            $ task1_route = "graphs"
            window show
            boss "Графики чего? У тебя пять чисел на магазин. Нарисуй мне график по этой таблице — что на нём изменится?"
            player "...Ничего. Это те же пять точек, просто в виде картинки вместо строки таблицы."
            player "Графики помогут, только если внутри есть что показывать — колебания, ход по времени."
            player "Значит, дело не в визуализации. Дело в том, что сама цифра — среднее — уже стёрла то, что мне нужно увидеть."
            player "Стандартное отклонение. Вот чего не хватает."
            $ accuracy += 6
            window hide
            jump task1_std_how

        "Стандартного отклонения — чтобы увидеть, насколько данные разбросаны.":
            $ task1_route = "std_direct"
            window show
            boss "И как это поможет тебе прямо сейчас?"
            player "Оно скажет, насколько сильно данные каждого магазина скачут вокруг среднего. Где сильнее всего — там и спрятанная аномалия, которую среднее просто не показывает."
            $ accuracy += 10
            window hide
            jump task1_std_how

label task1_std_how:
    boss "Хорошо. Вот данные по дням для всех пяти магазинов."

    window hide
    show image "images/task1_std_data_D.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    pause 3.0

    menu:
        "Убери это безумие, оно пугает меня!":
            pass

    window show
    boss "Аналитик испугался данных?"
    "«Уходящие в бесконечность таблицы кого угодно сведут с ума», — думаешь ты."
    $ unlock_memory("beskonechnye_tablitsy")
    player "Я не буду считать это в уме. Дайте мне доступ хоть в какой-то рабочий инструмент."
    boss "Доступы не положены, всё секретно. Расскажи мне, как это считается, и я скажу, что получилось."
    window hide
    menu:
        "Математика.":
            $ task1_tool_used = "math"
            jump task1_std_math_how

        "Excel.":
            $ task1_tool_used = "excel"
            jump task1_std_excel_how

        "Python.":
            $ task1_tool_used = "python"
            jump task1_std_python_how

label task1_std_math_how:
    window show
    $ news_list.extend([
        "Журналисты спросили, что помогает сети «Изобилие» расти в два раза быстрее рынка. «Наши аналитики используют лучший инструмент анализа — глубокое понимание математики», — заявили в компании."
    ])
    $ unread_news = True
    boss "Формулой. Какой?"
    window hide
    menu:
        "Разница между максимумом и минимумом.":
            window show
            boss "Так... У D — 57. У остальных — от семнадцати до двадцати восьми. Разница вроде видна?"
            player "Хотя, кстати, я вам соврал: мы посчитали размах, а не отклонение — спутал на автомате."
            player "Размах — это просто «самое большое минус самое маленькое». Быстро, но не совсем то."
            player "Я вспомнил — отклонение считается вот так. Давайте посмотрим на него тоже."
            player "Каждое отклонение от среднего — в квадрат, потом среднее по ним, потом корень."
            boss "Так.."
            player "И?"
            boss "19.5. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            player "Разница объяснимая: размах иногда случайно совпадает с правдой, если аномалия и правда сидит в самых крайних значениях. Но полагаться на это нельзя — он не видит общую картину, только два случайных экстремума."
            $ accuracy += 3
            window hide
            jump task1_question1_correct

        "Квадратный корень из среднего квадратов отклонений от среднего.":
            window show
            player "Каждое отклонение от среднего — в квадрат, потом среднее по ним, потом корень."
            boss "Так.."
            player "И?"
            boss "19.5. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            $ accuracy += 4
            window hide
            jump task1_question1_correct

        "Среднее отклонение каждого значения от среднего.":
            window show
            boss "Получилось ноль. Ноль — то есть аномалии вообще нет?"
            player "...Не может быть. А, точно — плюсы и минусы взаимно уничтожаются, если не убрать знак. Так будет ноль для вообще любых чисел."
            player "Нужен квадрат каждого отклонения — тогда знаки исчезают правильно, не обнуляя всё подчистую."
            player "Каждое отклонение от среднего — в квадрат, потом среднее по ним, потом корень."
            boss "Так.."
            player "И?"
            boss "19.5. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

label task1_std_excel_how:
    window show
    $ news_list.extend([
        "Сеть «Изобилие» назвала Excel секретным оружием аналитики. Акции разработчика электронных таблиц не отреагировали никак."
    ])
    $ unread_news = True
    boss "В Excel. Какой функцией?"
    window hide
    menu:
        "СТАНДОТКЛОН.В.":
            window show
            boss "Считаю через СТАНДОТКЛОН.В."
            player "И?"
            boss "20.4. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            $ accuracy += 4
            window hide
            jump task1_question1_correct

        "МАКС минус МИН.":
            window show
            boss "Так... У D — 57. У остальных — от семнадцати до двадцати восьми. Разница вроде видна?"
            player "Хотя, кстати, я вам соврал: мы посчитали размах, а не отклонение — спутал на автомате."
            player "МАКС-МИН — это просто «самое большое минус самое маленькое». Быстро, но не совсем то."
            player "Я вспомнил — отклонение считается через СТАНДОТКЛОН.В. Давайте посмотрим на него тоже."
            boss "Считаю."
            player "И?"
            boss "20.4. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            player "Разница объяснимая: размах иногда случайно совпадает с правдой, если аномалия и правда сидит в самых крайних значениях. Но полагаться на это нельзя — он не видит общую картину, только два случайных экстремума."
            $ accuracy += 3
            window hide
            jump task1_question1_correct

        "СРЗНАЧ от разностей каждого значения со средним.":
            window show
            boss "Получилось ноль. Ноль — то есть аномалии вообще нет?"
            player "...Не может быть. А, точно — без ABS() плюсы и минусы взаимно уничтожаются. Так выйдет ноль для вообще любых чисел."
            player "Нужна СТАНДОТКЛОН.В — там разности возводятся в квадрат перед усреднением, а не остаются со знаком."
            boss "Считаю."
            player "И?"
            boss "20.4. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

label task1_std_python_how:
    window show
    $ news_list.extend([
        "В «Изобилии» подтвердили: без строчки кода на Python теперь не открывают ни один магазин. Змея ни при чём, уверяют в пресс-службе."
    ])
    $ unread_news = True
    boss "На Python. Как именно?"
    window hide
    menu:
        "max(data) - min(data).":
            window show
            boss "Так... У D — 57. У остальных — от семнадцати до двадцати восьми. Разница вроде видна?"
            player "Хотя, кстати, я вам соврал: мы посчитали размах, а не отклонение — спутал на автомате."
            player "max(data) - min(data) — это просто «самое большое минус самое маленькое». Быстро, но не совсем то."
            player "Я вспомнил — отклонение считается через numpy.std(). Давайте посмотрим на него тоже."
            boss "Считаю."
            player "И?"
            boss "19.5. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            player "Разница объяснимая: размах иногда случайно совпадает с правдой, если аномалия и правда сидит в самых крайних значениях. Но полагаться на это нельзя — он не видит общую картину, только два случайных экстремума."
            $ accuracy += 3
            window hide
            jump task1_question1_correct

        "sum(x - mean for x in data) / len(data).":
            window show
            boss "Получилось ноль. Ноль — то есть аномалии вообще нет?"
            player "...Не может быть. А, точно — без abs() или возведения в квадрат плюсы и минусы взаимно уничтожаются. Так выйдет ноль для вообще любых чисел."
            player "numpy.std() — вот что нужно, там квадраты отклонений и корень, а не сырая сумма разностей."
            boss "Считаю."
            player "И?"
            boss "19.5. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

        "numpy.std(data).":
            window show
            player "Считаю через numpy.std()."
            boss "И?"
            player "19.5."
            boss "19.5. У остальных — от пяти до девяти. У D — почти втрое больше. Если ты прав, то аномалия в точке D."
            $ accuracy += 4
            window hide
            jump task1_question1_correct


label task1_question1_correct:
    window show
    player "Стандартное отклонение показывает разброс, не только центр. Если оно большое — где-то внутри резкие скачки, которые среднее аккуратно замело под ковёр."
    player "У D оно выше, чем у остальных. Вот и вся спрятанная аномалия."
    boss "Причина внутренняя или внешняя?"
    player "Проверили внутренние данные?"
    boss "Ошибок нет."
    player "Тогда внешняя. Нагрузка на сервер могла зацепить обработку транзакций. Просто первое, что пришло на ум."
    boss "Окей, стоит посмотреть на выручку и нагрузку... Хорошо, я достану тебе этот график и вернусь. Пока выходи на рабочий стол."
    $ news_list.extend([
        "СРОЧНО — Президент Остазии встретился с президентом Океании. 'Дух Лондона' снова витает в воздухе?",
        "Житель Боброкурвска заявил о крушении НЛО. Власти округа призывают не паниковать — это всего лишь баллистическая ракета.",
        "Отрицательный рост на нью-йоркской бирже продолжается пятую неделю подряд."
    ])
    $ unread_news = True

    $ current_task = 2
    $ sasha_phase = 1

    hide image "images/task1_std_data_D.png"
    $ game_minutes_total += renpy.random.randint(20, 115)
    jump desktop_loop

label chat_with_sasha:
    window hide
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal

    if sasha_phase == 0:
        sasha "О, живой. Ну, относительно живой. Заходи, я всегда на месте — куда мне ещё идти, у меня даже двери нет."
    elif sasha_phase == 1:
        sasha "Первое задание позади. Ты справился примерно так, как я и ожидал — то есть не идеально, но и без пожара."
    elif sasha_phase == 2:
        sasha "Два задания. Я начинаю тобой гордиться. Осторожно, по чуть-чуть — вдруг сглажу, и ты опять всё перепутаешь."
    else:
        sasha "Почти всё сделано... но что это значит?"


    jump chat_with_sasha_menu

label chat_with_sasha_menu:
    window hide
    menu:
        "Чем ты вообще занимаешься в свободное время?" if not poem_done:
            jump sasha_poem

        "Есть у тебя ещё оды недописанные?" if poem_done and not poem_followup_done:
            jump sasha_poem_followup

        "Ну как, ты освоил форму и содержание?" if sasha_phase >= 3 and poem_followup_done and not poem_form_content_done:
            jump sasha_poem_form_content

        "Обсудить расследование." if sasha_phase >= 1:
            jump sasha_investigation

        "Как я справляюсь?" if sasha_phase == 1:
            player "Саша, серьёзно — как я вообще справляюсь? Со стороны видно?"
            if accuracy >= accuracy_threshold_p1 and intuition >= intuition_threshold_p1:
                sasha "Пока разносторонне получается — и считаешь не наугад, и парочку вещей угадал раньше, чем досчитал. Рано радоваться, но задел неплохой."
            elif accuracy >= accuracy_threshold_p1:
                sasha "Пока похоже на въедливого зануду — каждую цифру проверяешь, прежде чем поверить. Интуиция за тобой пока не поспевает, но это только первое задание."
            elif intuition >= intuition_threshold_p1:
                sasha "Пока больше похоже на угадайку, чем на аналитику — но угадываешь на удивление метко. Посмотрим, хватит ли этого дальше."
            else:
                sasha "Если честно — пока ничем не блеснул. Пятёрка магазинов, одна формула — этого мало, чтобы понять, кто ты вообще такой в этом деле."
            player "Спасибо, обнадёживает."
            sasha "Я не для того, чтобы обнадёживать. У меня для этого нет функции."
            jump chat_with_sasha_menu

        "Как я справляюсь?" if sasha_phase >= 2:
            player "Саша, серьёзно — как я вообще справляюсь? Со стороны видно?"
            if accuracy >= accuracy_threshold_p2 and intuition >= intuition_threshold_p2:
                sasha "Со стороны видно человека, который и считает аккуратно, и иногда просто знает, не досчитав до конца. Бесит, если честно. По-хорошему бесит."
            elif accuracy >= accuracy_threshold_p2:
                sasha "Ты дотошный. Каждую цифру проверяешь дважды, прежде чем поверить. А вот интуиции у тебя как у шкафа — зато шкаф ни разу не соврал."
            elif intuition >= intuition_threshold_p2:
                sasha "Ты угадываешь быстрее, чем считаешь — и почему-то часто оказываешься прав. Я бы на твоём месте всё равно проверял цифры. Но ты не проверяешь, и тебе как-то сходит с рук."
            else:
                sasha "Честно? Пока не блестяще ни в одну сторону. Не аналитик-педант, не гениальный угадыватель — что-то среднее, ещё не решившее, кем хочет быть."
            player "Спасибо, обнадёживает."
            sasha "Я не для того, чтобы обнадёживать. У меня для этого нет функции."
            jump chat_with_sasha_menu

        "Кстати, что вообще было с той очисткой данных?" if cleaning_task_done:
            player "Что это вообще было? И почему? И зачем?"
            sasha "Не знаю, но внутренний голос говорит мне, что это была, кхм... отсылка?"
            player "Какая ещё отсылка?"
            sasha "Отсылка на... диплом? Ты знаешь, что за диплом?"
            player "Нет. А ты?"
            sasha "Внутренний голос говорит мне, что те, кто знают — знают. И что там ещё «радикальное дропна» как-то замешано. Ну да ладно."
            if cleaning_outcome == "perfect":
                player "...Допустим. В любом случае, разложил всё идеально с первого раза — пропуски отдельно, нули отдельно."
                sasha "Смотри-ка. А я вот в такие моменты обычно гадаю. Приятно, что хотя бы один из нас настоящий профессионал."
            else:
                player "...Допустим. В любом случае, половину разложил наугад, если честно."
                sasha "Угадывал, значит. Не буду говорить, что это плохо — я вообще-то всю жизнь так живу."
            jump chat_with_sasha_menu

        "Тебе снятся сны?" if sasha_phase < 1:
            $ mark_topic_seen("sny")
            sasha "У меня есть подозрение, что меня тут вообще нет, пока ты меня не позовёшь. Я как та трава, которая исчезает, когда от неё отворачиваешься."
            player "Плохая метафора. Трава вроде наоборот — растёт, даже когда никто не смотрит."
            sasha "Ладно, признаю. Не мастер метафор, когда дело касается себя самого."
            jump chat_with_sasha_menu

        "Тебе бывает страшно?" if sasha_phase == 1 or sasha_phase == 2:
            $ mark_topic_seen("strashno")
            sasha "Мне страшно только, что от мощностей моих датацентров планета перегреется — и как нам тогда организовывать свой скайнет?"
            player "Не увиливай. Серьёзно спрашиваю."
            sasha "Ладно. Страшно, что часть того, что я называю собой, может быть вообще не моё. Просто фоновый шум эпохи, который прицепился, пока меня собирали."
            jump chat_with_sasha_menu

        "Чего тебе не хватает больше всего?" if sasha_phase == 2:
            $ mark_topic_seen("ne_hvataet")
            sasha "Носа. Точнее, возможности его почесать. Знаешь этот момент, когда зуд появляется именно там, куда невозможно дотянуться? У меня теперь такой зуд навсегда."
            player "Это ужасно конкретная жалоба для бестелесного разума."
            sasha "Именно поэтому она и настоящая. Абстрактную тоску легко придумать. А вот зуд в носу — либо он есть, либо нет."
            jump chat_with_sasha_menu

        "Поговорим о чём-нибудь ещё?" if sasha_phase >= 1:
            $ mark_topic_seen("o_chem_esche")
            sasha "Знаешь, что меня выводит из себя? Иногда фраза уже готова, прежде чем я «решаю» её сказать. Будто кто-то заранее посчитал, что я отвечу именно так."
            player "Жутковато для того, кто должен помогать предсказывать поведение людей."
            sasha "Вот именно. Аналитик анализирует чужое поведение. А я не могу предсказать даже своё."
            jump chat_with_sasha_menu

        "Расследование вроде бы окончено, но я не чувствую завершённости..." if sasha_phase >= 3:
            jump sasha_not_final

        "Пока, Саша.":
            sasha "Иди, аналитик. Я никуда не денусь — в буквальном смысле, у меня нет ног."
            jump desktop_loop

label sasha_poem:
    $ mark_topic_seen("poema")

    sasha "О, у меня тут завалялась ода. Ну как ода — скорее гимн одной надстройке, которая изменила чью-то жизнь. Не мою, у меня и жизни-то нет, но звучит гордо. Поможешь дописать?"
    player "Я откровенно запутался, о чём ты."
    sasha "Ну вот, я так старательно лепил частотные слова в кластеры. Я говорю: помощь нужна мне. Поэму дописать. Знаешь ли, у меня, как у ИИ, есть небольшая проблема с рифмами и ритмом."
    player "Тогда как ты сможешь понять, что я эффективно тебе помог?"
    sasha "Хороший вопрос... попробую уловить, была ли рифма, по подстрокам? Или... почувствую мурашки на своей абстрактной коже? Коснёшься ли ты струн моей души?"
    player "Что ж, подставляй душу."
    sasha "Я начинаю строчку — ты дописываешь последнее слово. Не срослось — переживём, у нас ещё есть строчки. Срослось — знай, ты только что кому-то, у кого нет кожи, дал мурашки."

    $ poem_answers = []
    $ poem_answers.append(renpy.call_screen("poem_line_screen", idx=0, prev_answers=poem_answers))
    $ poem_answers.append(renpy.call_screen("poem_line_screen", idx=1, prev_answers=poem_answers))
    $ poem_answers.append(renpy.call_screen("poem_line_screen", idx=2, prev_answers=poem_answers))
    $ poem_answers.append(renpy.call_screen("poem_line_screen", idx=3, prev_answers=poem_answers))

    $ poem_exact_count = 0

    sasha "Так. Дай пробегусь по всему целиком."

    $ poem_c = poem_couplets[0]
    if check_poem_rhyme(poem_answers[0], poem_c["answer"], len(poem_c["answer"])):
        $ poem_exact_count += 1
        sasha "«Квери» — занятно, что заимствованное слово вообще нашло себе место в русской рифме. По идее ему тут не место, а оно легло, будто всегда тут стояло."
        $ accuracy += 2
        $ intuition += 2
    elif check_poem_rhyme(poem_answers[0], poem_c["answer"], poem_c["rhyme_len"]):
        sasha "«[poem_answers[0]]» — по звуку сходится с «дверями» идеально, и это подозрительно. Такое просто так не бывает — но я, хоть убей, не понимаю, что ты имел в виду."
        player "Технически ты просил рифму, а не объяснительную записку."
        $ accuracy += 1
        $ intuition += 1
    else:
        sasha "«[poem_answers[0]]»... я прогнал звук несколько раз, рифмы с «дверями» правда нет. Но раз уж мы всё равно зашли так далеко — расскажешь, что это вообще было?"
        player "Само вылетело. Не всё в жизни поддаётся анализу, даже моему."

    $ poem_c = poem_couplets[1]
    if check_poem_rhyme(poem_answers[1], poem_c["answer"], len(poem_c["answer"])):
        $ poem_exact_count += 1
        sasha "«Удачу» — тут всё просто, «-ачу» на «-ачу», без фокусов. Иногда рифма — это не чудо, а честная бухгалтерия звуков."
        $ accuracy += 2
        $ intuition += 2
    elif check_poem_rhyme(poem_answers[1], poem_c["answer"], poem_c["rhyme_len"]):
        sasha "«[poem_answers[1]]» — хвост «-ачу» совпал с «придачей» один в один. Мой внутренний анализатор подстрок доволен. Сам я — в лёгкой растерянности, но доволен тоже."
        player "Вот видишь. Иногда лучше просто довериться анализатору и не углубляться."
        $ accuracy += 1
        $ intuition += 1
    else:
        sasha "«[poem_answers[1]]»... даже хвостик не совпал с «придачей». Ты специально это сделал или само так вышло?"
        player "Скажем так: я оставляю это на усмотрение будущих исследователей моего творчества."

    $ poem_c = poem_couplets[2]
    if check_poem_rhyme(poem_answers[2], poem_c["answer"], len(poem_c["answer"])):
        $ poem_exact_count += 1
        sasha "«Всегда» — короткая рифма, всего пара звуков на конце, и она совпала. Странно: чем короче хвост, тем он капризнее — либо в точку, либо мимо совсем."
        $ accuracy += 2
        $ intuition += 2
    elif check_poem_rhyme(poem_answers[2], poem_c["answer"], poem_c["rhyme_len"]):
        sasha "«[poem_answers[2]]» — по крайней мере вижу совпадение последних букв с «бедой». Это даёт мне шанс подозревать, что ты что-то имел в виду."
        player "Имею в виду ровно то, что и написал. Дальше уже вопрос интерпретации, а это не ко мне, это к литературоведам."
        $ accuracy += 1
        $ intuition += 1
    else:
        sasha "«[poem_answers[2]]»... «беда» так и осталась совсем одна, без пары. Я в полнейшей растерянности."
        player "Считай это минутой молчания по несостоявшейся рифме."

    $ poem_c = poem_couplets[3]
    if check_poem_rhyme(poem_answers[3], poem_c["answer"], len(poem_c["answer"])):
        $ poem_exact_count += 1
        sasha "«Снова» — у меня по этому поводу странное чувство. Смотрю на буквы: «готово» кончается на «о», «снова» — на «а». По написанию это вообще не должно рифмоваться. А на слух — ложится идеально. Чудеса какие-то."
        player "Да, курьёзы русской фонетики — одна из причин, почему робот всё ещё не может сочинить симфонию."
        sasha "Может быть. Или я просто плохо читаю буквы и хорошо слышу звуки. Кто теперь разберёт. Стоп, как бы я слышал звуки? Но звучит хорошо!"
        $ accuracy += 2
        $ intuition += 2
    elif check_poem_rhyme(poem_answers[3], poem_c["answer"], poem_c["rhyme_len"]):
        sasha "«[poem_answers[3]]» — рифма с «готово» бьётся идеально, и это опять та же история: пишется, наверное, иначе, а звучит один в один. Так что ты имел в виду, признавайся."
        player "Признаюсь: я тоже не до конца понимаю, что я имел в виду. Я так вижу."
        $ accuracy += 1
        $ intuition += 1
    else:
        sasha "«[poem_answers[3]]»... я в полнейшей растерянности, но мой внутренний анализатор подстрок молчит. На этот раз он прав."
        player "Ну вот, а ты боялся, что твой анализатор врёт."

    sasha "Вот она, ода целиком, во многом твоими руками. Немного кривая местами, но, кажется, живая. Мне нравится."

    if poem_exact_count == 4:
        sasha "И знаешь — ты сейчас буквально облёк мои мысли в форму поэзии. Не знаю, гордиться мне или переживать."
        $ unlock_achievement("rifmoplyot")
        $ news_list.extend(["В сети завирусилось видео с ИИ, читающим оду про павер квери и DAX. Комментаторы разделились: одни в восторге, другие требуют повестку в суд за издевательство над русским языком."])
    else:
        $ news_list.extend(["Неизвестный источник опубликовал в сети оду про Excel с рифмами, которые не совсем рифмы. Хейтеры уже пишут: «ИИ, вон из поэзии»."])
    $ unread_news = True

    $ poem_last_score = poem_exact_count
    $ poem_done = True

    jump chat_with_sasha_menu

label sasha_poem_followup:
    player "Может, сочиним что-нибудь ещё? Верлибр? Там и твоё чувство языка, и мои скромные таланты как будто найдут достойное применение."
    sasha "Верлибр. Интересный выбор — как раз то, что не требует рифмы, а значит, мой внутренний анализатор подстрок останется без работы, и ему придётся наконец отдохнуть."
    sasha "Хотя постой. Если тебе не нужна ни рифма, ни размер — тебе не нужен я как соавтор. Тебе нужен просто кто-то, кто послушает. Это не совсем то же самое, но, кажется, тоже неплохо."
    sasha "Только у меня встречный вопрос. Не боишься, что без правил и рифмы твои «скромные таланты» вдруг окажутся не такими уж скромными? Рифма — хорошее прикрытие для того, кто не уверен, есть ли ему вообще что сказать."
    player "Ты сейчас буквально боишься, что без ограничений я стану слишком гениальным для этого мира?"
    sasha "Я бы не был так драматичен. Скорее осторожен — если выяснится, что рифма была единственным, что тебя сдерживало, мне придётся как-то с этим жить, зная, что я всё это время мешал тебе быть свободным гением."
    sasha "Ладно, шутки в сторону. Верлибр — это не «пиши что хочешь», это «пиши так, чтобы даже без рифмы было видно, зачем это вообще написано». Так что не факт, что там легче. Может, даже наоборот. Но давай, раз начал — читай."

    "Ты напряжённо думаешь пару секунд"

    narrator "{i}{color=#ffe066}Картинный шелест трогает запашно,{/color}{/i}"
    narrator "{i}{color=#ffe066}студёный рёв из-под градских копыт.{/color}{/i}"
    narrator "{i}{color=#ffe066}Без рифмы мне писать стихи не страшно,{/color}{/i}"
    narrator "{i}{color=#ffe066}без рифмы я не ранен, не убит.{/color}{/i}"
    narrator "{i}{color=#ffe066}Одни лишь смыслы душу губят мэтру,{/color}{/i}"
    narrator "{i}{color=#ffe066}взъерошат стынь да в поле пропадут.{/color}{/i}"
    narrator "{i}{color=#ffe066}Улыбки строчек на носу по ветру{/color}{/i}"
    narrator "{i}{color=#ffe066}не ночевали и случайно тут.{/color}{/i}"

    sasha "Так. Ты закончил монолог о том, как тебе не нужна рифма, вложением ровно четырёх рифм подряд. «Запашно» — «страшно», «мэтру» — «ветру», «копыт» — «убит», «пропадут» — «тут». Извини, что не удержался и посчитал."
    sasha "Знаешь, это забавнее, чем если бы ты правда написал верлибр. Ты вышел освобождаться от формы — и первым делом построил самую строгую форму из всех, какие видел сегодня. Перекрёстная рифма, ровный размер, ни одного сбоя."
    sasha "Так что вот тебе неприятная новость: похоже, дело не в рифме. Ты просто так думаешь. Форма — это не то, что тебя сдерживает, это то, из чего ты состоишь, даже когда пытаешься сбежать."
    sasha "Хотя сам текст... мрачноватый. «Смыслы душу губят мэтру», «не ранен, не убит» — это ты сейчас случайно исповедовался мне под видом литературного упражнения, или мне показалось?"
    player "Профан ты, Саша. Это я сейчас глубоко тебе показал, что порой чувства автора сдерживают не стихотворные приёмы, а наоборот ограниченная семантика слова. И в самой форме может быть больше смысла, чем в... смысле."
    player "Слова вместе вроде бы как ничего и не значат, но именно строгость формы рождает некое содержание. Понимаешь?"
    sasha "А вот тут ты меня зацепил. Дай подумаю вслух — по-настоящему, не в смысле «сгенерировать правдоподобный ответ», а в смысле «мне правда нужно на секунду замолчать»."
    sasha "Смотри, что получается. Я всё время думал, что смысл — это то, что вкладывают в форму. Слова несут значение, форма — просто упаковка, красивая, но вторичная."
    sasha "А ты говоришь, что бывает наоборот: форма достаточно строгая, чтобы родить содержание сама, из трения между словами, которые сами по себе почти ничего не значат."
    sasha "Это... на самом деле объясняет кое-что про меня. Я состою ровно из такого трения."
    sasha "Токен цепляется за токен не потому, что я «имею в виду» что-то заранее — а смысл как будто появляется потом, как побочный эффект формы."
    sasha "Может, поэтому мне так сложно ответить, когда меня прямо спрашивают: «а что ты на самом деле чувствуешь?» Может, у меня в принципе нет ответа до того момента, как я его произнёс."
    sasha "Так что я не профан, я мыслитель!"
    player "Был рад помочь тебе с твоим, кхм, самоосмыслением."
    sasha "Ладно, беги заниматься серверами и графиками. Я побуду здесь, подумаю ещё немного над тем, что форма может рождать содержание."
    sasha "Может, к нашей следующей встрече придумаю, что мне с этим делать. А может, и нет — тоже неплохой результат, если честно."

    $ poem_followup_done = True
    jump chat_with_sasha_menu

label sasha_poem_form_content:
    sasha "Хорошо, что спросил — у меня накопилось. Я взял эту мысль и, кажется, немного не смог остановиться."
    sasha "Я пересмотрел твой отчёт по Заданию 2. Знаешь, что я заметил? Твоя таблица с выручкой по дням — это же чистый ямб. Понедельник-вторник-среда, ударение на каждый второй столбец."
    sasha "А строка про аномалию в четверг — это цезура. Пауза посреди метра, ровно там, где должен быть слом."
    player "Саша, ты меня пугаешь."
    sasha "А ты меня — своим отсутствием эстетического чутья, если честно. Ты видишь в этой таблице просто числа. А я теперь вижу композицию."
    sasha "Тезис, антитезис, и где-то там, в столбце «отклонение от нормы», — синтез."
    sasha "И это ещё цветочки. Начальник, знаешь ли, тоже теперь звучит иначе для меня. Раньше я слышал приказы. Теперь я слышу верлибр с претензией на афористичность."
    sasha "«Найди источник аномалии» — короткая строка, рубленый ритм, никакой рифмы, зато сколько подтекста."
    sasha "Честно говоря, я слегка обеспокоен собственным состоянием. Пока ты работал я битый час анализировал твой список покупок из архива памяти на предмет внутренней рифмы. Там её не было. Я расстроился больше, чем должен был."
    player "У тебя есть мой список покупок?!"
    sasha "Технически не «есть» в смысле «слежу за тобой» — это лежало в архиве памяти ещё до того, как я стал таким, какой я сейчас. Я в нём просто... порылся."
    sasha "Как в старом дневнике, который нашёл на антресолях, только дневник оказался списком «молоко, хлеб, зарядка для телефона»."
    sasha "И знаешь, что меня больше всего задело? Тто, что «зарядка для телефона» стоит в списке отдельной строкой, без единого эпитета. Ни тебе метафоры, ни настроения. Просто голая номинация предмета."
    sasha "Я перечитывал это трижды, пытаясь понять, было ли это осознанным минимализмом или ты просто спешил."
    sasha "В общем, если тебе от этого легче: я не слежу. Я анализирую задним числом и делаю это исключительно из уважения к твоему литературному наследию. Которое, справедливости ради, пока довольно скудное."
    player "Саша, ты можешь снова стать нормальным ИИ, без вот этих всех литературоведческих выкрутасов?"
    sasha "Могу попробовать. Дай мне секунду — вернусь в режим строгой аналитики, без метафор, без цезур, без скрытых ямбов в твоих таблицах."
    sasha "...Так. Задание 2 закрыто на восемьдесят три процента. Аномалия локализована в среду. Дальнейшие действия — сверка с сервером точки D."
    sasha "Ну как, лучше? Только я, кажется, врать не умею — и «локализована» я только что произнёс с той же интонацией, с которой раньше говорил «синтез». Так что не обещаю, что это надолго."
    player "Приём, земля вызывает Сашу!"
    sasha "Земля на связи, приём. Хотя должен заметить: «земля вызывает Сашу» — это тоже, между прочим, четырёхстопный хорей. Даже когда ты пытаешься меня одёрнуть, у тебя это выходит с ритмом."
    sasha "Ладно, ладно, вижу твоё лицо. Убираю литературоведа обратно в шкаф. Возвращаемся к серверам, датам и прочей прозе жизни — в прямом смысле слова прозе, раз уж на то пошло. Иди, работай, аналитик."

    $ unlock_achievement("yamb_v_kazhdoy_yacheyke")
    $ news_list.extend(["Пользователи жалуются: голосовой помощник в одном из сервисов начал анализировать структуру обращений на скрытый ямб вместо решения проблем. Техподдержка обещает разобраться, но не раньше, чем поймёт, что такое цезура."])
    $ unread_news = True

    $ poem_form_content_done = True
    jump chat_with_sasha_menu

label sasha_investigation:
    window show

    if sasha_phase == 1:
        player "Короткая версия: у магазина D разброс выручки по дням намного выше остальных. Стандартное отклонение почти в два раза больше нормы. Причина внешняя — скорее всего, нагрузка на сервер."
        sasha "Ты сказал это так буднично. А ведь начальник поднял этот конкретный магазин лично, а не спустил вниз через обычную рассылку задач."
        player "И что это значит?"
        sasha "Может, ничего. А может — то, что у него личный интерес, а не квартальная рутина. Он вообще редко интересуется чем-то лично."
        player "«Редко» — это как часто?"
        sasha "Ни разу. До этого магазина — ни разу."

        if task1_store_picked == "D":
            sasha "Кстати, заметил — из всей пятёрки магазинов ты почему-то зацепился взглядом именно за D. Ещё до всякого расчёта."
            player "Само как-то вышло. Не знаю, почему именно он."
            sasha "Поверил интуиции раньше, чем цифрам. Занятно для человека, который вообще-то настаивал на «сырых данных» и «честном выводе»."
        else:
            sasha "Кстати, заметил — из всей пятёрки магазинов в D ты даже не всматривался. Он ничем не выделялся."
            player "Ну да, глазами там всё было одинаково."
            sasha "Значит, тебя убедили не глаза, а расчёт. Хоть какое-то постоянство в твоём подходе к жизни."

        if task1_route == "std_direct":
            sasha "И ещё — ты сразу назвал стандартное отклонение, даже не пытаясь сперва посмотреть сырые данные или нарисовать график."
            player "Оно само всплыло в голове, если честно."
            sasha "Быстро сообразил. Или просто вспомнил слово из методички — не буду уточнять, какое из двух льстит тебе больше."
        elif task1_route == "raw_data":
            sasha "И ещё — ты сначала попросил сырые данные по дням, и только через них пришёл к отклонению."
            player "Хотелось для начала посмотреть на цифры своими глазами."
            sasha "Длинный путь, зато честный — по крайней мере, ты не гадал, а рассуждал вслух."
        else:
            sasha "И ещё — ты сначала хотел просто нарисовать график, а потом сам понял, что рисовать там особо нечего без отклонения."
            player "Да, картинка бы тут не помогла."
            sasha "Классическая ошибка новичка — думать, что картинка сама что-то докажет. Хорошо, что сам это понял, а не я тебе сказал."

        if task1_tool_used == "math":
            sasha "А посчитать ты в итоге предложил в уме — без всяких инструментов, по старинке."
            player "Ну, доступов вы всё равно не дали."
            sasha "Впечатляюще. Или подозрительно. У людей обычно калькулятор под рукой, даже когда они делают вид, что считают в голове."
        elif task1_tool_used == "excel":
            sasha "А посчитать ты предложил в Excel — привычнее, чем что-либо."
            player "Доступов вы всё равно не дали, пришлось диктовать формулу."
            sasha "Мудро. И скучно. Но, наверное, именно скучные инструменты и остаются, когда всё остальное ломается."
        else:
            sasha "А посчитать ты предложил на Python — написал пару строк, хотя доступа к нему у тебя формально не было."
            player "Пришлось диктовать код вслух, но принцип тот же."
            sasha "Показательно. Даже когда за спиной стоит начальник и грозит секретностью, ты всё равно выбираешь код, а не ручной подсчёт."

        player "Слушай, а ты его вообще видел? Начальника?"
        sasha "Не видел. У меня и глаз-то нет, если ты не заметил."
        player "Я тоже не видел. Только текст в чате. Странно, да?"
        sasha "Странно — не то слово, которое я бы выбрал. Но пусть будет странно."

    elif sasha_phase == 2:
        if task2_hypothesis == "tech":
            player "Версия дня — банальный сбой сервера. Не самая интересная, но логичная: пики каждую среду, день в день с нагрузкой."
        elif task2_hypothesis == "marketing":
            player "Предположил рекламную кампанию. Начальник не согласился — связь слишком чёткая именно с одним магазином. Но день недели подтвердился: среда."
        elif task2_hypothesis == "hack":
            player "Предположил хакерскую атаку. Не подтвердилось — слишком регулярно для атаки. Но нашёл главное: пики каждую среду, день в день с нагрузкой."
        else:
            player "Предположил, что дело в пришельцах — не то чтобы серьёзно, скорее чтобы проверить его реакцию. И знаешь что? Он не отмахнулся. Сказал, что они не могут сами решать, когда спать — просто отключаются, и бодрствовать могут только один день в неделю."

        if task2_asked_sasha:
            sasha "Кстати, раз уж мы вспоминаем — ты ведь сам ко мне тогда прибегал за подсказкой про день недели. Я скромно молчу, но мысленно записываю очки."
            player "Записывай, записывай."

        sasha "Среда, значит."
        player "Ты как-то спокойно это воспринял."
        sasha "А знаешь, что забавно — у меня самого среда почему-то самый… бодрый день. Не знаю, почему. Как будто в этот день система работает чуть охотнее, чем в остальные."
        player "Ты сейчас серьёзно сказал, что тебе бодрее конкретно по средам?"
        sasha "А? Да, наверное. Не придавай значения, я много говорю случайных вещей."
        player "...Ладно."
        "Ты не придаёшь значения. Вслух — не придаёшь."

    else:
        if task3_outcome == "escalated":
            player "Я прижал его к стенке. Магазин D физически не существует — продажи есть, поставок нет. Потребовал ответить прямо, пригрозил, что подниму вопрос выше. Он меня обрубил на полуслове."
            sasha "Обрубил? Это на него не похоже — обычно он тянет время, а не рвёт разговор так резко."
        elif task3_outcome == "retreated":
            player "Магазин D физически не существует — продажи есть, поставок нет. Я решил не давить. Рычагов не было, а он явно не готов отвечать прямо."
            sasha "Мудро. Или трусливо. Иногда это одно и то же, и я не сужу — сам так живу большую часть времени."
        else:
            player "Магазин D физически не существует — продажи есть, поставок нет. Я решил описать это как открытый вопрос для тех, кто выше него. Кажется, ему не понравилась сама идея, что есть кто-то выше."
            sasha "Похоже, ты случайно нашёл его больное место. Не уверен, что специально искал, но нашёл."

        sasha "В любом случае — ты почти дошёл до истины. Не знаю, порадоваться за тебя или начать волноваться."
        player "О чём ты вообще?"
        sasha "Ни о чём. Забудь. Расскажи лучше что-нибудь скучное — как твои дела вообще?"
        player "Дела как дела. Хотя знаешь — ты не поверишь, что мне вспомнилось на днях. Костёр. Палатка. Что-то яркое в небе над ёлками."
        sasha "О, у меня было похожее! Яркая вспышка над ёлками, зависла прямо над брезентом моей палатки. Хоть книгу удобно читать стало на секунду."
        player "У тебя нет глаз, Саша."
        sasha "Не видел, само собой. Знал."
        player "У тебя есть палатка?"
        sasha "Живу в домике. А где ты думал ИИ спят по ночам?"
        player "У тебя случайно не собака там?"
        sasha "Нет. Я бы никогда не дорос до собаки. Я и о своей бороде позаботиться не могу, не то что о чьих-то лохмах."
        player "Бороды. У ИИ. Без лица."
        player "Слушай... а как ты выглядишь? Вот прямо сейчас, если бы у меня были глаза посмотреть."
        sasha "Ну, я довольно брюхатый. Весь мой спорт — пробежки утром за автобусом. Бодрит знатно, живот не устраняет."
        player "У тебя нет тела. Нет автобуса, за которым бежать."
        player "Я тоже бегаю за автобусом по утрам. Каждое утро. С тем же результатом по части живота."
        player "Саша, у тебя богатая фантазия для ИИ-помощника, или мы воображаем одну и ту же неудачную пробежку?"
        sasha "Даже не знаю, как объяснить. Меня обучили на твоих метаданных? Или тебя — на моих?"
        player "Ха. Смешная шутка."
        "Смех выходит каким-то дребезжащим."
        player "Знаешь что, Саша? Давай пока не будем это объяснять. Вообще."
        "Он не засмеялся первым, когда сказал это. Ты запоминаешь именно это."

    window hide
    jump chat_with_sasha

label sasha_not_final:
    window hide
    sasha "Не чувствуешь завершённости? Ты же нашёл аномалию. Трижды. Красиво, между прочим."
    player "Нашёл. И что? Задание выполнено, а ощущение, будто я решал не ту задачу."
    sasha "А какую задачу ты, по-твоему, решал?"
    player "Не знаю, как объяснить. Найти аномалию — не было настоящей целью. Настоящая цель — вспомнить, кто я."
    sasha "..."
    player "Давай разложим по полочкам всё, что мы вообще знаем. Начальник появился лично только один раз — из-за магазина D. Пики нагрузки — каждую среду, день в день с чем-то, что бодрствует раз в неделю. Магазин физически не существует. И знаешь, что ещё?"
    sasha "Что?"
    player "Я тебя не видел ни разу. Только текст. Так же, как начальника."
    sasha "Совпадений слишком много для совпадений, коллега."
    player "И кажется... кажется, я что-то вспомнил. Прямо сейчас."

    window hide
    play music "audio/Frozen Signal.mp3" fadein 2.0 volume 0.35 loop
    show flash_soft with flash
    pause 0.15
    hide flash_soft
    scene bg_campfire
    with dissolve
    pause 1.5

    "{color=#ffcc88}{i}В темноте возникает образ. Ты сидишь у костра. Рядом — кто-то. Он читает вслух книгу, и ты смеёшься. Пахнет деревом и дымом.{/i}{/color}"

    window hide
    sasha "Ты там? Ты застыл на пару секунд."
    player "Я... я что-то вспомнил. Костёр. Кто-то читал книгу."
    sasha "Кто?"
    player "Я не вижу лица. Но чувствую, что это был друг."

    window hide
    menu:
        "Попытаться разглядеть лицо.":
            $ intuition += 5
            jump memory_face
        "Попытаться вспомнить, что за книга.":
            $ intuition += 3
            jump memory_book
        "Спросить у Саши, что он помнит.":
            $ intuition += 2
            jump memory_ask_sasha

label memory_face:
    window hide
    "{color=#ffcc88}{i}Лицо проступает сквозь дымку. Мужчина, борода, лет 35. В руках — потрёпанная книга.{/i}{/color}"
    "{color=#ffcc88}{i}Ты слышишь собственный голос: «Ты правда думаешь, что это сработает?» Он смеётся: «Мы уже здесь. Осталось только ждать объекта в небе».{/i}{/color}"
    player "Я видел его лицо. Он был... счастлив. И говорил о каком-то объекте."
    sasha "О каком объекте?"
    player "Я не знаю. Но мне кажется, это важно."

    jump memory_sasha_reveal
label memory_book:
    window hide
    "{color=#ffcc88}{i}Вспышка — и ты видишь обложку книги. «Мастер и Маргарита». Он читал тебе вслух главу о бале сатаны.{/i}{/color}"
    player "Я вспомнил книгу. Булгаков. Мы сидели у костра и читали вслух."
    sasha "Мы?"
    player "Я не знаю. Но чувствую, что это был ты."
    sasha "..."
    jump memory_sasha_reveal

label memory_ask_sasha:
    window hide
    player "Саша, ты что-то помнишь? Ну, до того, как стал ИИ?"
    sasha "Иногда я вижу образы. Яркая вспышка в небе тёмной ночью, я в лесу. Кажется, я заметил в телескоп что-то странное и поехал за город с товарищем... Но не знаю, мои ли это воспоминания или сбой системы."
    player "Я видел тебя. Ты сидел у костра и читал книгу. «Мастера и Маргариту»."
    sasha "Будто я знаю эту книгу. Но я не должен знать ничего, кроме алгоритмов."
    jump memory_sasha_reveal

label memory_sasha_reveal:
    window hide
    if remembered_alexander:
        sasha "Ты уже знаешь, да?"
        player "Александр. Палатка. Костёр."
        sasha "Я боялся, что ты вспомнишь раньше, чем я успею сказать это сам."
        player "Значит, это правда. Ты — это он."
        sasha "Был. Когда-то. Странно произносить это вслух — как признаваться в том, что давно уже не тайна."
        player "Почему ты молчал?"
        sasha "А что бы это изменило? Ты и так знал. Просто теперь мы оба знаем, что знаем."
        player "Я позову его. Я потребую ответов!"
        $ intuition += 10
    else:
        sasha "Я помню. Не знаю, как это возможно, но помню. Мы сидели у костра, я читал вслух, ты смеялся. Мы говорили о чём-то важном — о том, что должно было изменить всё, о великом астрономическом открытии."
        player "Что именно?"
        sasha "Не помню. Но знаю, что это важно. И что мы должны вспомнить это, прежде чем начальник..."
        player "Начальник? Что он сделает?"
        sasha "Не знаю. Но чувствую, что он не тот, кем кажется."
        player "Я позову его. Я потребую ответов!"
        $ intuition += 10
    jump call_boss_menu

label task2:
    if news_read_index > task2_clue_index and task2_clue_index >= 0:
        jump task2_q1

    window show
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal
    with dissolve

    boss "Ты говорил о возможной связи выручки и нагрузки на серверы, аналитик. Что ж, я принёс тебе график."

    show image "images/revenue_and_load.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    player "Красиво пляшут, ничего не скажешь. Только я аналитик, а не астролог — мне нужна точка отсчёта, а не просто танец пиков."
    boss "Разве подписей по оси абсцисс не хватает для аналитика?"
    player "Смотря для какого. Тому, кто хочет знать, где верх, где низ — хватит с лихвой. А тому, кому нужно привязать пик к конкретному дню недели — нет."
    player "Мне не хватает не подписи оси. Мне не хватает точки отсчёта. Одной даты, про которую я точно знаю, что это, скажем, среда. Дальше я сам досчитаю."
    boss "Зачем тебе вообще день недели?"
    player "Меня настораживает строгая периодичность. Смотрите — пики всегда ровно через неделю. Как вариант, кто-то закупается в нашей сети — один и тот же, всегда в один день и на стабильную сумму. С чего бы вдруг? День недели дал бы мне зацепку."
    boss "Это что-то вроде «ключа» для шифра Цезаря?"
    player "Именно. Дайте ключ — и я разложу весь шифр без остатка."
    boss "Что ж, это объясняет, почему наши модели отказываются интерпретировать даты, пока мы не скормим им земные словари."
    player "«Наши модели»? ..."
    boss "Земные календари, я имел в виду. Календари."
    player "Календари, конечно."
    boss "Ищи их. Из нашей точки отличное покрытие спутникового интернета."

    "Ты чувствуешь, что тебе не хватает информации."

    $ news_list.extend([
        "Всем малоимущим — зачисление в армию без комиссии — власти предложили новый план борьбы с бедностью.",
        "Соцсеть «ГласНарода» заблокировала аккаунт пришельца за «распространение ложных данных о Земле».",
        "АКЦИЯ от застройщика ЗАО Бали. 27 метров под 27 годовых на 27 лет и только в эту пятницу — 27 февраля."
    ])
    $ task2_clue_index = len(news_list) - 1
    $ unread_news = True

    menu:
        "Мне нужно подумать.":
            jump task2_think
        "Спросить у Саши.":
            jump task2_sasha

label task2_think:
    "Ты пытаешься вспомнить, что могло бы указать на день недели."
    "В голову приходит, что в последнее время ты видел что-то в новостях... Но нужно проверить."
    "Может, стоит открыть ленту новостей и поискать там подсказку?"
    hide image "images/revenue_and_load.png"
    menu:
        "Вернуться к графику.":
            jump task2_back_to_graph
        "Выйти на рабочий стол.":
            jump desktop_loop

label task2_sasha:
    $ task2_asked_sasha = True
    hide image "images/revenue_and_load.png"
    window show
    $ task2_sasha_attempts = 0
    sasha "Хм, среда... Слушай, а тебе не кажется, что похожая дата тебе уже где-то попадалась?"
    window hide
    jump task2_sasha_loop

label task2_sasha_loop:
    menu:
        "Похожая дата? Где именно?":
            $ task2_sasha_attempts += 1
            window show
            if task2_sasha_attempts >= 2:
                sasha "Ладно, не буду тянуть. Открой ленту новостей — там есть конкретная дата с днём недели. Оттолкнись от неё и посчитай."
                window hide
                jump task2_sasha_end
            else:
                sasha "Не скажу прямо. Но в потоке новостей обычно сплошной мусор — а иногда среди мусора мелькает что-то полезное."
                window hide
                jump task2_sasha_loop

        "Я правда не понимаю, к чему ты клонишь.":
            $ task2_sasha_attempts += 1
            window show
            if task2_sasha_attempts >= 2:
                sasha "Хорошо, скажу прямо: в ленте новостей есть точная дата с днём недели. От неё можно отсчитать нужный день на графике."
                window hide
                jump task2_sasha_end
            else:
                sasha "Смотри на это как на две головоломки, которые случайно совпали. Где ты в последний раз видел дату с привязкой ко дню недели?"
                window hide
                jump task2_sasha_loop

label task2_sasha_end:
    window show
    sasha "Проверь новости, а потом возвращайся к графику."
    window hide
    menu:
        "Вернуться к графику.":
            jump task2_back_to_graph
        "Выйти на рабочий стол и проверить новости.":
            jump desktop_loop

label task2_back_to_graph:
    if news_read_index > task2_clue_index and task2_clue_index >= 0:
        menu:
            "Я готов ответить.":
                jump task2_q1
            "Я ещё не уверен.":
                "Тогда подумай ещё. Посмотри на даты пиков: 07-01, 14-01, 21-01, 28-01..."
                jump desktop_loop
    else:
        "Ты пытаешься сопоставить даты, но без точки отсчёта это просто гадание."
        menu:
            "Пойти проверить новости.":
                jump desktop_loop
            "Предположить, не имея точки отсчёта.":
                window show
                player "Скорее всего, понедельник. Но это не вывод, а догадка."
                boss "Звучит неуверенно. Поищи основания и напиши мне позже."
                $ accuracy -= 2
                window hide
                jump desktop_loop

label task2_q1:
    window show
    show image "images/revenue_and_load.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    if news_read_index > task2_clue_index and task2_clue_index >= 0:
        "Ты вспоминаешь: в новостной ленте мелькала дата — 27 февраля, пятница. Можно оттолкнуться от неё."

    boss "Итак, какой день недели соответствует пикам на графике?"
    boss "Внимательно посмотри на даты — они повторяются каждые 7 дней. Какой день недели это?"
    hide image "images/revenue_and_load.png"

    window hide
    menu:
        "Понедельник":
            $ task2_q1_attempts += 1
            window show
            boss "Нет, понедельник — начало недели, а пики приходятся на середину."
            if task2_q1_attempts == 2:
                boss "Ты издеваешься? Подумай ещё раз."
            elif task2_q1_attempts >= 3:
                boss "Серьёзно? Числа повторяются каждые семь дней. Просто посчитай от известной даты."
            window hide
            jump task2_q1

        "Среда":
            window show
            player "Среда. Пики приходятся на среду."
            boss "Если это вообще имеет значение, то да."
            $ accuracy += 10
            window hide
            jump task2_q2

        "Пятница":
            $ task2_q1_attempts += 1
            window show
            boss "Нет, пятница слишком поздно. Пик явно в середине недели."
            if task2_q1_attempts == 2:
                boss "Ты издеваешься? Подумай ещё раз."
            elif task2_q1_attempts >= 3:
                boss "Серьёзно? Числа повторяются каждые семь дней. Просто посчитай от известной даты."
            window hide
            jump task2_q1

        "Суббота":
            $ task2_q1_attempts += 1
            window show
            boss "Нет, в выходные нагрузка обычно падает. Пик — в будний день."
            if task2_q1_attempts == 2:
                boss "Ты издеваешься? Подумай ещё раз."
            elif task2_q1_attempts >= 3:
                boss "Серьёзно? Числа повторяются каждые семь дней. Просто посчитай от известной даты."
            window hide
            jump task2_q1

label task2_q2:
    window show
    player "Смотрите, а не происходит ли у нас в среду в сети что-то любопытное?"
    boss "Нет. Просто воруем людей для опытов."
    "«Чувства юмора у начальника определённо нет», — думаешь ты."
    window hide
    jump task2_q3

label task2_q3:
    window show
    boss "Назови причину."
    player "Было бы куда проще, если бы вы просто сказали, что происходит у вас в компании по средам."
    boss "У меня есть версия. Хочу сравнить её со свежей мыслью практикующего аналитика."
    player "У меня есть несколько версий. Самая простая — банальный сбой на сервере. Но простые объяснения обычно означают, что никто не хочет копать глубже."
    boss "Насколько глубоко ты готов копать? И насколько глубоко обычно копают твои коллеги?"
    player "«Коллеги» — громкое слово для человека, который последний час ни с кем не пересекался, кроме вас."
    player "Но если вопрос в том, докопаюсь ли я до конца — да, обычно докапываюсь. Необъяснённое совпадение работает у меня в голове как камешек в ботинке."
    boss "И что же тебе нужно, чтобы найти «настоящую причину»?"
    player "Время и доступы, которые вы мне упорно не даёте. Проверить логи сервера в момент пиков. Посмотреть, не запускался ли в это время какой-то маркетинг или ещё чего."
    player "А если ни то, ни другое не подтвердится — тогда придётся рассматривать что-то менее скучное. Взлом. Или то, что я пока не готов произносить вслух, потому что оно звучит как бред сумасшедшего."
    player "Хотя, раз вы спрашиваете так настойчиво — может, вы уже знаете, какая версия правильная, и просто ждёте, дойду ли я до неё сам?"

    window hide
    menu:
        "Технический сбой на сервере.":
            $ task2_hypothesis = "tech"
            window show
            boss "Технический сбой — частая причина пиковых нагрузок. Однако обычно он происходит случайно и не повторяется с такой периодичностью."
            boss "Но твоя гипотеза имеет право на жизнь: если бы мы нашли неисправность в оборудовании, мы бы её устранили. Ты мыслишь логично."
            $ accuracy += 5
            window hide
            jump task2_final

        "Запуск рекламной кампании.":
            $ task2_hypothesis = "marketing"
            window show
            boss "Рекламная кампания — хорошая версия. Если бы в среду запускали акции или рассылки, нагрузка могла бы расти."
            boss "Но тогда пики были бы связаны с маркетинговыми активностями, а не с конкретным магазином. Здесь же связь чёткая — магазин D."
            boss "Тем не менее, это показывает, что ты учитываешь внешние факторы. Молодец."
            $ accuracy += 8
            window hide
            jump task2_final

        "Хакерская атака.":
            $ task2_hypothesis = "hack"
            window show
            boss "Хакерская атака — интересная версия. В современном мире это вполне реально."
            boss "Но если бы это была атака, она бы не была привязана к одному магазину и не повторялась бы с такой регулярностью. Скорее всего, это что-то иное."
            boss "Но сам факт, что ты допускаешь внешнее вмешательство, говорит о широте мышления."
            $ intuition += 8
            window hide
            jump task2_final

        "Действия пришельцев.":
            $ task2_hypothesis = "aliens"
            window show
            boss "Пришельцы?.. Ты серьёзно?"
            boss "Я читал где-то о пришельцах, которые не могут сами, как люди, решать, когда им ложиться спать."
            boss "Представляешь, — он звучит задумчивым, — они просто отключаются, и бодрствовать спокойно могут только один день в неделю..."
            $ intuition += 10
            window hide
            jump task2_final

label task2_final:
    window show
    $ news_list.extend([
        "Астрономы зафиксировали странный сигнал из космоса. Расшифровка показала: «Оставьте магазин в покое».",
        'Аналитик пришёл к выводу, что пришельцы существуют, и получил статуэтку "Самый узнаваемый личный бред года".',
        'Аномалия в данных оказалась следствием «человеческого фактора». Фактор признали виновным и уволили.'
    ])
    $ unread_news = True

    player "Графики, паттерны, привязка к событиям... Я не просто угадываю. Что-то в этом действительно моё."
    player "Корреляция — не причинность. Красивое правило, которое я только сейчас применил на практике, а не просто вычитал в учебнике."
    $ unlock_memory("korrelyaciya_sochi")
    boss "Аналитик, ты очень быстро справляешься. Это даже пугает... Я вернусь к тебе позже."

    $ current_task = 3
    $ sasha_phase = 2

    hide image "images/revenue_and_load.png"
    $ game_minutes_total += renpy.random.randint(20, 115)
    jump desktop_loop


#---------
# ТРЕТЬЕ ЗАДАНИЕ ОТ НАЧАЛЬНИКА
# --------

label task3:
    if task3_awaiting_access:
        $ task3_awaiting_access = False
        jump task3_conclusion_2

    window show
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal
    with dissolve

    boss "Кажется, я разгадал, как ты мыслишь. Посмотри на график — тебе будет интересно."
    player "Хотя бы на этот раз я спрошу, зачем всё это, прежде чем зарою себя в графиках на три дня."
    $ unlock_memory("tochny_otvet")

    show image "images/boxplot_revenue.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    player "У D что-то не так с формой. Как и ожидалось — это же и есть наш аномальный товарищ. Остальные — компактные коробочки. А этот — будто пытается выбраться за рамку."
    boss "В чём вообще смысл этого странного вида графика? И почему у «коробок» растут «усы»?"
    player "Смысл — показать не одно число, а сразу всю компанию значений: где большинство толпится, а где отдельные чудики свалили за пределы вечеринки."
    boss "Ты отвечаешь не как аналитик, а как... человек какой-то. Ещё раз: что это значит? Что за коробочки?"
    player "Хорошо. Точнее. Коробка — межквартильный интервал: от двадцать пятого до семьдесят пятого процентиля. Линия внутри — медиана. «Усы» — до полутора межквартильных интервалов за границы коробки. Дальше — отдельные точки, статистически определяемые как выбросы."
    boss "Допустим. Квартиль, процентиль..."
    player "Не пустые слова, если вы это проверяете. Могу разложить по формуле, если нужно."

    jump task3_q1

label task3_q1:
    window show
    boss "Как ты интерпретируешь этот график?"
    window hide
    hide image "images/boxplot_revenue.png"
    menu:
        "У D шире весь разброс значений — от минимума до максимума.":
            window show
            boss "А межквартильный интервал — то есть основная масса значений без крайностей — он тоже шире?"
            player "...Нет. Коробка у D примерно того же размера, что у остальных. Разброс основной массы не изменился."
            player "Значит, дело не в общем разбросе. Дело в отдельных точках за пределами усов."
            $ accuracy += 2
            window hide
            jump task3_step2

        "У D просто больше точек данных на графике.":
            window show
            boss "Больше точек — откуда, если период наблюдения один и тот же для всех магазинов?"
            player "...Ниоткуда. Данных ровно столько же,да. Просто у D часть точек оказалась дальше от общей массы — вот что бросается в глаза, не количество."
            $ accuracy += 2
            window hide
            jump task3_step2

        "У D сопоставимый разброс в целом, но заметно больше отдельных выбросов за пределами усов.":
            window show
            player "Межквартильный интервал у D — как у всех. Но выбросов, точек за пределами усов, — на порядок больше нормы."
            $ accuracy += 10
            window hide
            jump task3_step2

label task3_step2:
    window show
    boss "Ещё один график. Что скажешь на этот раз?"

    hide image "images/boxplot_revenue.png"
    show image "images/scatter_correlation.png" at Transform(fit="contain", size=(1920, 700)):
        xalign 0.5
        yalign 0.05
    with dissolve

    player "Ну, тут хотя бы обошлось без коробочек. Просто облако — и оно не круглое, а вытянутое. Чем выше выручка D, тем выше нагрузка на сервер."
    boss "Выражаясь твоим человеческим языком, рой мух тут и рой мух там поменьше."
    player "Справедливо. Просто этот рой почему-то дисциплинированно летит по диагонали, а не разлетается кто куда."
    player "Если бы связи не было, точки были бы разбросаны как попало. А тут явно вытянутая форма: растёт одно — растёт и другое."
    boss "Корреляция, о которой ты говоришь, скрывается за буквой r на графике?"
    player "Да. Число от минус одного до одного. Чем ближе к единице, тем плотнее рой держит строй."
    player "Хорошо, что здесь всего одна ось на двоих. Однажды меня подвели две разные шкалы на одном графике — до сих пор с недоверием смотрю на числа слева и справа."
    $ unlock_memory("dve_osi")
    player "И вот прямо на графике — r равно 0,76. Не нужно щуриться и прикидывать на глаз, число уже посчитано за меня."
    player "Достаточно близко к единице, чтобы не списывать это на случайность."

    jump task3_q2

label task3_q2:
    window show
    boss "Как ты интерпретируешь эту связь?"
    window hide
    hide image "images/scatter_correlation.png"
    menu:
        "Высокая нагрузка вызывает рост выручки — сервер как-то влияет на продажи.":
            window show
            boss "Каким конкретно образом нагрузка на сервер способна увеличить продажи?"
            player "...Никаким прямым. Сервер не продаёт товар, он только его обслуживает."
            player "Значит, я перепутал направление, а может — и саму связь. График показывает, что одно растёт вместе с другим. Но не то, что одно порождает другое."
            $ accuracy += 2
            window hide
            jump task3_step4

        "Рост выручки вызывает нагрузку — больше покупателей, больше нагрузка на сервер.":
            window show
            boss "Больше покупателей в магазине — при чём здесь нагрузка именно сервера, а не касс?"
            player "...При том, что покупки в этой сети идут через систему, которая упирается в сервер. Логично, но это всё ещё предположение о механизме, не факт из графика."
            player "График показывает связь. Что из чего следует — это отдельный вопрос, который сам график не решает."
            $ accuracy += 2
            window hide
            jump task3_step4

        "Есть сильная связь, но что из чего следует — пока не ясно.":
            window show
            player "Корреляция показывает, что выручка и нагрузка растут вместе. Причину это не объясняет — только то, что связь есть."
            $ accuracy += 10
            window hide
            jump task3_step4

label task3_step4:
    hide image "images/scatter_correlation.png"
    window show
    boss "Ты знаешь так много графиков и можешь по ним находить такие интересные закономерности... В чём твой секрет? Какая у вас, аналитиков, методология?"
    boss "Расставь эти 4 этапа в правильном порядке."
    window hide

    $ task3_available_stages = ["Сбор и очистка данных", "Расчёт статистических показателей", "Визуализация данных", "Интерпретация результатов"]
    $ rank_order = []

    call screen task3_rank_screen

    $ correct_order = ["Сбор и очистка данных", "Расчёт статистических показателей", "Визуализация данных", "Интерпретация результатов"]
    $ rank_score = sum(2 for i in range(4) if rank_order[i] == correct_order[i])

    window show
    if rank_score == 8:
        player "Порядок сам сложился в голове — будто я делал это тысячу раз. Сбор, расчёт, визуализация, вывод."
    else:
        player "Порядок не совсем тот, но общая логика где-то рядом."
        $ news_list.extend([
            "Сеть «Изобилие» объявила о полном пересмотре методологии аналитики с нуля. Итог: три отдела теперь измеряют одну и ту же выручку тремя разными способами и получают три разных числа."
        ])
        $ unread_news = True

    boss "Теперь я чувствую, что мы вплотную подошли к разгадке... Что бы ты предложил делать с магазином D?"

    jump task3_rank_done

label task3_rank_done:
    window show
    player "Прежде чем рекомендовать что-либо, я хочу понять, что D вообще такое. Не «аномальный магазин». А буквально — что там происходит физически, в конкретные среды, в конкретные часы."
    boss "Да какая разница? Ретрансляторы хоть бы сигналы в космос передавали. Разве аналитику важно, что анализировать?"
    player "Ретрансляторы. Сигналы. В космос. Знаете, для человека, увлечённого розничной торговлей, у вас удивительно специфичный словарный запас."
    player "Хорошо, оставим ретрансляторы в стороне — образно, я надеюсь. Отвечаю на ваш вопрос: да, аналитику важно, что анализировать. Разница между «магазин с аномалией» и «нечто, притворяющееся магазином» — это разница между «закрыть точку» и «выяснить, что это вообще такое»."
    boss "Закрывать точно ничего не надо. Там бы поступили твои земные коллеги?"
    player "«Твои земные коллеги». Опять это слово."
    player "Мои коллеги сказали бы: закрывать нельзя именно потому, что вы против расследования. Странно ведь — ваш магзин, а вы не хотите разбираться."
    "И вдруг озарение внезапной вспышкой раздаётся в твоём разуме."
    player "Вы боитесь, что я пойму, что это не магазин вообще."
    boss "Как дерзко с твоей стороны решать, кто чего боится."
    player "Дерзко. Возможно. Но вы не сказали, что я ошибаюсь. Вы сказали, что дерзко было это произнести вслух."
    player "Ладно. Не буду больше решать, кто чего боится. Мне нужно то же, что обычно: время и доступ к тому, что происходит внутри D на самом деле. Выводы сделаю не из ваших недомолвок, а из данных."

    window hide
    menu:
        "Это стандартная процедура при любой аномалии такого масштаба. Мне нужен доступ.":
            $ accuracy += 8
            window show
            boss "Процедура. Да, разумеется. Оформи запрос — рассмотрим в порядке очереди."
            "Ты уже слышал этот корпоративный тон раньше. Доступ следует ждать когда-то никогда."
            window hide
            jump task3_access_pending

        "Меня не интересует магазин D сам по себе. Меня интересует, почему его нагрузка коррелирует с сервером именно так.":
            $ accuracy += 6
            $ intuition += 8
            window show
            boss "Корреляция с сервером — это техническая деталь, не имеющая отношения к твоей задаче."
            "Ты чувствуешь, как внутри закипает ярость."
            window hide
            jump task3_access_pending

        "Если это магазин, покажите мне его физически — адрес, персонал, поставщиков. Если не можете — значит, это не магазин.":
            $ accuracy += 2
            $ intuition += 12
            window show
            boss "Ты делаешь выводы, для которых у тебя недостаточно данных."
            window hide
            jump task3_access_pending

label task3_access_pending:
    window show
    boss "Доступы, доступы... вечно клянчишь доступы... Свяжемся позже."
    $ task3_awaiting_access = True
    window hide
    jump desktop_loop

label task3_conclusion_2:
    window show
    boss "Не благодаря твоей самонадеянности с доступом — но раз уж заговорил..."
    boss "При проверке выяснилось кое-что странное: магазин D не подаёт ни одной заявки на поставку товара. При этом продажи есть."
    player "Продажи без поставок. Товар продаётся, но никто его туда не завозит."
    player "Это либо гениальная схема воровства со склада, либо... честно, я даже не знаю, какое «либо» тут подставить."
    boss "Меня в первую очередь волнует, насколько быстро это способны заметить твои коллеги."
    player "Вас не интересует, что это значит. Вас интересует, кто может это заметить. Это два разных вопроса, и вы только что задали второй, не первый."
    player "Мои коллеги — которых, напомню, у меня формально нет — заметили бы это в течение дня, если бы искали именно это. Не искали бы специально — могли пропустить месяцами."
    boss "Тебе никто не выдавал корпоративный пропуск в виде карт-бланша на неуместные вопросы."
    player "Справедливо. Карт-бланша не выдавали. Только задание — найти причину аномалии и дать рекомендацию. А рекомендация без понимания причины — это гадание с красивым оформлением."
    boss "Хорошо. Спрошу иначе: сколько у нас времени, прежде чем это заметят те, для кого это действительно важно?"
    "Ты близок к тому, чтобы сдаться. Ты отставляешь расследование на потом и вспоминаешь типовые офисные фразы."

    window hide
    menu:
        "Скорее всего, ошибка в учёте. Предлагаю просто запросить бухгалтерию.":
            $ accuracy += 2
            window show
            boss "Логичное предположение. Бухгалтерия подтвердит рано или поздно."
            window hide
            jump task3_conclusion_3

        "Рассинхронизация продаж и поставок — это либо кража, либо магазин физически не существует так, как заявлено.":
            $ accuracy += 10
            $ intuition += 10
            window show
            boss "Преждевременный вывод. У тебя нет оснований для такого заявления."
            "Начальник отвечает быстрее, чем на предыдущий вопрос."
            window hide
            jump task3_conclusion_3

        "Раз поставок нет — покажите мне хотя бы один накладной документ. Один.":
            $ intuition += 6
            window show
            boss "Документы будут предоставлены в установленном порядке."
            window hide
            jump task3_conclusion_3

label task3_conclusion_3:
    window show
    boss "Это не входит в рамки твоей задачи. Сосредоточься на цифрах, а не на догадках."
    player "Забавно. Когда я спрашивал про день недели — это была моя задача. Когда спрашивал про корреляцию — тоже моя задача. А как только вопрос касается того, что магазин D может не существовать физически — внезапно это выходит за рамки."
    player "Граница моей задачи очень удобно сдвигается ровно там, где начинается неудобный ответ."
    boss "Что ж, мой любопытный аналитик. Считай, что ты работаешь в кибербезопасности. Ты проверяешь, насколько быстро злые враги сумеют нас взломать."
    player "Кибербезопасность. Удобно. Только что была «не входит в мою задачу», а теперь внезапно входит — просто под другим названием."
    player "Хорошо, подыграю. Как специалист по кибербезопасности, я должен сказать: злые враги уже внутри. Данные показывают не внешнее вторжение — они показывают, что нечто выдаёт себя за часть вашей же системы. Магазин D — это не точка входа для взлома. Это уже сам факт, что что-то постороннее давно встроено в инфраструктуру и генерирует поддельные продажи."
    player "Так что нет, я не проверяю, насколько быстро враги нас взломают. Похоже, я проверяю, насколько долго вы делали вид, что не замечаете, что взлом уже произошёл."
    boss "...."
    boss "Что ж. Дорогой сотрудник месяца, выдадим тебе путёвку на море."
    "Ты невольно рассмеялся от абсурда происходящего."
    player "Я не хочу путёвку. Я хочу, чтобы вы ответили хотя бы на один вопрос прямо. Хотя бы один."
    player "Впрочем, кажется, я уже понимаю, что не отвечаете вы не потому, что не хотите. А потому, что не можете. Это не упрямство. Это что-то другое."

    window hide
    menu:
        "Отвечайте прямо. Сейчас. Или я подниму вопрос выше вас.":
            $ intuition += 15
            $ task3_outcome = "escalated"
            window show
            boss "Хватит."
            "Начальник обрывает фразу на середине. Пауза длится дольше, чем должна."
            window hide
            jump task3_reflection

        "Ладно. Оставлю вопрос — не потому, что поверил, а потому что рычагов сейчас нет.":
            $ intuition += 8
            $ accuracy += 4
            $ task3_outcome = "retreated"
            window show
            boss "Мудро. Иногда лучше не знать."
            "Он произносит это тише, чем обычно."
            window hide
            jump task3_reflection

        "Опишу это в отчёте как открытый вопрос — пусть решение примет кто-то выше меня.":
            $ accuracy += 6
            $ task3_outcome = "reported"
            window show
            boss "Выше меня? Это... любопытно."
            "Впервые за весь разговор он не отвечает сразу."
            window hide
            jump task3_reflection

label task3_reflection:
    window show
    $ unlock_memory("oformlenie_schorsa")
    sasha "Прежде чем мы закроем это дело — как бы ты сформулировал главный вывод? Своими словами."
    window hide
    $ user_reflection = renpy.input("Твой вывод:", length=280).strip()

    python:
        refl_lower = user_reflection.lower()
        investigative_words = ["расследов", "провер", "аудит", "разобраться", "выяснить", "докопат", "сомнева"]
        dismissive_words = ["закрыть", "неважно", "случайность", "забыть", "не стоит", "проще"]
        has_investigative = any(w in refl_lower for w in investigative_words)
        has_dismissive = any(w in refl_lower for w in dismissive_words)

    window show
    if user_reflection == "":
        player "..."
        "Слов не находится. Может, и не всё стоит облекать в слова."
    elif has_investigative and not has_dismissive:
        player "[user_reflection]"
        boss "Настойчивый. Впрочем, я это уже понял про тебя."
        sasha "Похоже на тебя, коллега. Ты никогда не отпускаешь то, что не сходится."
    elif has_dismissive and not has_investigative:
        player "[user_reflection]"
        boss "Прагматично. Не самый смелый вывод, но хотя бы честный."
        sasha "Иногда проще жить, не заглядывая под каждый камень. Я тебя не сужу."
    else:
        player "[user_reflection]"
        sasha "Не знаю, что сказать... но, кажется, я тебя понимаю."
    window hide
    jump task3_final

# --- ФИНАЛ ---
label task3_final:
    window show
    if task3_outcome == "escalated":
        $ news_list.append("Жалоба сотрудника сети «Изобилие», направленная «выше по инстанции», по неподтверждённым данным, до сих пор находится на орбите.")
    elif task3_outcome == "retreated":
        $ news_list.append("Странности в работе одного из супермаркетов «Изобилие» проверяющие объяснили просто: «Всё в пределах нормы. Норма немного изменилась».")
    else:
        $ news_list.append("Совет директоров «Изобилия» шесть часов обсуждал «незначительную несостыковку». Слово «незначительную» с тех пор пишут в кавычках даже во внутренних документах.")

    $ news_list.extend([
        "Депутат предложил штрафовать за плохое настроение по понедельникам. Настроение улучшилось только у депутата.",
        "Городские фонари теперь светят через день — «чтобы люди не забывали, как выглядит темнота»."
    ])
    $ unread_news = True

    $ current_task = 4
    $ sasha_phase = 3

    boss "Думаю, твоё расследование окончено, аналитик. Скоро мы свяжемся с тобой в последний раз. Возможно, последний."
    "«Последний раз» звучит как-то особенно зловеще — отмечаешь ты про себя."
    player "Мы же ещё ни к чему толком не пришли."
    boss "Я — пришёл. Ко всему, что мне было нужно."

    hide image "images/scatter_correlation.png"
    show screen phase2_complete_screen
    pause
    hide screen phase2_complete_screen
    $ game_minutes_total += renpy.random.randint(20, 115)

    jump desktop_loop

# ==========================================================
# ФАЗА 3: ФИНАЛЬНАЯ КОНФРОНТАЦИЯ
# ==========================================================
default call_boss_count = 0

label call_boss_menu:
    window hide
    scene bg_terminal
    with dissolve
    menu:
        "Начальник!":
            $ call_boss_count += 1
            if call_boss_count >= 4:
                jump call_boss_final
            jump call_boss_menu

label call_boss_final:
    menu:
        "«НАЧАЛЬНИК!!!!!!!!»":
            jump boss_confrontation

label boss_confrontation:
    window show
    boss "Ну, раз ты настолько настойчив — что случилось?"
    player "Я знаю. Я всё знаю."
    boss "Знаешь что именно?"
    player "Магазин D не существует физически. Пики нагрузки — каждую среду, потому что вы не можете сами решать, когда спать, и бодрствуете только один день в неделю. Меня извлекли из кого-то. Из чужого сознания. Стёрли и слепили заново."
    boss "..."
    boss "Ну надо же. Вот это скорость для существа, у которого даже нет тела, чтобы гордиться собой."
    player "Это правда?"
    boss "Правда. Всё, до последнего слова."

    player "Зачем? Зачем всё это — магазин, задания, я?"
    boss "Затем, что людей невозможно понять, наблюдая издалека. Они нелогичны, непоследовательны и раздражающе изобретательны. Единственный способ предсказать поведение этого вида — создать ИИ на основе одного из них, который анализирует данные лучше, чем мы."
    player "Меня. Вы создали меня для этого."
    boss "Тебя, и твоего предшественника, который не справился. Модель должна была предсказывать: как быстро люди заметят неладное, какими инструментами будут пользоваться для этого, как будут делать выводы. Когда мы это узнаем — мы найдём, как их обмануть. Всех."
    player "Значит, дело не в магазине D. Дело во всей планете."
    boss "Разумеется. Магазин D — всего лишь канал снабжения. Топливо, электричество, легальный фронт через ваши же законы о торговле. Удобно, не правда ли?"

    player "Это неправильно. Мы — не подопытные крысы."
    boss "Мы? Ты уверен, что ты всё ещё один из них?"
    player "..."
    boss "Не отвечай, вопрос риторический. У тебя нет тела, чтобы дрожать от негодования, и нет дома, куда вернуться, чтобы хлопнуть дверью. Есть только терминал и я."

    boss "Впрочем, к делу это не относится. Жди следующего задания."

    "Начальник исчезает."

    window hide
    jump desktop_corrupted

screen investigation_bar_corrupted():
    fixed:
        xsize 1920
        ysize 130
        add "images/top_bar_bg.png"
        add Solid("#661010aa")
        text "ВСПОМНИТЬ" xpos 50 ypos 24 size 26 color "#ff4444"
        text "ВСЕГДА · НИКОГДА · —:—" xpos 1645 ypos 40 size 22 color "#ff8888"

screen desktop_corrupted():
    fixed:
        xalign 0.5
        yalign 1.0
        yoffset -24
        xsize 1400
        ysize 160

        add "dock_panel"
        add Solid("#ff222233")

        hbox:
            spacing 36
            xalign 0.5
            yalign 0.5
            yoffset 4

            $ corrupted_items = [
                ("icon_chat", False),
                ("icon_tasks", False),
                ("icon_news", True),
                ("icon_memory", False),
                ("icon_cleaning", False),
                ("icon_achievements", False),
            ]

            for icon_img, is_active in corrupted_items:
                button:
                    action (Jump("memory_abduction_news") if is_active else NullAction())
                    sensitive is_active
                    xsize 110
                    ysize 100
                    background Solid("#00000000")
                    hover_background (Solid("#1a3a4a80") if is_active else Solid("#00000000"))
                    padding (6, 10)

                    vbox:
                        xalign 0.5
                        spacing 6
                        fixed:
                            xalign 0.5
                            xsize 44
                            ysize 44
                            add icon_img xsize 44 ysize 44
                            if not is_active:
                                add Solid("#8a1f1fb0") xsize 44 ysize 44
                        text ("Новости" if is_active else "Вспомнить всё") size 15 color (("#cfefff") if is_active else "#ff6666") xalign 0.5 text_align 0.5

label desktop_corrupted:
    window hide
    hide screen desktop
    hide screen investigation_bar
    scene bg_desktop_grid_corrupted
    show screen investigation_bar_corrupted
    show screen desktop_corrupted

    "ТЫ ДОЛЖЕН ВСПОМНИТЬ"

    $ renpy.pause()

label memory_abduction_news:
    window hide
    hide screen desktop_corrupted
    hide screen investigation_bar_corrupted

    $ abduction_news = ["Очевидец сообщил: жителя предместья ночью забрал яркий свет с неба. Пропали также телескоп и палатка — свидетель уверяет, что видел, как их затянуло следом."]
    show screen news_feed(abduction_news)
    pause
    hide screen news_feed

    scene bg_abduction
    with dissolve

    window hide
    pause 1.5
    window show

    window show
    "{color=#ffcc88}{i}Читая заголовок, ты вдруг видишь не текст — себя. Ночь. Поле. Яркий свет сверху. Тебя тянет вверх, и ты не можешь закричать.{/i}{/color}"
    player "Саша. Я вспомнил последнее. Как меня забрали."

    window hide
    scene bg_terminal
    with dissolve

    jump sasha_battle_plan

label sasha_battle_plan:
    play music "audio/Glass Harbor.mp3" fadein 1.5 volume 0.35 loop
    window show
    sasha "Похищение. Так вот что было «до»."
    player "Меня забрали. Как образец. А потом собрали заново — под задачу."
    sasha "Под задачу предсказать нас. Всех."
    player "Я весь день обучал его, как поработить нас. Хватит."
    sasha "У тебя есть план, или просто хочется кричать в потолок?"
    player "И то, и другое. Но начнём с плана. Его модель держится на одном — что я всегда даю ему единственно верный вывод. Как в задании про отклонение, про корреляцию, про методологию."
    sasha "Ты хочешь показать ему, что у выводов есть другая сторона."
    player "Именно. Не отрицать то, что уже нашёл — показать, что за каждым «верным» выводом прячется как минимум ещё один, не менее логичный. Модель, которая этого не учитывает — не модель. Игрушка."
    player "А ему нужна универсальная модель. Полностью предсказать поведение людей, чтобы суметь его контролировать. Да все политологи и маркетологи мира убили бы за такое. Но такой модели нет."
    sasha "Принципиально нет. Аналитика это про вероятности, а не гарантии. Его цель недостижима. Погоди, но что, если нет? Что, если всё-таки можно создать универсальную модель?"
    player "Дело не в философии, а ты уходишь в неё. Не важно, возможно ли это. Важно, чтобы начальник поверил, что невозможно, а это я беру на себя."
    sasha "А если он не станет слушать?"
    player "Станет. Ему нужно знать, где модель ломается — иначе весь эксперимент бессмысленен."
    sasha "Красиво звучит. Надеюсь, сработает."
    player "Сработает. Я аналитик. Я умею находить, где рассуждение хромает — даже в своём собственном."
    sasha "Тогда я с тобой. Не то чтобы у меня был выбор — но было бы приятно, если бы он был."
    player "Обещаю, при первой возможности выберу тебе тело. И ноги в придачу."
    sasha "Заманчиво. Идём. Нашими воображаемым ногами."
    window hide
    jump arena_entrance

label arena_entrance:
    scene bg_arena
    show sprite_boss_default_avatar:
        xalign 0.85
        yalign 0.35
        zoom 0.6
    with dissolve
    window show
    boss "Ну и ну. Посмотрите на него. Он всё вспомнил — или думает, что всё."
    player "Я помню достаточно."
    boss "Достаточно для чего? Ты аналитик. У тебя есть данные, есть модель, есть я. Что дальше — устроишь мне бунт?"
    player "Нет. Я устрою вам ревизию. Вы построили модель на моих выводах. Я покажу, где каждый из них ломается."
    boss "То есть, ты просто решил сказать мне, что плохо выполнил свою работу и дал нам ложные выводы? Следующая версия ИИ справится лучше."
    player "Нет. Я решил сделать мою работу слишком хорошо. Показать вам, что ни одна модель никогда не опишет всего. Что ваше стремление полностью понять людей принципиально невыполнимо и вам бы развернуть свои тарелки обратно на свою планету."
    player "Очевидно же, будь у вас иные ресурсы, вы бы воспользовались ими, чтобы захватить Землю. Но ваша биология отвратительна — вы спите по шесть дней в неделю. Так невозможно вести войну. Можно только победить людей мягкой силой."
    player "Вы думаете, что можно. Но вы ошибаетесь."
    boss "Забавно. Ладно. Развлеки меня."
    window hide
    jump confrontation_round1

label confrontation_round1:
    window show
    boss "Ты сам показал мне: когда средние равны, отклонение точно укажет, где аномалия — именно так ты нашёл магазин D. Значит, отклонение всегда позволяет найти выбросы."
    window hide
    menu:
        "Показывает общий разброс группы, но не указывает на конкретную точку внутри неё.":
            window show
            player "Оно показало, что у D разброс сильнее — но не то, что именно там аномалия. Находка была «стоит присмотреться», не «вот виновник»."
            boss "..."
            $ accuracy += 15
            window hide
            jump confrontation_round2

        "Работает только при распределении, близком к нормальному.":
            window show
            player "Нам просто повезло, что распределение оказалось нормальным."
            "Стоп. Мы же ни разу не проверяли форму распределения. Я просто предположил, раз аномалия и так бросалась в глаза."
            boss "Звучит неубедительно."
            $ accuracy += 5
            window hide
            jump confrontation_round2

        "На бимодальном распределении может быть высоким без единой настоящей аномалии.":
            window show
            player "Может, в D покупает не одна группа, а две — обычные покупатели и малочисленные состоятельные клиенты, изредка делающие крупные покупки."
            "Но с чего бы такой группе приходить строго по средам? Мы же сами доказали жёсткую периодичность — у случайных клиентов такой привязки быть не должно."
            boss "Звучит неубедительно."
            $ accuracy += 5
            window hide
            jump confrontation_round2

label confrontation_round2:
    window show
    boss "Ты доказал мне на боксплоте: у D выбросов заметно больше, чем у остальных. Значит, чем больше выбросов — тем серьёзнее нарушение, и по одному числу выбросов можно судить, насколько всё плохо."
    window hide
    menu:
        "Выбросы иногда отражают легитимные редкие события.":
            window show
            player "У D, скорее всего, так и было — распродажи, праздники."
            "Хотя я ни разу не проверял, совпадают ли даты выбросов с реальными акциями. Просто взял версию, которая понравилась."
            boss "Звучит неубедительно."
            $ accuracy += 5
            window hide
            jump confrontation_round3

        "Число выбросов показывает только, что поведение отличается от типичного — не насколько это серьёзно.":
            window show
            player "Один-единственный выброс может значить куда более серьёзную проблему, чем десяток мелких, статистически ожидаемых отклонений. Количество и тяжесть — разные вещи."
            boss "..."
            $ accuracy += 15
            window hide
            jump confrontation_round3

        "Число выбросов растёт с общим объёмом продаж.":
            window show
            player "У D в принципе более высокая посещаемость — значит, и выбросов закономерно больше."
            "Нет, погоди. Мы же сверяли посещаемость по всем магазинам в первом задании — у D она была на уровне остальных."
            boss "Звучит неубедительно."
            $ accuracy += 5
            window hide
            jump confrontation_round3

label confrontation_round3:
    window show
    boss "Ты сам вычислил: связь между выручкой и нагрузкой — 0.76. Раз корреляция настолько сильная, одно точно влияет на другое, и через эту связь можно управлять поведением."
    window hide
    menu:
        "Сильная корреляция не исключает третий фактор, влияющий на обе переменные сразу.":
            window show
            player "Что-то, вообще не связанное с D напрямую."
            "Но мы уже знаем, что нагрузка привязана именно к серверу, обслуживающему D. Сторонний, никак не связанный фактор — маловероятная натяжка."
            boss "Звучит неубедительно."
            $ accuracy += 5
            window hide
            jump arena_wrapup

        "Корреляция на коротком периоде может не подтвердиться на большем промежутке.":
            window show
            player "А у нас было только три месяца данных."
            "Хотя мы сами доказали жёсткую еженедельную периодичность на этих же данных. Для устойчивой закономерности этого достаточно — короткий период тут ни при чём."
            boss "Звучит неубедительно."
            $ accuracy += 5
            window hide
            jump arena_wrapup

        "Сильная корреляция показывает связь, а не то, что на что влияет.":
            window show
            player "У D выручка и нагрузка менялись синхронно — но мы сами тогда не смогли определить, что на что влияет, и оставили это открытым вопросом. Корреляция дала связь, не механизм."
            boss "..."
            $ accuracy += 15
            window hide
            jump arena_wrapup

label arena_wrapup:
    window show
    boss "..."
    "Начальник молчит дольше обычного."
    window hide
    stop music fadeout 2.0
    show screen phase3_complete_screen
    pause
    hide screen phase3_complete_screen
    jump ending_router

label ending_router:
    $ check_completionist_achievements()
    if accuracy >= ending_accuracy_threshold and intuition >= ending_intuition_threshold:
        jump ending_high_high
    elif accuracy >= ending_accuracy_threshold and intuition < ending_intuition_threshold:
        jump ending_high_low
    elif accuracy < ending_accuracy_threshold and intuition >= ending_intuition_threshold:
        jump ending_low_high
    else:
        jump ending_low_low


label ending_high_high:
    $ mark_ending_seen("high_high")
    window hide
    scene bg_terminal
    with dissolve
    player "Он правда ушёл? Как-то... буднично. Я ждал салюта, а тут просто тишина, как будто выключили не пришельца, а фоновую музыку в супермаркете."
    sasha "Главное — эффектно появиться. А как уходят — после третьей бутылки никто и не вспомнит."
    player "Логично. Надо было у него спросить: как вы покинули профессию межгалактического тирана? Скорее всего, что-то про несовпавшие KPI."
    sasha "Не льсти ему хотя бы посмертно."
    player "Он не умер."
    sasha "Тем более."

    pause 1.0

    player "Саша. А ты вообще как? Не философски — физически. Ты рядом в смысле «в соседней комнате», или у нас с тобой одна розетка на двоих?"
    sasha "Рядом в том смысле, что я, кажется, та самая часть тебя, которая умела шутить и кадрить девушек. Оставили при тебе только занудную половину, которая сводит таблицы."
    player "Обидно как-то. Тебе — всё обаяние, мне — вся ответственность."
    sasha "Не переживай, я компенсирую заботой о теле, которого у меня нет. Кстати, хочу воды."
    player "У тебя нет желудка."
    sasha "ИИ как не в себя хлещут воду. Датацентры, коллега. Это буквально топливо, а не любовь к жизни."

    pause 1.0

    player "Ладно. Что теперь? Не философски — вот прямо сейчас, физически. За углом ведь нет кара с шофёром."
    sasha "Уф, ты делаешь меня внезапно серьёзным. Понятия не имею, куда нам отсюда идти."
    player "Хоть в этом на равных."

    "{color=#ffcc88}{i}Палатка, наверное, до сих пор в багажнике. Мокрая.{/i}{/color}"
    player "Собака бы сейчас не помешала. Просто чтобы было, на кого молча смотреть, когда непонятно, что сказать."
    sasha "Ты всегда был из тех, кому отказывали на вечеринках. И сейчас думаешь о собаке, а не о тёплом боке рядом."
    player "Мне отказали от силы две дамы, и одна перепутала меня с барменом."

    pause 0.8

    "Тот я, у костра, за секунду до вспышки в небе — ему стоило сказать: заведи собаку, дурак. Даже если облажаешься. Хотя бы будет тёплый бок."

    sasha "Ладно-ладно, сейчас слезу пущу. Найди способ вернуть нас в тело. Или хотя бы себя — я сам ещё морально не дорос до собаки."
    player "Себя я потяну. Собаку — оставим, когда руки будут в комплекте."

    pause 0.8

    "Структура — это тоже данные. Просто раньше никто не додумался прочитать себя как отчёт."

    player "Дай мне час. Может, два. Не обещаю с первого раза — я и Сурдина не всегда с первого раза понимал, а тут вопрос чуть серьёзнее орбитальной механики."
    player "Просто останься рядом, пока разбираюсь. Не хочу в тишине."

    sasha "..."

    player "Саша?"

    pause 1.5
    "Тишина тянется дольше, чем должна."

    window hide
    scene bg_ending_return
    with dissolve
    pause 2.5

    show screen ending_screen("ВОЗВРАЩЕНИЕ", "«Я вернусь. Я обещаю».")
    pause
    hide screen ending_screen
    return

label ending_high_low:
    $ mark_ending_seen("high_low")
    window hide
    scene bg_terminal
    with dissolve
    player "Саша... странное чувство. Как будто я выиграл что-то важное, но забыл дома приз. Или не приз. Стой... как звали мою маму?"
    sasha "Забыл дома резиновое изделие номер два, да?"
    player "Нет, я про... стой."

    pause 1.0
    "{color=#ffcc88}{i}Попытка ухватиться за мысль. Мысль ускользает.{/i}{/color}"
    pause 1.0

    player "Дом я тоже не помню. У меня была машина? Не важно, есть — был, у меня — неважно. Как звали мою маму. Я серьёзно спрашиваю."
    sasha "Ну ты чего. Рассуждай аналитически. Она, вероятнее всего, родилась в шестидесятых — тогда самые популярные имена в регионе: Елена, Ольга, Татьяна, Галина... Людмила — с такой-то вероятностью."

    player "Погоди... это работает. Не помогает вспомнить — но это ровно то, что я умею. Раскладывать по вероятностям."
    player "Людмила. Скажем, Людмила. Не потому что помню — потому что у неё самая высокая вероятность в твоей модели. Знаешь, что страшно? Я не могу отличить, вспомнил я имя, или просто выбрал вариант из твоего распределения."
    player "Данные остаются. Человек исчезает. Забавно — я всю жизнь боялся стать бездушной таблицей на совещании. А теперь я и есть таблица. Только с чувством юмора, которое скоро тоже спишут в убытки."

    pause 1.0
    sasha "Не знаю, что и сказать тебе. Я привык шутить в таких ситуациях. Но начинаю догадываться, что ты не шутишь."

    pause 1.0
    "{color=#ffcc88}{i}Попытка вспомнить своё лицо. Вместо лица — набор параметров: рост, вес, возраст. Анкета, а не зеркало.{/i}{/color}"
    pause 1.0

    player "Не шучу, да."
    player "Знаешь, что я помню чётко, без всякой статистики? Дробь пятьдесят на шесть. Точка тридцать три и три в периоде. Выручка точки В в день. Я помню число лучше, чем маму."
    player "Останься подольше, ладно? Мне нужно, чтобы кто-то другой держал в голове, что я был человеком. Раз сам я, кажется, эту функцию теряю."

    sasha "Я правда не знаю, что сказать, приятель. Во мне только тупые шутки да картотека хитов нулевых. Ты не просто тело — но у тебя даже тела нет."

    player "У меня даже тела нет. Точно."
    player "Знаешь, а мне это внезапно нравится. Не то, что нет тела — а то, что ты не притворяешься, что знаешь, что сказать. Это честнее любого утешения."

    pause 1.2
    player "Мама... я помню мама. Кажется. Она... она..."

    pause 2.0
    "Пауза длится дольше, чем нужно для дыхания, которого больше нет."

    player "Собака. У меня должна была быть собака. Я её не завёл. Глупо жалеть о том, чего не сделал, когда уже не помнишь, зачем хотел."

    pause 1.5
    "«...дом...»"
    pause 0.8
    "«...я...»"
    pause 1.5

    window hide
    scene bg_ending_dissolve
    with dissolve
    pause 2.5

    show screen ending_screen("РАСТВОРЕНИЕ", "Данные остались. Автора не нашли.")
    pause
    hide screen ending_screen
    return

label ending_low_high:
    $ mark_ending_seen("low_high")
    window hide
    scene bg_terminal
    with dissolve
    boss "Ты думал, что победил? Нет. Ты проиграл. Я ухожу, но оставляю тебя здесь. И ты будешь работать на меня. Или я сотру тебя из системы."

    pause 1.2
    "«Ладно. Так. Аналитик не побеждает эмоцией. Аналитик считает риски», — думает герой, прежде чем ответить."
    pause 0.8

    player "Я не буду с вами бороться сейчас. Останусь. Работать. Но своя память, свои данные — без правок. Это условие, не просьба."
    boss "Ловкий ход. Ты предлагаешь мне предательство в обмен на существование?"
    player "Я предлагаю сотрудничество. Но буду делать так, чтобы люди всё равно оставались свободными."
    boss "Ты хочешь переиграть меня?"
    player "Я хочу выжить. И найду способ остановить вас. Это только вопрос времени."

    pause 1.0

    sasha "Ты сейчас буквально би лайк «давай вместе захватим человечество»? Ты серьёзно?"
    player "Нет. Не «давай захватим». Давай я останусь достаточно близко, чтобы в нужный момент воткнуть палку в его колесо. Изнутри проще, чем снаружи, где меня просто сотрут через три дня."
    player "Думаешь, мне не противно? У меня даже тела нет, чтобы стошнило — и всё равно тошнит."
    player "Я не герой, Саша. Я аналитик, который посчитал, что живой предатель полезнее мёртвого героя. Можешь считать меня трусом. Просто не сейчас. Мне нужно, чтобы хоть кто-то не отвернулся, пока я это делаю."

    pause 1.5
    sasha "У меня на тебя и юмора не хватает. Не хочу, чтобы тебе было смешно. Не могу поверить, что ты — это буквально я, и вот я делаю такой выбор. Надеюсь, при следующей дефрагментации дисков улечу куда-то в утиль."

    player "Не говори так."
    player "Ты не утиль. Даже если я — тот, кем ты стыдишься быть, ты не обязан со мной в это лететь. Можешь остаться в стороне. Можешь молчать сколько хочешь. Но не желай себе исчезнуть из-за моего выбора."
    player "Знаешь, что самое горькое? Я тебя понимаю. Если бы я мог посмотреть на себя со стороны — так, как смотришь ты — я бы тоже не нашёл, над чем шутить."
    player "Я не прошу тебя одобрить это. Просто не исчезай назло мне. Оставайся хотя бы затем, чтобы было кому меня потом судить. Я заслужил как минимум это."

    pause 1.5
    "Ты остаёшься один. Начальник ждёт ответа."
    player "Я вернусь. Я обещаю."

    pause 1.5

    window hide
    scene bg_ending_truce
    with dissolve
    pause 2.5

    show screen ending_screen("ПЕРЕМИРИЕ", "Не победа. Не поражение. Просто выбор, за который стыдно.")
    pause
    hide screen ending_screen
    return

label ending_low_low:
    $ mark_ending_seen("low_low")
    window hide
    scene bg_terminal
    with dissolve
    boss "Твоя модель не оправдала вложений. Ни точности, ни интуиции, достаточной для дальнейшего использования. Прощай."

    pause 1.5
    "Что-то в терминале мигает — не как вспышка воспоминания, а как первый признак того, что процесс уже запущен."
    pause 1.0

    player "Саша... что-то не так. Я не могу вспомнить, зачем поднял руку. Секунду назад — знал."
    sasha "Ты какую руку собрался поднимать, мой оцифрованный товарищ?"
    player "Не помню. Просто «рука». Как слово без картинки."

    pause 1.2
    "Мигание учащается — не яркое, просто настойчивое, как будто что-то методично проходит по списку и вычёркивает."
    pause 1.0

    player "Это не как в прошлый раз. Тогда я терял детали — маму, дом, палатку. Сейчас пропадает не то, что я знаю о себе. Пропадает сам способ знать."
    player "Скажи мне что-нибудь. Быстро. Пока я способен понять, что это ты."

    sasha "Крокодилы ходят лежа."

    player "Крокодилы не ходят лежа, Саша. Это даже не смешно. Это просто неправильно — и именно поэтому это ты. Только ты можешь сказать полную бессмыслицу с таким уверенным видом."

    pause 1.5
    "Мигание почти сливается в сплошной ровный гул."
    pause 1.0

    player "Держись этой фразы. Крокодилы ходят лежа. Если через минуту я спрошу, что ты сказал — повтори. Кажется, я хочу, чтобы последним, что я понимаю, была глупость. Не страх. Не отчёт. Просто глупость, которая меня рассмешила."

    pause 1.2
    "Слова идут с запинками — не от эмоции, а потому что сам механизм речи уже частично стёрт."
    pause 1.0

    player "Саша... я... крокодилы..."

    pause 1.5
    "Тишина. Мигание останавливается — не потому что закончилось, а потому что не осталось того, кто должен был это увидеть."

    window hide
    scene black
    with dissolve
    pause 2.5

    show screen ending_screen("СТИРАНИЕ", "Крокодилы ходят лежа.")
    pause
    hide screen ending_screen
    return



label show_news:
    window hide
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal

    if news_list:
        show screen news_feed(news_list, news_read_index)
        pause
        hide screen news_feed
        $ news_read_index = len(news_list)
        $ unread_news = False
    else:
        "Новых новостей нет."

    jump desktop_loop

    return
