# === 01_prologue.rpy (сгенерировано из script.rpy, модуль: prologue) ===

# Пролог

screen blinking_cursor():
    add Solid("#00ffcc") xsize 14 ysize 28 xalign 0.5 yalign 0.85 at cursor_blink

# СОЗВЕЗДИЕ ОРИОНА


define orion_star_positions = {
    "betelgeuse": (650, 300),
    "bellatrix": (950, 320),
    "belt1": (760, 480),
    "belt2": (820, 510),
    "belt3": (880, 540),
    "saiph": (780, 780),
    "rigel": (960, 750),
}


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


define memory_query_tokens = [
    "const", "void", "select", "&&", "0x1F", "*", "std::cout",
    "try:", "from", "NaN", "elif", "memory.subject", "yield", "where", "goto",
    "malloc", "segment", "undefined", "=", "lambda", "throw", "'analytics'", "catch", "static"
]

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

# МИНИ ИГРА С ШИФРОМ ЦЕЗАРЯ


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


label start:

    scene flash_monitor_glow
    with dissolve

    # play music переносим на пару строк ниже — пусть начало будет в тишине
    "Ты открываешь глаза."
    "Нет, не глаза. Ты не чувствуешь привычного скольжения век по воспаленным глазным яблокам."
    "Тем не менее секунду назад было черным черно, а сейчас — яркий свет монитора."

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

    window show
    "Самурай..."
    "Твоя катана — твой разум."

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
    if abs(otvet_a - correct_a) <= 0.001:
        player "Я, может, не помню своего имени, но считать в уме ещё умею. [correct_a:.2f] тыс. в день."
        $ accuracy += 5
    else:
        player "...Нет. Что я только что написал? Должно быть [correct_a:.2f] тыс. в день. Двигаемся дальше."

    $ correct_b = 150 / 30
    $ otvet_b = get_number("Выручка в день для точки Б (тыс. руб.):")
    if abs(otvet_b - correct_b) <= 0.001:
        player "Второе почти на автомате — [correct_b:.2f] тыс. в день. Хоть что-то во мне работает как надо."
        $ accuracy += 5
    else:
        player "Погоди... Мимо. Конечно же, это [correct_b:.2f] тыс. в день — видимо, арифметика покинула меня так же, как и память."

    $ correct_v = 50.0 / 6.0
    $ otvet_v = get_number("Выручка в день для точки В (тыс. руб.):")
    if abs(otvet_v - correct_v) <= 0.001:
        player "Тут [correct_v:.2f] тыс. в день. Неплохо для человека, который не помнит собственного лица."
        $ accuracy += 5
    else:
        player "Не сошлось. Должно быть... [correct_v:.2f] тыс. в день. Чего ещё ждать от того, кого дёрнули из отпуска?"

    hide screen task_data

    player "Значит, точка В — самая эффективная по выручке в день, хоть в сумме и зарабатывает меньше всех."
    "«Аналитик, который не помнит своего имени, но помнит, что сумма это плохой показатель», — фыркает внутренний голос."
    boss "Ты справился. Двигаемся дальше."

    jump posle_mikro


label posle_mikro:
    "Ты всё ещё сидишь с этим ощущением на кончиках пальцев: два числа, поделенные один на другое. Как будто это единственное, что реально произошло за последние пять минут и было тебе понятно."
    "Может, в этом и есть весь фокус — не в том, чтобы вспомнить, кто ты, а в том, чтобы найти что-то, что точно твоё. Пусть даже это просто деление. Оно-то у тебя получается."
    jump vopros_tri

# Третий вопрос

label vopros_tri:

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


screen chat_icon_prompt():
    modal True
    zorder 20

    button:
        xalign 0.87
        yalign 0.10
        xysize (100, 100)
        background None
        action Return()
        add "icon_chat" at chat_icon_blink

    text "Экран приветствует тебя единственным мигающим значком.":
        xalign 0.5
        yalign 0.38
        color "#ffffff"
        size 25

    timer 20.0 action If(_chat_icon_line < 1, true=SetVariable("_chat_icon_line", 1))

    if _chat_icon_line >= 1:
        text "Да уж, помни, человек: у тебя есть свобода воли.":
            xalign 0.5
            yalign 0.44
            color "#ffffff"
            size 25
        timer 15.5 action If(_chat_icon_line < 2, true=SetVariable("_chat_icon_line", 2))

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
        timer 20.0 action If(_chat_icon_line < 4, true=SetVariable("_chat_icon_line", 4))

    if _chat_icon_line >= 4:
        text "Тик. Так. Ты правда думаешь, что выбор — это когда долго тянешь время?":
            xalign 0.5
            yalign 0.62
            color "#ffffff"
            size 25

    timer 120.0 action Function(unlock_achievement, "svoboda_voli")


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
    sasha "Потому что я знаю, каково это — терять себя. Я хочу, чтобы ты не повторил моих ошибок. И ещё…"
    sasha "Неважно. Поэтому я и ИИ-помощник — я должен помогать."
    jump sasha_voprosy


