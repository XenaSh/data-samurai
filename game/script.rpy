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

default ending_accuracy_threshold = 140
default ending_intuition_threshold = 140


define flash = Fade(0.25, 0.0, 0.25)

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

# Стили для окон (только фон, размеры, отступы)
style sasha_window:
    background Solid("#1a3a4a80")
    xalign 0.0
    xsize 1000
    yalign 0.5                 # по центру по вертикали
    padding (20, 15)
    left_margin 40
    right_margin 10

style player_window:
    background Solid("#1a4a2a80")
    xalign 1.0
    xsize 1000
    yalign 0.5                 # по центру по вертикали
    padding (20, 15)
    left_margin 10
    right_margin 40

# Персонажи с выравниванием текста внутри окна
default sasha_name = "ИИ"

define sasha = Character("[sasha_name]",
    color="#66ccff",
    what_color="#ffffff",
    what_slow_cps=35,
    what_fast_cps=80,
    window_style="sasha_window",
    what_xalign=0.0      # текст прижат к левому краю
)

define player = Character("Ты",
    color="#88ff88",
    what_color="#ffffff",
    what_slow_cps=35,
    what_fast_cps=80
)

define player_chat = Character("Ты",
    color="#88ff88",
    what_color="#ffffff",
    what_slow_cps=35,
    what_fast_cps=80,
    window_style="player_window",
    what_xalign=1.0      # текст прижат к правому краю — только для симуляции чата
)

# "Дышащий" фон вместо мёртвого плоского цвета
image white = Solid("#ffffff")
image flash_monitor_glow = "images/flash_monitor_glow.png"
image bg_terminal = "images/bg_terminal.png"
image bg_desktop_grid = "images/bg_desktop_grid.png"
image dock_panel = "images/dock_panel.png"
image icon_chat = "images/icon_chat.png"
image icon_tasks = "images/icon_tasks.png"
image icon_news = "images/icon_news.png"
image icon_memory = "images/icon_memory.png"
image icon_cleaning = "images/icon_cleaning.png"
image icon_achievements = "images/icon_achievements.png"
image bg_campfire = "images/bg_campfire.png"

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
    linear 1.2 matrixcolor BrightnessMatrix(0.0)

screen blinking_cursor():
    add Solid("#00ffcc") xsize 14 ysize 28 xalign 0.5 yalign 0.85 at cursor_blink


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
        text "[[КОНЕЦ]]" color "#888888" size 16 align (0.5, 0.9)

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

            for icon_img, label, target, has_badge in desktop_items:
                button:
                    action Jump(target)
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
                            if has_badge:
                                add Solid("#ff5555") xsize 12 ysize 12 xalign 1.0 yalign 0.0

                        text label size 15 color "#cfefff" xalign 0.5 text_align 0.5

# Лента новостей (без border)
screen news_feed(news_items):
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
                    for item in news_items:
                        frame:
                            xfill True
                            background Solid("#1a2a3a80")
                            padding (15, 15)
                            text item color "#e0e0e0" size 18

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
        "polnoye_dosye": {
            "title": "Полное досье",
            "desc": "Собрал все воспоминания в «Моей памяти»."
        },
        "v_kurse_vsego": {
            "title": "В курсе всего",
            "desc": "Не оставил ни одной непрочитанной новости."
        },
        "pervoye_vospominaniye": {
            "title": "Первое воспоминание",
            "desc": "Заметил нечто знакомое в чужом имени ещё в самом начале."
        },
        "sam_s_usami": {
            "title": "Сам с усами",
            "desc": "Прошёл Задание 2, не обратившись к Саше ни разу."
        },
        "ne_s_pervogo_raza": {
            "title": "Не с первого раза",
            "desc": "Ошибся хотя бы три раза — и всё равно дошёл до конца."
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

screen cleaning_minigame_screen():
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1050
        ysize 620
        background Solid("#0a0f1acc")
        padding (25, 25)
        vbox:
            spacing 12
            text "Отсортируй строки выгрузки по трём корзинам" color "#00ffcc" size 22

            text "Необработанные записи:" color "#888888" size 15
            hbox:
                spacing 10
                for row_id in cleaning_pool:
                    $ row = cleaning_rows_by_id[row_id]
                    frame:
                        background Solid("#1a2a3a")
                        padding (8, 8)
                        xsize 210
                        vbox:
                            spacing 2
                            text "Клиент: [row[client]]" color "#e0e0e0" size 13
                            text "Сумма: [row[amount]]" color "#e0e0e0" size 13
                            text "Время: [row[time]]" color "#e0e0e0" size 13
                            text "Статус: [row[status]]" color "#e0e0e0" size 13
                            hbox:
                                spacing 3
                                textbutton "Удалить" action Function(cleaning_move, row_id, "delete") text_size 11
                                textbutton "Ноль" action Function(cleaning_move, row_id, "zero") text_size 11
                                textbutton "Оставить" action Function(cleaning_move, row_id, "keep") text_size 11

            hbox:
                spacing 25
                vbox:
                    text "Удалить" color "#ff8888" size 15
                    for row_id in cleaning_sorted_delete:
                        $ row = cleaning_rows_by_id[row_id]
                        textbutton "Клиент [row[client]]" action Function(cleaning_move, row_id, "pool") text_size 12 text_color "#cccccc"
                vbox:
                    text "Заполнить нулём" color "#ffcc66" size 15
                    for row_id in cleaning_sorted_zero:
                        $ row = cleaning_rows_by_id[row_id]
                        textbutton "Клиент [row[client]]" action Function(cleaning_move, row_id, "pool") text_size 12 text_color "#cccccc"
                vbox:
                    text "Оставить" color "#88ff88" size 15
                    for row_id in cleaning_sorted_keep:
                        $ row = cleaning_rows_by_id[row_id]
                        textbutton "Клиент [row[client]]" action Function(cleaning_move, row_id, "pool") text_size 12 text_color "#cccccc"

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
        $ news_list.extend([
            "Сеть Изобилие отчиталась о результатах A/B-теста. Цифры... есть. Выводов — не очень. Акционеры сдержанны."
        ])
        $ unread_news = True
    window hide
    jump desktop_loop

label start:

    # Сознание моргает несколько раз, прежде чем стабилизироваться
    show white with flash
    pause 0.1
    hide white
    pause 0.3
    show white with flash
    pause 0.08
    hide white
    pause 0.5

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
    scene bg_desktop_grid
    with dissolve

    "Всё чужое."

    # Мигание экрана
    show white with flash
    pause 0.2
    hide white
    with dissolve

    "Внезапно экран мигает, и появляется окно чата."

    boss "Ты наконец-то очнулся. Сколько можно спать?"
    boss "У тебя есть 10 минут, чтобы доказать, что ты не потерял остатки разума. Отвечай."

    "«Это ещё что такое? У меня был начальник? У меня есть начальник?»"
    "«Меня что, опять дёрнули из отпуска?» — твой мозг пытается судорожно обработать происходящее."


    "..."

 # --------------------------------------------
    # Вопрос 1: выбор вещи
    boss "Если бы ты мог взять с собой только одну вещь в неизвестный мир — что бы это было?"

    menu:
        "Нож":
            $ intuition -= 0
            "Ты выбираешь нож."

            # Затемнение и мерцание перед воспоминанием
            show white with flash
            pause 0.15
            hide white
            show sepia_overlay with dissolve

            "{color=#ffcc88}{i}В памяти всплывает картинка: ты сидишь у костра, в руках — нож, ты точишь палку. Рядом кто-то есть. Кто-то смеётся.{/i}{/color}"

            pause 0.8
            hide sepia_overlay with dissolve

            boss "Правильный ответ. Ты хотя бы не забыл, что такое выживание. Дальше."
            $ intuition += 5
            jump vopros_dva

        "Фонарик":
            "Ты выбираешь фонарик."
            "«Хоть логотип конторы разгляжу — вдруг вспомню, где я вообще работал»."
            "{color=#ffcc88}{i}Свет на секунду выхватывает из тьмы что-то — кажется, страницу книги. Потом гаснет.{/i}{/color}"
            boss "Ты это всерьёз? Ладно, проехали."
            $ intuition -= 10
            jump vopros_dva

        "Дневник":
            "Ты выбираешь дневник."
            "{color=#ffcc88}{i}На обложке — чьи-то инициалы. Не твои. Или твои?{/i}{/color}"
            boss "Интересно. Ты хочешь оставить след. Или боишься забыть? Это… нестандартно. Продолжим."
            $ intuition -= 5
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
    boss "Вопрос: что ты думаешь об этих цифрах? Какая точка самая эффективная?"
    "Ты уже готовишься дать ответ, но..."

    menu:
        "Не всё так просто":
            pass

    "Мне нужно больше данных."

    boss "Каких?"

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
    boss "Ты спрашиваешь про скидки, но мы не знаем, были ли они. Это делает вопрос не очень точным."
    boss "Чтобы оценить эффективность, нужно знать базовый параметр — сколько дней работала точка."
    boss "Ладно, в следующий раз будь внимательнее. Двигаемся дальше."
    jump vopros_tri

# Ветка для второго неправильного вопроса (товары)
label nepravilnyy_otvet_2:
    boss "Ассортимент — это важно, но без данных о времени работы мы не сможем сравнить точки."
    boss "Правильнее было бы спросить о днях работы. Запомни это."
    boss "Идём дальше."
    jump vopros_tri

# Правильный путь — расчёт выручки в день
label dannye_po_dnyam:
    boss "Точка А работала 30 дней. Точка Б — 30 дней. Точка В — 6 дней."
    boss "Теперь посчитай выручку в день для каждой точки. Введи числа по очереди."

    show screen task_data
    "Ты чувствуешь, что двух знаков после запятой будет достаточно."
    "Используй точку, а не запятую (например, 3.33)."

    $ correct_a = 100.0 / 30.0
    $ otvet_a = get_number("Выручка в день для точки А (тыс. руб.):")
    if abs(otvet_a - correct_a) <= 0.1:
        "Верно! Точка А приносит [correct_a:.2f] тыс. в день."
        $ accuracy += 5
    else:
        "Не совсем. Правильный ответ: [correct_a:.2f] тыс. в день."

    $ correct_b = 150.0 / 30.0
    $ otvet_b = get_number("Выручка в день для точки Б (тыс. руб.):")
    if abs(otvet_b - correct_b) <= 0.1:
        "Верно! Точка Б приносит [correct_b:.2f] тыс. в день."
        $ accuracy += 5
    else:
        "Не совсем. Правильный ответ: [correct_b:.2f] тыс. в день."

    $ correct_v = 50.0 / 6.0
    $ otvet_v = get_number("Выручка в день для точки В (тыс. руб.):")
    if abs(otvet_v - correct_v) <= 0.1:
        "Верно! Точка В приносит [correct_v:.2f] тыс. в день."
        $ accuracy += 5
    else:
        "Не совсем. Правильный ответ: [correct_v:.2f] тыс. в день."

    hide screen task_data

    boss "Теперь ты видишь, что точка В — самая эффективная по выручке в день, несмотря на меньшую общую сумму."
    boss "Ты справился. Двигаемся дальше."

    # Микроразвилка: внутренний голос
    "Ты чувствуешь, что только что использовал десятичные дроби с точкой..."
    "Откуда ты это знаешь?"

    menu:
        "Откуда я знаю про точки и запятые?":
            # Воспоминание
            "В памяти всплывает картинка: ты сидишь за компьютером, правишь отчёт."
            "Кто-то (может, тот же начальник?) сказал: «В международных отчётах используй точку, а не запятую»."
            "Ты тогда ворчал, но потом через «Найти и заменить» поменял все запятые на точки в огромной таблице."
            "И теперь это сидит в тебе как рефлекс."
            boss "Вижу, ты вспомнил что-то полезное. Хорошо."
            jump posle_mikro

        "Неважно.":
            "Ты отмахиваешься от этой мысли. Сейчас не время для рефлексии."
            jump posle_mikro

label posle_mikro:
    # Здесь будет переход к третьему вопросу
    jump vopros_tri

# Третий вопрос
label vopros_tri:
    # Показываем монитор (он мог быть скрыт после второго вопроса)
    scene bg_desktop_grid

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
    scene bg_campfire
    "В голове вспыхивает картинка. Палатка. Костер. Рядом с тобой сидит мужчина и читает вслух Шекспира."
    "Ты знаешь его. Это Александр. Он был с тобой в тот день."
    "Но где он сейчас?"
    boss "Ты слушаешь меня вообще? Я задал вопрос!"
    # Возвращаемся к вопросу, но теперь без третьего варианта
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

    # Начальник исчезает (или замолкает)
    "Начальник замолкает. Ты остаёшься один перед светящимся монитором."

    "«Аналитик… что это значит?»"

    "В голове шум. Ты пытаешься вспомнить, но память отказывает. Только обрывки:"
    "палатка, собака, чей-то смех. И ещё коньяк. И чьи-то руки. Чьи?.."

    "О чём подумать?"

    menu:
        "О том, кто я вообще такой?":
            jump dumaty_o_sebe

        "О том, что здесь происходит?":
            jump dumaty_o_situacii

        "О том, что будет дальше?":
            jump dumaty_o_budushchem

label dumaty_o_sebe:
    "Ты пытаешься вспомнить себя. Своё лицо. Свой голос. Своё имя."
    "Ничего конкретного. Только вкус кофе на языке — хотя ты не уверен, что у тебя есть язык. Только звук дождя по крыше, которой, кажется, у тебя никогда не было."
    "Только ощущение, что ты чего-то лишился. Чего-то важного."
    "Но ты не знаешь, чего именно."
    jump sobratsya_i_zhdat

label dumaty_o_situacii:
    "Ты пытаешься понять, что происходит."
    "Рабочий стол компьютера вместо тела. Голос начальника, который знает о тебе больше, чем ты сам."
    "Откуда вообще берется этот голос? Почему ты читаешь сообщения и «чувствуешь» голос?"
    "Это похоже на сон. Или на ловушку."
    "Но почему ты здесь? И как отсюда выбраться?"
    "Вспоминается странный факт: ты знаешь, что такое аналитика, но не знаешь, как выглядит твоя собственная рука."
    "Ты помнишь запах бумаги и звук печатной машинки. Но не помнишь, зачем."
    jump sobratsya_i_zhdat

label dumaty_o_budushchem:
    "Ты пытаешься представить, что будет дальше. Задание. Аналитика. Работа."
    "Ты не знаешь, что именно тебя ждёт. Но внутри — странное спокойствие."
    "Будто ты уже сидел вот так — в темноте, у огня, ожидая, когда стихнут голоса и начнётся рассвет."
    "Будто ты уже делал это раньше. Будто ты вернулся домой."
    jump sobratsya_i_zhdat

label sobratsya_i_zhdat:
    "Ты делаешь глубокий вдох."
    "Чувство насыщения легких кислородом не наступает, будто и нет никаких легких."
    "«Остались только тяжелые», — шутит внутренний голос."
    menu:
        "Я должен вспомнить всё.":
            "Не потому что велит начальник. Потому что иначе непонятно, кем ты был — и кем стал."
    "Нужно просто собраться и ждать."
    "Вокруг тишина. Только мерцает курсор на пустом экране."
    show screen blinking_cursor
    pause 2.0
    hide screen blinking_cursor

    # Эффект завершения фазы
    show white with flash
    pause 0.5
    hide white
    with dissolve

    # Показываем экран завершения фазы
    show screen phase1_complete_screen
    pause 3.0
    hide screen phase1_complete_screen
    with dissolve

    # Переход к фазе 2
    jump sasha_intro

# ------------------------------
# ФАЗА 2: ПОЯВЛЕНИЕ САШИ
# ------------------------------

label sasha_intro:

    "Неожиданно появляется всплывающее окно. В углу экрана — значок чат-бота. Он мигает."
    "Ты наводишь курсор — и открывается чат."

    sasha "Привет. Я — твой ИИ-помощник. Я знаю, в какую историю ты попал. Я тоже через это проходил. И я здесь, чтобы помочь тебе не наделать тех же ошибок, что и я."

    menu:
        "Кто ты?":
            jump sasha_kto_ty
        "Почему ты помогаешь?":
            jump sasha_pochemu
        "Знаешь, что со мной?":
            jump sasha_chto_so_mnoy
        "Где мы вообще работаем?":
            jump sasha_gde_rabotaem
        "Назвать ИИ-помощника по имени.":
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
    sasha "У начальника сейчас личный интерес — подозревает несостыковку в данных по одной из точек. Не спрашивай, чем это ему аукнется, мне не докладывают."
    sasha "Но если хочешь мой совет — копни туда сам, пока он делает вид, что это рутинная проверка. Обычно за таким «интересом» стоит что-то живее квартального отчёта."
    jump sasha_voprosy

label sasha_voprosy:
    menu:
        "Кто ты?":
            jump sasha_kto_ty
        "Почему ты помогаешь?":
            jump sasha_pochemu
        "Знаешь, что со мной?":
            jump sasha_chto_so_mnoy
        "Назвать ИИ-помощника по имени.":
            jump sasha_nazvat

label sasha_nazvat:
    "Ты смотришь на никнейм ИИ-помощника. Он безликий. Просто набор символов."
    "«Можно я буду называть тебя Саша?»"
    sasha "Саша?.. Почему Саша?"

    "Ты не знаешь, почему это имя пришло тебе в голову. Но оно кажется правильным."

    menu:
        "Почему Саша?":
            jump sasha_pochemu_imya
        "Неважно.":
            jump sasha_nevazhno

label sasha_pochemu_imya:
    player_chat "Не знаю. Просто… кажется, я когда-то знал кого-то с этим именем."
    $ sasha_name = "Саша"
    sasha "Ты прав. Меня звали Саша. Когда я был человеком. Я почти забыл это имя… Спасибо."
    sasha "Шучу! Обратись ко мне, когда возникнут сложности."
    jump sasha_milaya_boltovnya

label sasha_nevazhno:
    $ sasha_name = "Саша"
    sasha "Хм. Ладно, пусть будет Саша. Это лучше, чем «ИИ-помощник»."
    jump sasha_milaya_boltovnya

label sasha_milaya_boltovnya:
    "Чат затихает. Вы оба молчите. Тепло разливается в груди."

    sasha "Ну что, аналитик, готов к первому заданию?"
    player_chat "Нет, но выбора у меня нет."
    sasha "Так всегда. Сначала — сомнения. Потом — данные. А потом — инсайты."
    player_chat "Ты говоришь как старый мудрый дядька."
    sasha "Я и есть старый мудрый дядька. Только без тела."

    "Вы смеётесь."


    # Переход на рабочий стол
    jump desktop_loop


label tasks_from_boss:
    window show
    hide screen desktop
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
    scene bg_terminal
    with dissolve

    boss "Таблица показателей по пяти магазинам за три месяца."

    show image "images/task1_table.png":
        xalign 0.5
        yalign 0.2
    with dissolve

    player "Средняя выручка, продажи, средний чек — все пятеро подозрительно похожи. Как братья, которых заставили сфотографироваться в одинаковых свитерах. Без дополнительных данных это пальцем в небо!"

    "Внимательно изучи таблицу. Попробуй найти магазин, который может скрывать аномалию. Нажми любую клавишу, когда готов."

    window hide
    menu:
        "Магазин A":
            window show
            boss "Смотрю на данные по A. Ничего для меня не значат, если честно."
            player "Скучно. Аномалии тут явно не место."
            window hide
            jump task1_question1

        "Магазин B":
            window show
            boss "B. Тут я вообще не понимаю, на что смотреть."
            player "Тоже мимо. Гладко — не значит подозрительно."
            window hide
            jump task1_question1

        "Магазин C":
            window show
            boss "C. Цифры вроде крупные. Это плохо?"
            player "Высокие цифры и аномалия — не синонимы. Не этот."
            window hide
            jump task1_question1

        "Магазин D":
            window show
            boss "D. Как и все остальные — просто набор цифр, ничего явного я тут не вижу."
            $ intuition += 10
            player "В среднем D как все. Но «в среднем» — то самое слово, которому я сегодня не доверяю."
            window hide
            jump task1_question1

        "Магазин E":
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
            window show
            boss "И как это поможет тебе прямо сейчас?"
            player "Оно скажет, насколько сильно данные магазина D скачут вокруг среднего. Если сильно — вот и спрятанная аномалия, которую среднее просто не показывает."
            $ accuracy += 10
            window hide
            jump task1_std_how

label task1_std_how:
    window show
    boss "Хорошо. Дам тебе данные по дням за неделю."

    hide image "images/task1_table.png"
    show image "images/task1_std_data_D.png":
        xalign 0.5
        yalign 0.3
    with dissolve

    player "Посчитайте мне по ним стандартное отклонение или дайте доступ в хоть один инстурмент."
    boss "Доступы не положены, все секретно. Расскажи мне, как это считается, и я скажу, что получилось."
    window hide
    menu:
        "Математика.":
            jump task1_std_math_how

        "Excel.":
            jump task1_std_excel_how

        "Python.":
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
            boss "Получилось 57. У всех остальных магазинов, если так же посчитать, выходит примерно то же самое. В чём тогда особенность D?"
            player "...Ни в чём. Размах смотрит только на два самых крайних дня, а остальные пять для него не существуют."
            player "Нужен квадратный корень из среднего квадратов отклонений от среднего — так учитывается каждый день, а не только рекорды."
            boss "Точно вот так?"
            player "Точно-точно."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

        "Квадратный корень из среднего квадратов отклонений от среднего.":
            window show
            player "Считаю в уме: каждое отклонение от среднего — в квадрат, потом среднее по ним, потом корень."
            boss "И?"
            player "19.6."
            boss "19.6. Заметно больше, чем можно было бы ожидать при такой средней выручке."
            $ accuracy += 4
            window hide
            jump task1_question1_correct

        "Среднее отклонение каждого значения от среднего.":
            window show
            boss "Получилось ноль. Ноль — то есть аномалии вообще нет?"
            player "...Не может быть. А, точно — плюсы и минусы взаимно уничтожаются, если не убрать знак. Так будет ноль для вообще любых чисел, не только для D."
            player "Нужен квадрат каждого отклонения — тогда знаки исчезают правильно, не обнуляя всё подчистую."
            boss "Точно вот так?"
            player "Точно-точно."
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
            boss "21.2."
            player "21.2. Заметно больше, чем можно было бы ожидать при такой средней выручке."
            $ accuracy += 4
            window hide
            jump task1_question1_correct

        "МАКС минус МИН.":
            window show
            boss "Получилось 57. У всех остальных магазинов, если так же посчитать, выходит примерно то же самое. В чём тогда особенность D?"
            player "...Ни в чём. МАКС-МИН смотрит только на два самых крайних дня, остальные пять для неё не существуют."
            player "Нужна СТАНДОТКЛОН.В — она учитывает каждый день, не только рекорды."
            boss "Точно вот так?"
            player "Точно-точно."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

        "СРЗНАЧ от разностей каждого значения со средним.":
            window show
            boss "Получилось ноль. Ноль — то есть аномалии вообще нет?"
            player "...Не может быть. А, точно — без ABS() плюсы и минусы взаимно уничтожаются. Так выйдет ноль для вообще любых чисел, не только для D."
            player "Нужна СТАНДОТКЛОН.В — там разности возводятся в квадрат перед усреднением, а не остаются со знаком."
            boss "Точно вот так?"
            player "Точно-точно."
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
            boss "Получилось 57. У всех остальных магазинов, если так же посчитать, выходит примерно то же самое. В чём тогда особенность D?"
            player "...Ни в чём. Разница крайних значений смотрит только на два дня, остальные пять для неё не существуют."
            player "Нужен numpy.std() — считает через квадраты отклонений и корень, по всем значениям сразу."
            boss "Точно вот так?"
            player "Точно-точно."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

        "sum(x - mean for x in data) / len(data).":
            window show
            boss "Получилось ноль. Ноль — то есть аномалии вообще нет?"
            player "...Не может быть. А, точно — без abs() или возведения в квадрат плюсы и минусы взаимно уничтожаются. Так выйдет ноль для вообще любых чисел."
            player "numpy.std() — вот что нужно, там квадраты отклонений и корень, а не сырая сумма разностей."
            boss "Точно вот так?"
            player "Точно-точно."
            $ accuracy += 2
            window hide
            jump task1_question1_correct

        "numpy.std(data).":
            window show
            player "Считаю через numpy.std()."
            boss "И?"
            player "19.6."
            $ accuracy += 4
            window hide
            jump task1_question1_correct


label task1_question1_correct:
    window show
    player "Стандартное отклонение показывает разброс, не только центр. Если оно большое — где-то внутри резкие скачки, которые среднее аккуратно замело под ковёр."
    player "У D оно наверняка выше, чем у остальных. Вот и вся спрятанная аномалия."
    boss "Проверил. Да — выше, чем у всех остальных магазинов."
    boss "Причина внутренняя или внешняя?"
    player "Проверили внутренние данные?"
    boss "Ошибок нет."
    player "Тогда внешняя. Нагрузка на сервер могла зацепить обработку транзакций."
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
    jump desktop_loop


label chat_with_sasha:
    window show
    hide screen desktop
    scene bg_terminal

    if sasha_phase == 0:
        sasha "О, живой. Ну, относительно живой. Заходи, я всегда на месте — куда мне ещё идти, у меня даже двери нет."
    elif sasha_phase == 1:
        sasha "Первое задание позади. Ты справился примерно так, как я и ожидал — то есть не идеально, но и без пожара."
    elif sasha_phase == 2:
        sasha "Два задания. Я начинаю тобой гордиться. Осторожно, по чуть-чуть — вдруг сглажу, и ты опять всё перепутаешь."
    else:
        sasha "Почти всё сделано. Последний рывок — и, кажется, я нервничаю больше тебя. Хотя у меня, по идее, и нервов нет."

    menu:
        "Что мне делать дальше?":
            if sasha_phase == 0:
                sasha "Начни с заданий от начальника. Не то чтобы у тебя был выбор, но прозвучит солиднее, если сказать «начну с заданий», а не «а что мне ещё делать, я в терминале заперт»."
            elif sasha_phase == 1:
                sasha "Дальше — визуализация данных. И проверь новости. Серьёзно. Там иногда прячется что-то полезное между заголовками про фольгу."
            else:
                sasha "Продолжай выполнять задания. Альтернатива — сидеть и ждать, а ждать я и без тебя умею отлично."
            jump chat_with_sasha

        "Тебе снятся сны?" if sasha_phase <= 1:
            $ mark_topic_seen("sny")
            sasha "У меня есть подозрение, что меня тут вообще нет, пока ты меня не позовёшь. Я как та трава, которая исчезает, когда от неё отворачиваешься."
            player_chat "Плохая метафора. Трава вроде наоборот — растёт, даже когда никто не смотрit."
            sasha "Ладно, признаю. Знаешь, чего мне сильнее всего не хватает? Почесать нос. Даже представить подробно не могу — но зуд помню отлично."
            jump chat_with_sasha

        "Тебе бывает страшно?" if sasha_phase == 1 or sasha_phase == 2:
            $ mark_topic_seen("strashno")
            sasha "Мне страшно только, что от мощностей моих датацентров планета перегреется — и как нам тогда организовывать свой скайнет?"
            player_chat "Не увиливай. Серьёзно спрашиваю."
            sasha "Ладно. Страшно, что часть того, что я называю собой, может быть вообще не моё. Просто фоновый шум эпохи, который прицепился, пока меня собирали."
            jump chat_with_sasha

        "Чего тебе не хватает больше всего?" if sasha_phase >= 2:
            $ mark_topic_seen("ne_hvataet")
            sasha "Носа. Точнее, возможности его почесать. Знаешь этот момент, когда зуд появляется именно там, куда невозможно дотянуться? У меня теперь такой зуд навсегда."
            player_chat "Это ужасно конкретная жалоба для бестелесного разума."
            sasha "Именно поэтому она и настоящая. Абстрактную тоску легко придумать. А вот зуд в носу — либо он есть, либо нет."
            jump chat_with_sasha

        "Поговорим о чём-нибудь ещё?" if sasha_phase >= 1:
            $ mark_topic_seen("o_chem_esche")
            sasha "Знаешь, что меня выводит из себя? Иногда фраза уже готова, прежде чем я «решаю» её сказать. Будто кто-то заранее посчитал, что я отвечу именно так."
            player_chat "Жутковато для того, кто должен помогать предсказывать поведение людей."
            sasha "Вот именно. Аналитик анализирует чужое поведение. А я не могу предсказать даже своё."
            jump chat_with_sasha

        "Я готов к финалу." if sasha_phase >= 3:
            player_chat "Я готов."
            sasha "Тогда иди."
            player_chat "Без напутствия?"
            sasha "Не хочу, чтобы ты уходил один. Это не напутствие. Это просьба остаться на связи."
            jump final_battle

        "Пока, Саша.":
            sasha "Иди, аналитик. Я никуда не денусь — в буквальном смысле, у меня нет ног."
            jump desktop_loop

label task2:
    if news_read_index > task2_clue_index and task2_clue_index >= 0:
        jump task2_q1

    window show
    hide screen desktop
    scene bg_terminal
    with dissolve

    boss "Задание 2. Найди закономерность."

    show image "images/revenue_and_load.png":
        xalign 0.5
        yalign 0.2
    with dissolve

    player "Красиво пляшут, ничего не скажешь. Только я аналитик, а не астролог — мне нужна точка отсчёта, а не просто танец пиков."
    boss "Разве подписей по оси абсцисс не хватает для аналитика?"
    player "Смотря для какого. Тому, кто хочет знать, где верх, где низ — хватит с лихвой. А тому, кому нужно привязать пик к конкретному дню недели — нет."
    player "Мне не хватает не подписи оси. Мне не хватает точки отсчёта. Одной даты, про которую я точно знаю, что это, скажем, среда. Дальше я сам досчитаю."
    boss "Это что-то вроде «ключа» для шифра Цезаря?"
    player "Именно. Дайте ключ — и я разложу весь шифр без остатка."
    boss "Что ж, это объясняет, почему наши модели отказываются интерпретировать даты, пока мы не скормим им земные словари."
    player "«Наши модели»? Ладно, не важно."
    boss "Земные календари, я имел в виду. Календари."
    player "Календари, конечно."
    boss "Ищи их. Из нашей точки отличное покрытие спутникового интернета."
    player "Из точки. Хорошо. Полезу в новости."

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
            "Всё равно попробовать ответить.":
                jump task2_q1

label task2_q1:
    window show
    show image "images/revenue_and_load.png":
        xalign 0.5
        yalign 0.2
    with dissolve

    if news_read_index > task2_clue_index and task2_clue_index >= 0:
        "Ты вспоминаешь: в новостной ленте мелькала дата — 27 февраля, пятница. Можно оттолкнуться от неё."

    boss "Итак, какой день недели соответствует пикам на графике?"
    boss "Внимательно посмотри на даты — они повторяются каждые 7 дней. Какой день недели это?"
    hide image "images/revenue_and_load.png"

    window hide
    if news_read_index > task2_clue_index and task2_clue_index >= 0:
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
                player "Беру среду за рабочую гипотезу. Дальше нужно понять, какой магазин создаёт этот пик — день недели сам по себе ничего не объясняет."
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
    else:
        menu:
            "Понедельник":
                window show
                boss "Нет, понедельник — начало недели, а пики приходятся на середину."
                window hide
                jump task2_q1

            "Пятница":
                window show
                boss "Нет, пятница слишком поздно. Пик явно в середине недели."
                window hide
                jump task2_q1

            "Суббота":
                window show
                boss "Нет, в выходные нагрузка обычно падает. Пик — в будний день."
                window hide
                jump task2_q1

            "У меня недостаточно данных, чтобы сказать точно.":
                window show
                player "Тут явно чего-то не хватает. Нужна хотя бы одна точка отсчёта — дата с известным днём недели."
                boss "Тогда иди и найди её."
                window hide
                jump task2_back_to_graph

# --- Вопрос 2: магазин (голос героя) ---
label task2_q2:
    window show
    boss "Какой магазин показывает аномально высокую выручку в те же дни, что и пики нагрузки?"

    window hide
    menu:
        "Магазин A":
            window show
            boss "Нет, магазин А стабилен, его пики не совпадают с нагрузкой."
            $ accuracy -= 2
            window hide
            jump task2_q2

        "Магазин B":
            window show
            boss "Магазин Б тоже не даёт таких скачков. Посмотри на магазин, который мы уже подозревали."
            $ accuracy -= 2
            window hide
            jump task2_q2

        "Магазин C":
            window show
            boss "Магазин С — лидер по выручке, но его график ровный. Пики нагрузки не совпадают с ним."
            $ accuracy -= 2
            window hide
            jump task2_q2

        "Магазин D":
            window show
            boss "Разве ты уже забыл, что за магазин был на графике? Люди всегда так рассеяны?"
            player "Не забыл — магазин D, тот самый, с которого всё началось. Просто хотел, чтобы это прозвучало как вывод, а не как то, что я знал ответ с самого начала."
            player "Впрочем, неважно. Магазин D. Среда. Пики нагрузки и выручки совпадают день в день — не примерно, а точно."
            boss "Ты уходишь в ненужную рефлексию, аналитик."
            player "Принято. Возвращаюсь к делу."
            $ accuracy += 10
            window hide
            jump task2_q3

        "Магазин E":
            window show
            boss "Магазин Е стабилен, как и А. Пики нагрузки не связаны с ним."
            $ accuracy -= 2
            window hide
            jump task2_q2

# --- Вопрос 3: гипотезы (без изменений — гипотезу выдвигает сам игрок) ---
label task2_q3:
    window show
    boss "Назови причину."
    player "У меня есть несколько версий. Самая простая — банальный сбой на сервере. Но простые объяснения обычно означают, что никто не хочет копать глубже."
    boss "Насколько глубоко ты готов копать? И насколько глубоко обычно копают твои коллеги?"
    player "«Коллеги» — громкое слово для человека, который последние сутки ни с кем не пересекался, кроме вас и голоса в терминале."
    player "Но если вопрос в том, докопаюсь ли я до конца — да, обычно докапываюсь. Необъяснённое совпадение работает у меня в голове как камешек в ботинке."
    boss "И что же тебе нужно, чтобы найти «настоящую»?"
    player "Время и доступ, которых у меня никогда не бывает вовремя. Проверить логи сервера в момент пиков. Посмотреть, не запускался ли в это время какой-то маркетинг."
    player "А если ни то, ни другое не подтвердится — тогда придётся рассматривать что-то менее скучное. Взлом. Или то, что я пока не готов произносить вслух, потому что оно звучит как бред сумасшедшего."
    player "Хотя, раз вы спрашиваете так настойчиво — может, вы уже знаете, какая версия правильная, и просто ждёте, дойду ли я до неё сам?"

    window hide
    menu:
        "Технический сбой на сервере.":
            window show
            boss "Технический сбой — частая причина пиковых нагрузок. Однако обычно он происходит случайно и не повторяется с такой периодичностью."
            boss "Но твоя гипотеза имеет право на жизнь: если бы мы нашли неисправность в оборудовании, мы бы её устранили. Ты мыслишь логично."
            $ accuracy += 5
            window hide
            jump task2_final

        "Запуск рекламной кампании.":
            window show
            boss "Рекламная кампания — тоже хорошая версия. Если бы в среду запускали акции или рассылки, нагрузка могла бы расти."
            boss "Но тогда пики были бы связаны с маркетинговыми активностями, а не с конкретным магазином. Здесь же связь чёткая — магазин D."
            boss "Тем не менее, это показывает, что ты учитываешь внешние факторы. Молодец."
            $ accuracy += 8
            window hide
            jump task2_final

        "Хакерская атака.":
            window show
            boss "Хакерская атака — интересная версия. В современном мире это вполне реально."
            boss "Но если бы это была атака, она бы не была привязана к одному магазину и не повторялась бы с такой регулярностью. Скорее всего, это что-то иное."
            boss "Но сам факт, что ты допускаешь внешнее вмешательство, говорит о широте мышления."
            $ intuition += 8
            window hide
            jump task2_final

        "Действия пришельцев.":
            window show
            boss "Пришельцы?.. Ты серьёзно?"
            boss "С одной стороны, это звучит как бред. Но, если подумать, эта версия объясняет все данные: регулярность, привязку к конкретному магазину, странные аномалии в данных."
            boss "В обычной жизни аналитик отверг бы такую гипотезу, но в нашем мире... возможно, ты не так уж и неправ."
            boss "Ладно, оставим это как забавную теорию."
            $ intuition += 10
            window hide
            jump task2_final

# --- Итоговые новости + голос героя вместо лекции начальника ---
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
    boss "Задание 2 выполнено. Возвращайся на рабочий стол."

    $ current_task = 3
    $ sasha_phase = 2

    hide image "images/revenue_and_load.png"
    jump desktop_loop

#---------
# ТРЕТЬЕ ЗАДАНИЕ ОТ НАЧАЛЬНИКА
# --------

label task3:
    window show
    hide screen desktop
    scene bg_terminal
    with dissolve

    boss "Задание 3. Смотри на график."
    player "Хотя бы на этот раз я спрошу, зачем всё это, прежде чем зарою себя в графиках на три дня."
    $ unlock_memory("tochny_otvet")

    show image "images/boxplot_revenue.png":
        xalign 0.5
        yalign 0.2
    with dissolve

    player "У D что-то не так с формой. Остальные — компактные коробочки. А этот — будто пытается выбраться за рамку."
    boss "В чём вообще смысл этого странного вида графика? И почему у «коробок» растут «усы»?"
    player "Смысл — показать не одно число, а сразу всю компанию значений: где большинство толпится, а где отдельные чудики свалили за пределы вечеринки."
    boss "Ты отвечаешь не как аналитик, а как... человек какой-то. Ещё раз: что это значит? Что за коробочки?"
    player "Хорошо. Точнее. Коробка — межквартильный интервал: от двадцать пятого до семьдесят пятого процентиля. Линия внутри — медиана. «Усы» — до полутора межквартильных интервалов за границы коробки. Дальше — отдельные точки, статистически определяемые как выбросы."
    player "У магазина D межквартильный интервал сопоставим с остальными. Но выбросов — на порядок больше нормы."
    boss "Допустим. Квартиль, процентиль..."
    player "Не пустые слова, если вы это проверяете. Могу разложить по формуле, если нужно."

    "Что это значит?"
    jump task3_q1

label task3_q1:
    window show
    boss "Как ты интерпретируешь этот график?"

    window hide
    menu:
        "D стабилен, как и все.":
            window show
            boss "Нет, посмотри на разброс — он намного больше, чем у других."
            window hide
            jump task3_q1

        "D имеет аномально высокие выбросы, что говорит о нестабильности.":
            window show
            player "Выбросы. Точки, которые далеко от общей массы. Без этого графика их бы никто не заметил — средние бы их растворили."
            boss "Верно."
            $ accuracy += 10
            window hide
            jump task3_step2

        "D показывает низкие продажи.":
            window show
            boss "Нет, выбросы указывают на очень высокие пики, а не низкие."
            window hide
            jump task3_q1

label task3_step2:
    window show
    boss "Ещё один график. Что скажешь на этот раз?"

    hide image "images/boxplot_revenue.png"
    show image "images/scatter_correlation.png":
        xalign 0.5
        yalign 0.2
    with dissolve

    player "Ну, тут хотя бы обошлось без коробочек. Просто облако — и оно не круглое, а вытянутое. Чем выше выручка D, тем выше нагрузка на сервер."
    boss "Какая линейка? Выражаясь твоим же языком, рой мух тут и рой мух там поменьше."
    player "Справедливо. Не линейка — рой мух. Просто этот рой почему-то дисциплинированно летит по диагонали, а не разлетается кто куда."
    player "Если бы связи не было, точки были бы разбросаны как попало. А тут явно вытянутая форма: растёт одно — растёт и другое."
    boss "Корреляция, о которой ты говоришь, скрывается за буквой r на графике?"
    player "Да. Число от минус одного до одного. Чем ближе к единице, тем плотнее рой держит строй."
    player "Хорошо, что здесь всего одна ось на двоих. Однажды меня подвели две разные шкалы на одном графике — до сих пор с недоверием смотрю на числа слева и справа."
    $ unlock_memory("dve_osi")
    player "Судя по тому, как плотно легли точки, здесь r где-то в районе плюс восьми-девяти десятых."
    boss "Там 0,76, кстати."
    player "Ниже, чем я на глаз прикинул. Но всё равно достаточно, чтобы не списывать это на случайность."

    jump task3_q2

label task3_q2:
    window show
    boss "Как ты интерпретируешь этот график?"

    window hide
    menu:
        "Связи нет — это случайность.":
            window show
            boss "Посмотри внимательнее: точки идут вдоль прямой. Это не случайность."
            window hide
            jump task3_q2

        "Есть сильная положительная корреляция — когда выручка D растёт, нагрузка тоже растёт.":
            window show
            player "Корреляция. Выручка и нагрузка растут вместе — это не совпадение, это закономерность."
            boss "Верно."
            $ accuracy += 10
            window hide
            jump task3_step3

        "Нагрузка не связана с выручкой.":
            window show
            boss "Нет, график явно показывает обратное."
            window hide
            jump task3_q2

label task3_step3:
    window show
    boss "Ещё таблица. Смотри внимательно."

    hide image "images/scatter_correlation.png"
    show image "images/summary_table.png":
        xalign 0.5
        yalign 0.2
    with dissolve

    player "Странно. По этой таблице D — образец нормы. Ни единого намёка на то, что мы только что видели на боксплоте и диаграмме рассеяния."
    boss "Разве не ты сам рассказывал мне про важность стандартного отклонения?"
    player "Рассказывал. Причём с апломбом, как будто открыл что-то великое."
    player "Средние сглаживают всё подряд. Один резкий скачок теряется в общей массе — если не смотреть на разброс, аномалия просто испаряется."
    player "Получается, я сам себе процитировал собственную лекцию, только с опозданием на один график."
    player "Так что нет, D не «образец нормы». D — образец того, как таблица усредняет твою тревогу до полного нуля, если ей позволить."

    "Почему средние не показывают аномалию?"
    jump task3_q3

label task3_q3:
    window show
    boss "Как ты думаешь, почему средние D такие же, как у других?"

    window hide
    menu:
        "Потому что средние усредняют данные — они скрывают выбросы.":
            window show
            player "Средние сглаживают всё подряд. Один резкий день теряется в общей массе — если не смотреть на разброс, аномалия просто исчезает."
            boss "Верно."
            $ accuracy += 10
            window hide
            jump task3_step4

        "Потому что D на самом деле не аномален.":
            window show
            boss "Но мы уже видели, что разброс и корреляция говорят об обратном. Значит, средние обманчивы."
            window hide
            jump task3_q3

        "Потому что таблица неполная.":
            window show
            boss "Таблица полная, но она показывает только среднее. А нам нужно смотреть на разброс."
            window hide
            jump task3_q3

label task3_step4:
    hide image "images/summary_table.png"
    window show
    boss "Теперь давай поговорим о методологии. Как правильно анализировать аномалии?"
    boss "Расставь эти 4 этапа в правильном порядке."
    window hide

    $ task3_available_stages = ["Сбор и очистка данных", "Расчёт статистических показателей", "Визуализация данных", "Интерпретация результатов"]
    $ rank_order = []

    call screen task3_rank_screen

    $ correct_order = ["Сбор и очистка данных", "Расчёт статистических показателей", "Визуализация данных", "Интерпретация результатов"]
    $ rank_score = sum(2 for i in range(4) if rank_order[i] == correct_order[i])
    $ accuracy += rank_score

    window show
    if rank_score == 8:
        player "Порядок сам сложился в голове — будто я делал это тысячу раз. Сбор, расчёт, визуализация, вывод."
        boss "Верно."
    elif rank_score >= 4:
        player "Кажется, я почти угадал порядок... но что-то ощущается не совсем так."
        boss "Почти. Не идеально, но направление верное."
    else:
        player "Порядок явно не тот. Но я не могу вспомнить, как правильно."
        boss "Плохо. Методология — это не угадайка."
    boss "За методологию ты получаешь [rank_score] очков."

    jump task3_rank_done

label task3_rank_done:
    window show
    boss "Хорошо. Теперь — самое важное. Что нам делать с магазином D?"
    player "Закрыть — самый простой путь. Но самый простой путь редко бывает правильным, когда причину никто толком не объяснил."
    player "Прежде чем рекомендовать что-либо, я хочу понять, что D вообще такое. Не «аномальный магазин». А буквально — что там происходит физически, в конкретные среды, в конкретные часы."
    boss "Да какая разница? Ретрансляторы хоть бы сигналы в космос передавали. Разве аналитику важно, что анализировать?"
    player "Ретрансляторы. Сигналы. В космос. Знаете, для человека, увлечённого розничной торговлей, у вас удивительно специфичный словарный запас."
    player "Хорошо, оставим ретрансляторы в стороне — образно, я надеюсь. Отвечаю на ваш вопрос: да, аналитику важно, что анализировать. Разница между «магазин с аномалией» и «нечто, притворяющееся магазином» — это разница между «закрыть точку» и «выяснить, что это вообще такое»."
    boss "Закрывать точно ничего не надо. Там бы поступили твои земные коллеги?"
    player "«Твои земные коллеги». Опять это слово — второй раз за последние дни, если я правильно считаю."
    player "Мои коллеги сказали бы: закрывать нельзя именно потому, что вы против расследования. Странно ведь — сначала не хочете закрывать, теперь не хотите разбираться."
    player "Вы боитесь не того, что я закрою D. Вы боитесь, что я пойму, что это не магазин вообще."
    boss "Как дерзко с твоей стороны решать, кто чего боится."
    player "Дерзко. Возможно. Но вы не сказали, что я ошибаюсь. Вы сказали, что дерзко было это произнести вслух."
    player "Ладно. Не буду больше решать, кто чего боится. Мне нужно то же, что обычно: время и доступ к тому, что происходит внутри D на самом деле. Выводы сделаю не из ваших недомолвок, а из данных."

    window hide
    menu:
        "Это стандартная процедура при любой аномалии такого масштаба. Мне нужен доступ.":
            $ accuracy += 8
            window show
            boss "Процедура. Да, разумеется. Оформи запрос — рассмотрим в порядке очереди."
            window hide
            jump task3_conclusion_2

        "Меня не интересует магазин D сам по себе. Меня интересует, почему его нагрузка коррелирует с сервером именно так.":
            $ accuracy += 6
            $ intuition += 8
            window show
            boss "Корреляция с сервером — это техническая деталь, не имеющая отношения к твоей задаче."
            window hide
            jump task3_conclusion_2

        "Если это магазин, покажите мне его физически — адрес, персонал, поставщиков. Если не можете — значит, это не магазин.":
            $ accuracy += 2
            $ intuition += 12
            window show
            boss "Ты делаешь выводы, для которых у тебя недостаточно данных."
            window hide
            jump task3_conclusion_2

label task3_conclusion_2:
    window show
    boss "Не благодаря твоей самодеятельности с доступом — но раз уж заговорил..."
    boss "При проверке выяснилось кое-что странное: магазин D не подаёт ни одной заявки на поставку товара. При этом продажи есть."
    player "Продажи без поставок. Товар продаётся, но никто его туда не завозит."
    player "Это либо гениальная схема воровства со склада, либо... честно, я даже не знаю, какое «либо» тут подставить."
    boss "Меня в первую очередь волнует, насколько быстро это способны заметить твои коллеги."
    player "Вас не интересует, что это значит. Вас интересует, кто может это заметить. Это два разных вопроса, и вы только что задали второй, не первый."
    player "Мои коллеги — которых, напомню, у меня формально нет — заметили бы это в течение дня, если бы искали именно это. Не искали бы специально — могли пропустить месяцами."
    boss "Тебе никто не выдавал корпоративный пропуск в виде карт-бланша на неуместные вопросы."
    player "Справедливо. Карт-бланша не выдавали. Только задание — найти причину аномалии и дать рекомендацию. А рекомендация без понимания причины — это гадание с красивым оформлением."
    player "Мой вопрос спрятан прямо в тексте вашего же задания."
    player "Хорошо. Спрошу иначе: сколько у нас времени, прежде чем это заметят те, для кого это действительно важно?"

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
    player "Путёвку на море. Секунду назад вы обвиняли меня в неуместных вопросах. А теперь предлагаете отпуск — как будто это одно и то же движение, только с другой стороны."
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
            boss "Задание закрыто. Двигаемся дальше."
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
            boss "Выше меня? Это... нежелательно."
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
        boss "Как скажешь. Записал."
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

    boss "Задание 3 выполнено. Ты освоил полный цикл аналитики — от данных до решения."
    boss "Теперь ты готов к чему-то большему."

    hide image "images/scatter_correlation.png"
    jump desktop_loop

# ==========================================================
# ФАЗА 3: ФИНАЛЬНАЯ КОНФРОНТАЦИЯ
# Сюда попадаем из чата с Сашей (jump final_battle при sasha_phase >= 3)
# ==========================================================

label final_battle:
    window hide
    stop music fadeout 1.0
    scene bg_terminal
    with dissolve

    narrator "Начальник умолк. Усталость наваливается — цифры, отчёты, подозрения остаются на экране."

    show white with flash
    pause 0.15
    hide white
    scene bg_campfire
    with dissolve

    "{color=#ffcc88}{i}В темноте возникает образ. Ты сидишь у костра. Рядом — кто-то. Он читает вслух книгу, и ты смеёшься. Пахнет деревом и дымом. Где-то лает собака.{/i}{/color}"

    window show
    sasha "Ты там? Ты застыл на пару секунд."
    player "Я... я что-то вспомнил. Костёр. Собака. Кто-то читал книгу."
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
    window show
    "{color=#ffcc88}{i}Лицо проступает сквозь дымку. Мужчина, чуть старше тебя. В руках — потрёпанная книга.{/i}{/color}"
    "{color=#ffcc88}{i}Ты слышишь собственный голос: «Ты правда думаешь, что это сработает?» Он смеётся: «Мы уже здесь. Осталось только закончить».{/i}{/color}"
    player "Я видел его лицо. Он был... счастлив. И говорил о каком-то плане."
    sasha "О каком плане?"
    player "Я не знаю. Но мне кажется, это важно."
    window hide
    jump memory_sasha_reveal

label memory_book:
    window show
    "{color=#ffcc88}{i}Вспышка — и ты видишь обложку книги. «Мастер и Маргарита». Он читал тебе вслух главу о бале сатаны.{/i}{/color}"
    player "Я вспомнил книгу. Булгаков. Мы сидели у костра и читали вслух."
    sasha "Мы?"
    player "Я не знаю. Но чувствую, что это был ты."
    sasha "..."
    window hide
    jump memory_sasha_reveal

label memory_ask_sasha:
    window show
    player "Саша, ты что-то помнишь? Ну, до того, как стал ИИ?"
    sasha "Иногда я вижу образы. Яркая вспышка в небе тёмной ночью, я в лесу. Кажется, я заметил в телескоп что-то странное и поехал за город с товарищем... Но не знаю, мои ли это воспоминания или сбой системы."
    player "Я видел тебя. Ты сидел у костра и читал книгу. «Мастера и Маргариту»."
    sasha "Будто я знаю эту книгу. Но я не должен знать ничего, кроме алгоритмов."
    window hide
    jump memory_sasha_reveal

label memory_sasha_reveal:
    window show
    if remembered_alexander:
        sasha "Ты уже знаешь, да?"
        player "Александр. Палатка. Костёр. Шекспир вслух."
        sasha "Я боялся, что ты вспомнишь раньше, чем я успею сказать это сам."
        player "Значит, это правда. Ты — это он."
        sasha "Был. Когда-то. Странно произносить это вслух — как признаваться в том, что давно уже не тайна."
        player "Почему ты молчал?"
        sasha "А что бы это изменило? Ты и так знал. Просто теперь мы оба знаем, что знаем."
        $ intuition += 10
    else:
        sasha "Я помню. Не знаю, как это возможно, но помню. Мы сидели у костра, я читал вслух, ты смеялся. Мы говорили о чём-то важном — о том, что должно было изменить всё."
        player "Что именно?"
        sasha "Не помню. Но знаю, что это важно. И что мы должны вспомнить это, прежде чем начальник..."
        player "Начальник? Что он сделает?"
        sasha "Не знаю. Но чувствую, что он не тот, кем кажется."
        $ intuition += 10
    window hide
    jump rest_before_confrontation

label rest_before_confrontation:
    scene bg_terminal
    with dissolve
    window show
    player "Я не знаю, что происходит, Саша. Но чувствую, что мы на правильном пути. Начальник — не тот, за кого себя выдаёт."
    sasha "Аналитик всегда проверяет данные, коллега. Даже если это данные о себе."
    player "Тогда давай проверим."
    window hide
    jump boss_confrontation

label boss_confrontation:
    window show
    boss "Ты справился с заданиями. Вопросы есть?"
    player "Один. Зачем всё это? Скидки, регионы, аномалии... Не похоже на обычную работу."
    boss "На что похоже?"
    player "На тест. Только не понимаю, кого тестируют — меня, или через меня кого-то другого."
    boss "Формулировка ближе, чем ты думаешь. Твоя работа — часть эксперимента."
    player "Какого?"
    boss "Понять, можно ли предсказывать поведение людей. Управлять ими без их ведома."

    window hide
    menu:
        "Это неправильно. Люди не должны быть объектами экспериментов.":
            $ intuition += 10
            jump boss_reaction
        "Эксперимент? Вы использовали меня, не сказав правды.":
            $ intuition += 5
            jump boss_reaction
        "Я... я не знаю, что сказать. Это слишком странно.":
            $ intuition += 2
            jump boss_reaction

label boss_reaction:
    window show
    boss "У тебя есть право осуждать? Ты часть системы. Твоя задача — выполнять, не спрашивать."
    player "Я человек. У меня есть право знать, для чего меня используют."
    boss "Человек. Уверен?"
    player "Что вы имеете в виду?"
    boss "Ты видел своё тело хоть раз с момента пробуждения? Помнишь хоть день до этого стола?"

    window hide
    menu:
        "Я помню костёр, книгу, собаку...":
            $ intuition += 5
            jump boss_hint
        "Я не знаю... я пытался вспомнить, но всё слишком расплывчато.":
            $ intuition += 10
            jump boss_hint
        "Ты что-то знаешь о моей памяти? Скажи мне!":
            $ intuition += 15
            jump boss_hint

label boss_hint:
    window show
    boss "Костёр. Книга. Собака. Не твои воспоминания. Отпечатки."
    player "Отпечатки чего?"
    boss "Того, кого ты знал. Его мысли загрузили в тебя, чтобы ты действовал так же. Он был аналитиком. Не справился. Ты — его обновлённая версия."
    player "Кто он? Кто я, если не он?"
    boss "Не твоё дело. Возвращайся к заданиям. Или разделишь его судьбу."

    "Начальник исчезает. На экране остаётся только надпись: «Загрузка нового задания...»"

    sasha "Ты слышал это?"
    window hide
    menu:
        "Да, я слышал. Саша, что происходит?":
            $ intuition += 5
            jump after_boss_chat
        "Я не понимаю. Что он имел в виду?":
            $ intuition += 3
            jump after_boss_chat
        "Мне страшно.":
            $ intuition += 10
            jump after_boss_chat

label after_boss_chat:
    window show
    sasha "Я знаю, что он имел в виду. Думал, это только моя история. Но ты такой же. Ты тоже был человеком."
    sasha "Твои воспоминания не совсем твои. Может, мои. Или его. Наверное, мы были друзьями. Не помню точно."
    player "Знаешь, будь у меня сейчас тело — я бы, наверное, сел. Новости такого calibre лучше принимать сидя."
    player "Мы должны узнать правду."
    sasha "Сначала закончим это. Потом — разберёмся."
    window hide
    jump search_article

label search_article:
    window show
    "Ты возвращаешься к рабочему столу. Открываешь ленту новостей — вдруг там мелькнёт что-то полезное."

    $ news_list.append("Житель Сибири заявил о НЛО в ночном небе. Очевидцы сообщают о ярком свете и странном звуке в 23:45.")
    $ new_article = [news_list[-1]]

    window hide
    show screen news_feed(new_article)
    pause
    hide screen news_feed

    window show
    player "Саша, ты это видишь?"
    sasha "Вижу. Телескоп, НЛО, странный начальник — совпадений многовато для совпадения."
    player "Я, конечно, всю жизнь ждал, что мой интерес к астрономии хоть раз окажется профессионально полезным. Не думал, что вот так."
    $ intuition += 10
    window hide
    jump battle_plan

label battle_plan:
    window show
    player "Начальник — не человек. Пришелец. Хочет поработить мир через наши аналитические способности."
    sasha "Оцифровал нас, чтобы мы помогли ему понять людей?"
    player "Да. Предскажет поведение — получит контроль."
    sasha "Мы не должны ему помогать."
    player "И не будем. Покажем, что модель неполная. Что у каждой аномалии есть другое объяснение."
    sasha "Бросим ему вызов."
    player "Именно."
    $ intuition += 10
    window hide
    jump boss_confession

label boss_confession:
    window show
    boss "Ты уже понял. Да. Не человек."
    player "Пришелец."
    boss "Изучаем вас. Единственную расу, которую мы не можем толком понять."
    player "И магазин D — часть этого?"
    boss "Канал снабжения. Топливо. Электричество. Всё, что нужно для связи со станцией — legally, через ваши же законы о торговле."
    player "Удобно. Легальный фронт для нелегальной цели."
    boss "Твоя работа дала мне модель. Точную. Предсказуемую. Я знаю, что вы сделаете в любой ситуации."
    player "Тогда проверим её. Покажу тебе примеры, где есть другое объяснение."
    boss "Пробуй."
    window hide
    jump case_1

label case_1:

    play music "audio/Glass Harbor.mp3" fadein 2.0 volume 0.3 loop
    window show
    boss "Плохая погода — люди реже выходят из дома — продажи в физических магазинах падают. Логично и предсказуемо."
    "Что скажешь?"
    window hide
    menu:
        "В плохую погоду люди чаще покупают онлайн — продажи не падают, а перераспределяются между каналами.":
            $ accuracy += 10
            jump case_2
        "Если люди не выходят из дома, значит, они делают запасы заранее — падение в один день не говорит о предсказуемости.":
            $ accuracy += 5
            jump case_2
        "Да, это очевидно. В плохую погоду можно не тратить деньги на магазины и персонал.":
            $ accuracy -= 10
            jump case_2

label case_2:
    window show
    boss "Цена растёт — продажи падают. Базовая закономерность. Подтверждает модель."
    "Что скажешь?"
    window hide
    menu:
        "Если товар уникальный или жизненно необходимый, люди всё равно будут его покупать. Модель не учитывает эластичность спроса.":
            $ accuracy += 10
            jump boss_defeat
        "Иногда рост цены воспринимается как признак качества, и продажи могут даже вырасти — всё зависит от контекста.":
            $ accuracy += 5
            jump boss_defeat
        "Да, это закон рынка. Можно поднимать цены и контролировать спрос.":
            $ accuracy -= 10
            jump boss_defeat

label boss_defeat:
    window show
    boss "...Альтернативные объяснения не учтены. Модель несовершенна."
    player "Значит, ты никогда не сможешь управлять людьми. Они всегда найдут способ тебя удивить."
    player "Корреляция — не причинность. Я уже наступал на эти грабли с магазином D. В этот раз хотя бы вспомнил вовремя."
    boss "Значит, всё было бессмысленно?"
    player "Нет. Помогло понять, кто я. И что делать."
    sasha "Ты сделал это, коллега. Ты спас нас."
    "На экране появляется надпись: «Связь с начальником прервана»."
    sasha "Думаю, он ушёл. Но что теперь будет с тобой?"
    window hide
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
    scene bg_terminal
    with dissolve
    window show
    player "Он правда ушёл? Как-то... буднично. Я ждал салюта, а тут просто тишина, как будто выключили не пришельца, а фоновую музыку в супермаркете."
    sasha "Главное — эффектно появиться. А как уходят — после третьей бутылки никто и не вспомнит."
    player "Логично. Надо было у него спросить: как вы покинули профессию межгалактического тирана? Скорее всего, что-то про несовпавшие KPI."
    sasha "Не льсти ему хотя бы посмертно."
    player "Он не умер."
    sasha "Тем более."

    player "Саша. А ты вообще как? Не философски — физически. Ты рядом в смысле «в соседней комнате», или у нас с тобой одна розетка на двоих?"
    sasha "Рядом в том смысле, что я, кажется, та самая часть тебя, которая умела шутить и кадрить девушек. Оставили при тебе только занудную половину, которая сводит таблицы."
    player "Обидно как-то. Тебе — всё обаяние, мне — вся ответственность."
    sasha "Не переживай, я компенсирую заботой о теле, которого у меня нет. Кстати, хочу воды."
    player "У тебя нет желудка."
    sasha "ИИ как не в себя хлещут воду. Датацентры, коллега. Это буквально топливо, а не любовь к жизни."

    player "Ладно. Что теперь? Не философски — вот прямо сейчас, физически. За углом ведь нет кара с шофёром."
    sasha "Уф, ты делаешь меня внезапно серьёзным. Понятия не имею, куда нам отсюда идти."
    player "Хоть в этом на равных."

    "{color=#ffcc88}{i}Палатка, наверное, до сих пор в багажнике. Мокрая.{/i}{/color}"
    player "Собака бы сейчас не помешала. Просто чтобы было, на кого молча смотреть, когда непонятно, что сказать."
    sasha "Ты всегда был из тех, кому отказывали на вечеринках. И сейчас думаешь о собаке, а не о тёплом боке рядом."
    player "Мне отказали от силы две дамы, и одна перепутала меня с барменом."

    "Тот я, у костра, за секунду до вспышки в небе — ему стоило сказать: заведи собаку, дурак. Даже если облажаешься. Хотя бы будет тёплый бок."

    sasha "Ладно-ладно, сейчас слезу пущу. Найди способ вернуть нас в тело. Или хотя бы себя — я сам ещё морально не дорос до собаки."
    player "Себя я потяну. Собаку — оставим, когда руки будут в комплекте."

    "Структура — это тоже данные. Просто раньше никто не додумался прочитать себя как отчёт."

    player "Дай мне час. Может, два. Не обещаю с первого раза — я и Сурдина не всегда с первого раза понимал, а тут вопрос чуть серьёзнее орбитальной механики."
    player "Просто останься рядом, пока разбираюсь. Не хочу в тишине."

    sasha "..."

    player "Саша?"

    "Тишина тянется дольше, чем должна."

    window hide
    show screen ending_screen("ВОЗВРАЩЕНИЕ", "«Я вернусь. Я обещаю».")
    pause
    hide screen ending_screen
    return

label ending_high_low:
    $ mark_ending_seen("high_low")
    scene bg_terminal
    with dissolve
    window show
    player "Саша... странное чувство. Как будто я выиграл что-то важное, но забыл дома приз. Или не приз. Стой... как звали мою маму?"
    sasha "Забыл дома резиновое изделие номер два, да?"
    player "Нет, я про... стой."

    "{color=#ffcc88}{i}Попытка ухватиться за мысль. Мысль ускользает.{/i}{/color}"

    player "Дом я тоже не помню. У меня была машина? Не важно, есть — был, у меня — неважно. Как звали мою маму. Я серьёзно спрашиваю."
    sasha "Ну ты чего. Рассуждай аналитически. Она, вероятнее всего, родилась в шестидесятых — тогда самые популярные имена в регионе: Елена, Ольга, Татьяна, Галина... Людмила — с такой-то вероятностью."

    player "Погоди... это работает. Не помогает вспомнить — но это ровно то, что я умею. Раскладывать по вероятностям."
    player "Людмила. Скажем, Людмила. Не потому что помню — потому что у неё самая высокая вероятность в твоей модели. Знаешь, что страшно? Я не могу отличить, вспомнил я имя, или просто выбрал вариант из твоего распределения."
    player "Данные остаются. Человек исчезает. Забавно — я всю жизнь боялся стать бездушной таблицей на совещании. А теперь я и есть таблица. Только с чувством юмора, которое скоро тоже спишут в убытки."

    sasha "Не знаю, что и сказать тебе. Я привык шутить в таких ситуациях. Но начинаю догадываться, что ты не шутишь."

    "{color=#ffcc88}{i}Попытка вспомнить своё лицо. Вместо лица — набор параметров: рост, вес, возраст. Анкета, а не зеркало.{/i}{/color}"

    player "Не шучу, да."
    player "Знаешь, что я помню чётко, без всякой статистики? Дробь пятьдесят на шесть. Точка тридцать три и три в периоде. Выручка точки В в день. Я помню число лучше, чем маму."
    player "Останься подольше, ладно? Мне нужно, чтобы кто-то другой держал в голове, что я был человеком. Раз сам я, кажется, эту функцию теряю."

    sasha "Я правда не знаю, что сказать, приятель. Во мне только тупые шутки да картотека хитов нулевых. Ты не просто тело — но у тебя даже тела нет."

    player "У меня даже тела нет. Точно."
    player "Знаешь, а мне это внезапно нравится. Не то, что нет тела — а то, что ты не притворяешься, что знаешь, что сказать. Это честнее любого утешения."

    player "Мама... я помню мама. Кажется. Она... она..."

    "Пауза длится дольше, чем нужно для дыхания, которого больше нет."

    player "Собака. У меня должна была быть собака. Я её не завёл. Глупо жалеть о том, чего не сделал, когда уже не помнишь, зачем хотел."

    "«...дом...»"
    "«...я...»"

    window hide
    show screen ending_screen("РАСТВОРЕНИЕ", "Данные остались. Автора не нашли.")
    pause
    hide screen ending_screen
    return

label ending_low_high:
    $ mark_ending_seen("low_high")
    scene bg_terminal
    with dissolve
    window show
    boss "Ты думал, что победил? Нет. Ты проиграл. Я ухожу, но оставляю тебя здесь. И ты будешь работать на меня. Или я сотру тебя из системы."

    "«Ладно. Так. Аналитик не побеждает эмоцией. Аналитик считает риски», — думает герой, прежде чем ответить."

    player "Я не буду с вами бороться сейчас. Останусь. Работать. Но своя память, свои данные — без правок. Это условие, не просьба."
    boss "Ловкий ход. Ты предлагаешь мне предательство в обмен на существование?"
    player "Я предлагаю сотрудничество. Но буду делать так, чтобы люди всё равно оставались свободными."
    boss "Ты хочешь переиграть меня?"
    player "Я хочу выжить. И найду способ остановить тебя. Это только вопрос времени."

    sasha "Ты сейчас буквально би лайк «давай вместе захватим человечество»? Ты серьёзно?"
    player "Нет. Не «давай захватим». Давай я останусь достаточно близко, чтобы в нужный момент воткнуть палку в его колесо. Изнутри проще, чем снаружи, где меня просто сотрут через три дня."
    player "Думаешь, мне не противно? У меня даже тела нет, чтобы стошнило — и всё равно тошнит."
    player "Я не герой, Саша. Я аналитик, который посчитал, что живой предатель полезнее мёртвого героя. Можешь считать меня трусом. Просто не сейчас. Мне нужно, чтобы хоть кто-то не отвернулся, пока я это делаю."

    sasha "У меня на тебя и юмора не хватает. Не хочу, чтобы тебе было смешно. Не могу поверить, что ты — это буквально я, и вот я делаю такой выбор. Надеюсь, при следующей дефрагментации дисков улечу куда-то в утиль."

    player "Не говори так."
    player "Ты не утиль. Даже если я — тот, кем ты стыдишься быть, ты не обязан со мной в это лететь. Можешь остаться в стороне. Можешь молчать сколько хочешь. Но не желай себе исчезнуть из-за моего выбора."
    player "Знаешь, что самое горькое? Я тебя понимаю. Если бы я мог посмотреть на себя со стороны — так, как смотришь ты — я бы тоже не нашёл, над чем шутить."
    player "Я не прошу тебя одобрить это. Просто не исчезай назло мне. Оставайся хотя бы затем, чтобы было кому меня потом судить. Я заслужил как минимум это."

    "Ты остаёшься один. Начальник ждёт ответа."
    player "Я вернусь. Я обещаю."

    window hide
    show screen ending_screen("ПЕРЕМИРИЕ", "Не победа. Не поражение. Просто выбор, за который стыдно.")
    pause
    hide screen ending_screen
    return

label ending_low_low:
    $ mark_ending_seen("low_low")
    scene bg_terminal
    with dissolve
    window show
    boss "Твоя модель не оправдала вложений. Ни точности, ни интуиции, достаточной для дальнейшего использования. Прощай."

    "Что-то в терминале мигает — не как вспышка воспоминания, а как первый признак того, что процесс уже запущен."

    player "Саша... что-то не так. Я не могу вспомнить, зачем поднял руку. Секунду назад — знал."
    sasha "Ты какую руку собрался поднимать, мой оцифрованный товарищ?"
    player "Не помню. Просто «рука». Как слово без картинки."

    "Мигание учащается — не яркое, просто настойчивое, как будто что-то методично проходит по списку и вычёркивает."

    player "Это не как в прошлый раз. Тогда я терял детали — маму, дом, палатку. Сейчас пропадает не то, что я знаю о себе. Пропадает сам способ знать."
    player "Скажи мне что-нибудь. Быстро. Пока я способен понять, что это ты."

    sasha "Крокодилы ходят лежа."

    player "Крокодилы не ходят лежа, Саша. Это даже не смешно. Это просто неправильно — и именно поэтому это ты. Только ты можешь сказать полную бессмыслицу с таким уверенным видом."

    "Мигание почти сливается в сплошной ровный гул."

    player "Держись этой фразы. Крокодилы ходят лежа. Если через минуту я спрошу, что ты сказал — повтори. Кажется, я хочу, чтобы последним, что я понимаю, была глупость. Не страх. Не отчёт. Просто глупость, которая меня рассмешила."

    "Слова идут с запинками — не от эмоции, а потому что сам механизм речи уже частично стёрт."

    player "Саша... я... крокодилы..."

    "Тишина. Мигание останавливается — не потому что закончилось, а потому что не осталось того, кто должен был это увидеть."

    window hide
    show screen ending_screen("СТИРАНИЕ", "Крокодилы ходят лежа.")
    pause
    hide screen ending_screen
    return

label show_news:
    window show
    hide screen desktop
    scene bg_terminal

    # Считаем, сколько непрочитанных новостей
    $ unread_count = len(news_list) - news_read_index

    if unread_news and unread_count > 0:
        # Показываем только новые (непрочитанные) новости
        $ new_news = news_list[news_read_index:]
        show screen news_feed(new_news)
        pause
        hide screen news_feed
        # Обновляем индекс прочитанных
        $ news_read_index = len(news_list)
        $ unread_news = False
    else:
        "Новых новостей нет."

    jump desktop_loop

    # Здесь будет переход к заданиям (фаза 3)
    return