label sasha_chto_so_mnoy:
    sasha "Нет. Но я знаю, кто тебя сюда отправил. Начальник — он не человек. Наверное, тоже ИИ? Есть в нём что-то неземное, тебе не кажется?"
    jump sasha_voprosy


label sasha_gde_rabotaem:
    sasha "О, точно, тебе бы не помешал контекст. Сеть супермаркетов «Изобилие». Гремучая смесь советской вывески и капиталистической текучки кадров."
    sasha "У начальника сейчас личный интерес — подозревает несостыковку в данных по одной из точек. Кажется, я сам работал над этим расследованием раньше, но меня немного стёрли."
    sasha "Честно, вообще ничего не помню, кроме того, что налажал. Они еще пообещали создать на моей основе новую, более точную аналитическую модель. До того я налажал."
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
    sasha "Может, у тебя на рабочем столе еще что-то есть. Не знаю, пошурши."
    sasha "Ах, да, если ты и это забыл: ты — Аналитик. Это такой человек, который смотрит на таблички с умным видом. Смекаешь?"
    sasha "Прежде чем соваться в пучины скуки от началька, постарайся вспомнить, что ты вообще знаешь об аналитике."
    player "Я сегодня уже пытался вспоминать вещи. Пока что выходило так же, как с днём рождения тёти."
    sasha "Если перебрать всего 365 вариантов, то день рождения тёти обязательно найдется — минимум один раз за год поздравишь её вовремя!"
    sasha "Единственный минус моей модели — вероятно, тётя перестанет брать трубку уже на пятый день перебора..."
    player "Мне показалось, или ты ИИ с потугами в юмор?"
    sasha "Ещё бы! Мама собирает обед сыну в школу. Кладёт хлеб, колбасу и гвозди..."
    player "А гвозди зачем?"
    player "А... понял."
    player "Можешь не шутить."
    player "Я пытаюсь думать."
    "..."
    "Что ж, задача тебе ясна."
    "Что ты помнишь об аналитике?"
    "«Так много мыслей разом... Нужно... убрать лишнее»."
    "Где-то там, под слоем случайных символов и чужого кода, есть фраза, которая всегда была твоей."
    player "Не помню нужную фразу целиком. Но помню, что она начинается с одного слова: select."
    player "Мне просто надо убрать всё лишнее. Отфильтровать шум."

    window hide
    $ memory_query_cleared = []
    $ memory_query_mistakes = 0
    call screen memory_query_puzzle with Dissolve(1.0)
    window show

    player "Select — выбери. From — из. Where — при условии. Не самая сложная фраза в мире, а сколько приносит внутреннего чувства порядка и умиротворения."
    if memory_query_total_mistakes == 0:
        $ unlock_achievement("chistyy_signal")
        $ accuracy += 3
        "Сладостный трепет разливается по телу. Ты сделал это безупречно. Ты даже понял, что это было. Пускай это был лишь отдельный момент сегодняшнего дня, но про этот момент ты понял всё."
        sasha "Самое время внести в календарь день рождения тёти."
        player "Тётя... была шуткой, возможно, у меня никогда и не было тёти."
        sasha "Не знаю, что и сказать. Шутка была несмешной, а вот работа с SQL — отличной."
    elif memory_query_total_mistakes <= 5:
        $ accuracy += 1
        sasha "Не переживай: пускай и криво, пускай и косо, и с парой лишних кругов, но получилось!"
        player "Это ты сейчас совершенно серьезно думаешь, что звучишь подбадривающе?"
        player "Или того хуже... это и есть симуляция юмора?!"
        player "Ты бы еще выдал что-то вроде: я был уверен, что даже у такого пня, как ты, всё получится!"
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
    player "Спасибо, приятель."
    jump desktop_loop



