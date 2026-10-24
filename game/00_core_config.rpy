style vscrollbar:
    xsize 4
    top_bar Solid("#0a1518")
    bottom_bar Solid("#3a6a6a")
    thumb_shadow None
    unscrollable "hide"

default accuracy = 100
default intuition = 100

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

default task3_outcome = ""

default sasha_topics_seen = []

default task3_awaiting_access = False

default task2_hypothesis = ""

default game_minutes_total = 0

default poem_done = False

default poem_last_score = 0

default poem_followup_done = False

default poem_form_content_done = False

default task1_store_picked = ""

default task1_route = ""

default task1_tool_used = ""

define accuracy_threshold_p1 = 135
define intuition_threshold_p1 = 110
define accuracy_threshold_p2 = 155
define intuition_threshold_p2 = 116

default cipher_mentioned = False

default crypto_done = False

default crypto_p1_solved = False

default graph_reflection_done = False

default graph_trick_done = False

default hero_trading_backstory_known = False

default hidden_quest_phase1_done = False

default scalp_price = 100.0

default scalp_history = [100.0]

default scalp_position = None

default scalp_entry_price = 0.0

default scalp_bank = 0

define ending_accuracy_threshold = 220
define ending_intuition_threshold = 160

default task2_intro_done = False



define config.window_show_transition = Dissolve(0.2)

define gui.text_font = "fonts/Exo2-Regular.ttf"

define gui.name_text_font = "fonts/Exo2-Bold.ttf"

define gui.interface_text_font = "fonts/Exo2-Regular.ttf"


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
        xalign 0.5
        yalign 1.0
        yoffset -60
        spacing 6

        for i in items:
            $ _is_story = i.caption.startswith("★")
            $ _caption = i.caption[1:].strip() if _is_story else i.caption
            if _is_story:
                textbutton _caption action i.action:
                    xalign 0.5
                    padding (22, 8)
                    background Solid("#05161acc")
                    text_color "#ffbb33"
                    text_hover_color "#fff5cc"
                    hover_background "#3a2a00cc"
            else:
                textbutton _caption action i.action:
                    xalign 0.5
                    padding (22, 8)
                    background Solid("#05161acc")
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
image bg_task1_briefing = "images/bg_task1_briefing_cyan.png"
image bg_poem_street = "images/poem/bg_poem_street.png"
image bg_poem_poplars1 = "images/poem/bg_poem_poplars1.png"
image bg_poem_field = "images/poem/bg_poem_field.png"
image bg_poem_runes = "images/poem/bg_poem_runes.png"
image bg_poem_poplars2 = "images/poem/bg_poem_poplars2.png"
image bg_poem_tree = "images/poem/bg_poem_tree.png"

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


default orion_stars_clicked = []


define orion_star_order = ["betelgeuse", "bellatrix", "belt1", "belt2", "belt3", "saiph", "rigel"]


default samurai_letters_state = {}


define samurai_word = ["С", "А", "М", "У", "Р", "А", "Й"]

define samurai_target_rot = [-9.5, -9.0, -1.7, 7.2, -8.3, -6.1, 2.8]

define samurai_x_pos = [465, 613, 814, 940, 1113, 1286, 1490]

define samurai_y_pos = [447, 562, 487, 442, 455, 544, 540]

define samurai_start_offsets = [90, 45, 135, 45, 90, 135, 45]

define samurai_rotation_step = 45

default memory_query_cleared = []

default memory_query_mistakes = 0

default memory_query_total_mistakes = 0

default task3_break_chat_seen = False


define memory_query_target_idx = [2, 5, 8, 11, 13, 16, 18, 21]

define memory_query_cols = 8



default nq_selected_sentence = None

default nq_pairs = {}


default pd_selected = set()

default nf_links = []
default nf_avail = []


init python:
    def unlock_memory(key):
        if key not in memory_unlocked:
            memory_unlocked.append(key)

    memory_articles = {
        "oformlenie_schorsa": {
            "title": "Три часа утра на Щорса",
            "trigger": "Ох... до сих пор содрогаюсь от стыда.",
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
            "trigger": "Да уж, новая цель жизни: не стать Геной.",
            "text": "У нас был Гена — не помню, чтобы кто-то называл его иначе, хотя не уверен, что это было его настоящее имя. Гена не доверял формулам. «Чёрный ящик, — говорил он, — компьютер за меня решил, что аномалия, а я должен просто поверить». Поэтому однажды он решил искать аномалию честно — глазами.\n\nРаспечатал всю таблицу. Не выборку — всю. Заклеил скотчем стену переговорной от пола до потолка, лист к листу, как будто мы расследуем не падение выручки, а серию нераскрытых убийств.\n\nТри дня Гена ходил вдоль этой стены с маркером и кофе, который темнел день ото дня быстрее, чем его настроение. На планёрке он торжественно объявил: аномалия — где-то в районе четвёртого квартала, «я чувствую её кожей».\n\nМы сверили. Он ошибся на два месяца и один магазин. Я в это время вбил одну формулу стандартного отклонения — тридцать секунд, никакого скотча, никакой кожи.\n\nСтену, кстати, так и не отклеили — то ли из уважения к труду, то ли из лени. Изредка прохожу мимо переговорной и вижу этот бумажный саркофаг боковым зрением.\n\nС тех пор, когда кто-то говорит «я чувствую аномалию кожей», я молча кладу перед ним лист с формулой отклонения. И рулон скотча — на всякий случай, чтобы не расставаться с привычками сразу."
        },
        "shifr_pod_partoy": {
            "title": "Шифр под партой",
            "trigger": "Какой же шифр разгадать сложнее — шифр реальности или моей памяти?",
            "text": "Дети постоянно что-то придумывают. В том числе пути прятать свои секреты от взрослых.\n\nМой первый искусственный язык я придумал ещё до школы: мне показалось совершенно гениальной идеей к каждому слову просто добавлять слог «-ца». Писать я только-только научился, поэтому в глаголах это «ца» то и дело у меня задваивалось: «мамаца вечерца убираецаца» и «кошкаца играецаца сца клубокца». Так что, когда отец нашёл мой дневник с «секретами», долго смеялся с трёх вещей сразу: с уровня тайности секретной информации, с моей безграмотности и с того, до чего же нелепо лёгкий шифр у меня получился.\n\nЯ это запомнил. Поэтому в средней школе принялся делать записки Ромычу и шпаргалки уже с более продвинутым шифром — использовал «штакетник». Марь Иванна однажды перехватила такую записку, а я сидел с совершенно спокойным лицом: расшифровать-то она не сможет! Но оказалось, что Марь Иванне было достаточно самого факта передачи записки, чтобы считать её шпорой. Так что два я всё равно отхватил. Зато по информатике у меня были одни пятёрки. К 11 классу я знал уже десятки разных шифров и криптографических приёмов — способов скрыть тайное или сжать его для удобного хранения.\n\nУж не знаю, что именно привело меня в аналитику. Я вроде как целенаправленно на неё и не учился, в дипломе у меня написано что-то невразумительное, однако по этому невразумительному я в жизни не проработал ни дня.\n\nНаверное, мне и не нужно было «приходить» в аналитику. Она всегда была со мной, в каждой моей попытке осмыслить реальность, описать её формулой, выявить паттерн и предсказать поведение систем. Может быть, аналитиками и вовсе не становятся?.. Этого я не знаю.\n\nНо я знаю вот что: мир кажется случайным ровно до тех пор, пока ты не найдёшь правильный угол, под которым он перестаёт таким быть."
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
            "title": "Уоррен Баффет",
            "desc": "Доказал крутость стоимостного инвестирования."
        },
        "zvezdochet": {
            "title": "Звездочёт",
            "desc": "Сложил ночные измерения в одну картину."
        },
        "priznalsya_a_ne_pritvorilsya": {
            "title": "Гадалка",
            "desc": "Играешь на бирже как твоя бабуля."
        },
        "lyuboznatelny": {
            "title": "Обо всём понемногу",
            "desc": "Поговорил с Сашей на все темы, какие только были доступны."
        },
        "vzlomshik_po_mode": {
            "title": "Взломщик по моде",
            "desc": "Переизобрёл частотный анализ."
        },
        "yamb_v_kazhdoy_yacheyke": {
            "title": "Ямб в каждой ячейке",
            "desc": "Довёл ИИ-аналитика до того, что он увидел цезуру в таблице выручки."
        },
        "sam_s_usami": {
            "title": "Сам с усами",
            "desc": "Прошёл Задание 2, не обратившись к Саше ни разу."
        },
        "stoprocentny_skeptik": {
            "title": "Стопроцентный (или 142-процентный) скептик",
            "desc": "Прошёл всю серию графиков-обманов и разучился доверять диаграммам на глаз."
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
    import math
    import random

    NF_TEXT = {
        "studied":  "Босс исследовал не точку D, а меня.",
        "bored":    "Узнал мою методологию — и закрыл дело",
        "slips":    "Оговорки: земные коллеги, ретрансляторы, похищения",
        "news":     "В новостях упоминались пришельцы... кажется",
        "today":    "Сегодня среда",
        "peaks":    "Пики выручки D — по средам",
        "load":     "Выручка идёт вместе с нагрузкой на сервер",
        "nosupply": "Продажи есть, заявок на поставку нет",
        "closed":   "По средам D закрыт для покупателей",
        "nord":     "Норд-Капитал контролирует D",
        "sky":      "Объект в небе ярче раз в семь суток",
        "awoke":    "Очнулся здесь без памяти и... без тела?",
        "astro":    "Я астроном-любитель, ехал смотреть объект за городом",
        "ahead":    "Журнал кто-то открыл и этот кто-то будто читал мои мысли",
        "flash":    "Вспышка пришла ночью, как я предсказал",
    }

    NF_SHORT = {
        "studied": "босс изучал меня", "bored": "закрыл дело", "slips": "оговорки",
        "news": "новости", "today": "сегодня среда", "peaks": "пики по средам",
        "load": "нагрузка", "nosupply": "нет поставок", "closed": "закрыт по средам",
        "nord": "Норд-Капитал", "sky": "объект в небе", "awoke": "очнулся здесь",
        "astro": "астроном", "ahead": "журнал знал заранее", "flash": "вспышка ночью",
    }

    NF_POS = {
        "studied": (520, 380), "bored": (300, 260), "ahead": (760, 250),
        "slips": (480, 600), "news": (250, 700), "awoke": (780, 650),
        "astro": (1020, 790), "sky": (1380, 680), "flash": (1620, 540),
        "peaks": (1120, 420), "today": (960, 260), "load": (1420, 270),
        "closed": (1360, 430), "nosupply": (1010, 570), "nord": (1190, 610),
    }

    # мысли героя при верной связи (черновик, перепиши под свой голос)
    NF_EDGES = {
        frozenset(["today", "peaks"]):    "Сегодня именно тот день: выручка D пиковая по средам.",
        frozenset(["peaks", "load"]):     "Две кривые идут вместе. По средам что-то грузит сервер.",
        frozenset(["peaks", "nosupply"]): "Выручка есть, поставок нет. Это не торговля.",
        frozenset(["studied", "bored"]):  "Он получил, что хотел: мой метод. Дело ему было не нужно.",
        frozenset(["studied", "slips"]):  "Он не человек. Он изучает человека. Я его подопытный.",
        frozenset(["news", "slips"]):     "Не одна оговорка: небо и космос повсюду.",
        frozenset(["closed", "peaks"]):   "Закрыто для людей, а выручка максимальная. Кто кому платит?",
        frozenset(["sky", "peaks"]):      "Объект и D живут в одном ритме: семь суток, среда.",
        frozenset(["astro", "sky"]):      "Я ехал смотреть именно этот объект.",
        frozenset(["awoke", "astro"]):    "Я ехал смотреть объект и очнулся здесь. Это связано.",
        frozenset(["nord", "nosupply"]):  "Владелец, которому поставки не нужны. Владелец занят не торговлей.",
        frozenset(["ahead", "studied"]):  "Система слушала меня раньше, чем я говорил.",
        frozenset(["flash", "sky"]):      "Расписание...",
        frozenset(["awoke", "slips"]):    "Он говорил о похищениях. А я очнулся здесь без тела.",
        frozenset(["studied", "peaks"]):  "Аномалия была приманкой. Изучали меня.",
    }

    def nf_available():
        a = ["studied", "bored", "slips", "today", "peaks", "load", "nosupply", "awoke"]
        if news_read_index > 0: a.append("news")
        if hidden_quest_phase2_done: a += ["astro", "sky"]
        if "wishes" in hq2_viewed: a.append("closed")
        if hidden_quest_phase1_done: a.append("nord")
        if task2_secret_access: a.append("ahead")
        if hq2_confirmed: a.append("flash")
        return a

    def nf_has(a, b):
        return frozenset([a, b]) in nf_links

    def nf_line(x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        return max(2, int(math.hypot(dx, dy))), math.degrees(math.atan2(dy, dx))

    def nf_center(avail):
        xs = [NF_POS[k][0] for k in avail]
        ys = [NF_POS[k][1] for k in avail]
        return sum(xs) / float(len(xs)), sum(ys) / float(len(ys))

    def nf_xy(k, avail, p):
        cx, cy = nf_center(avail)
        x, y = NF_POS[k]
        x += 960 - cx
        y += 500 - cy
        e = p * p * (3 - 2 * p)
        f = 1.0 - 0.45 * e
        return int(960 + (x - 960) * f), int(500 + (y - 500) * f)

    def nf_make_bg():
        r = random.Random(11)
        out = []
        for i in range(110):
            out.append((r.randint(10, 1910), r.randint(10, 1070), r.choice([1, 1, 2, 2, 3]),
                        r.uniform(0.12, 0.3), r.uniform(0.45, 0.9), r.uniform(1.5, 4.0), r.uniform(0.0, 3.0)))
        return out

    NF_BG = nf_make_bg()

default _chat_icon_line = 0


default call_boss_count = 0

init python:
    CR_FONT = "fonts/JetBrainsMono-Regular.ttf"
    CR_SPEED = 70.0
    CR_COL = {"player": "#00ffcc", "sasha": "#d650be"}
    CR_WHO = {"player": "ТЫ", "sasha": "САША"}
    CR_H = {"title": 70, "name": 54, "sub": 40, "msg": 54, "gap": 44, "big": 64, "pause": 380}

    CR_ITEMS = [
        ("title", "Этот проект стал возможен благодарям им. Спасибо:"), ("gap", ""),
        ("name", "Анне"), ("sub", "за яркий логотип и дизайн"), ("gap", ""),
        ("name", "Ольге"), ("sub", "за дизайн и промпт-инжиниринг"), ("gap", ""),
        ("name", "Лере"), ("sub", "за координационную поддержку и связи"), ("gap", ""),
        ("name", "Але"), ("sub", "за эстетическое консультирование"), ("gap", ""),
        ("name", "Нейросетям"), ("sub", "за помощь и поиск проблем"), ("pause", 1),
        ("name", "Мне"), ("sub", "мои ручки старались и написали для вас пару тысяч строк"), ("pause", 2),
        ("title", "Отдельные благодарности:"), ("gap", ""),
        ("name", "Маме"), ("sub", "мам, люблю тебя. Однажды я найду нормальную работу. Честно."), ("gap", ""),
        ("name", "Бро"), ("sub", "сам знаешь, за что, ты же мой бро"), ("pause", 3),
        ("sub", "Игра выполнена на бесплатном движке Ren'Py"), ("pause", 4),
        ("msg", "Любите аналитику, любите данные, любите человечество"), ("gap", ""),
        ("msg", "Будьте на стороне людей"), ("gap", ""),
        ("msg", "Берегите себя"), ("pause", 5),
        ("big", "Спасибо"), ("pause", 6),
    ]

    def cr_layout():
        y = 0
        marks = {}
        rows = []
        for kind, payload in CR_ITEMS:
            if kind == "pause":
                marks[payload] = y
            rows.append((kind, payload, y))
            y += CR_H[kind]
        return rows, marks, y

    CR_ROWS, CR_MARKS, CR_END = cr_layout()

    def run_credits(lines):
        cur = 0
        renpy.show_screen("cr_roll", 1080, 1080, 0.01)
        renpy.pause(0.6, hard=True)
        for k in sorted(CR_MARKS):
            target = 380 + CR_MARKS[k]
            t = (target - cur) / CR_SPEED
            renpy.show_screen("cr_roll", int(1080 - cur), int(1080 - target), t)
            renpy.pause(t, hard=True)
            cur = target
            for who, what in lines.get(k, []):
                renpy.show_screen("cr_say", who, what)
                renpy.pause(max(2.4, 0.05 * len(what) + 1.4))
                renpy.hide_screen("cr_say")
                renpy.pause(0.4, hard=True)
        renpy.pause(1.0, hard=True)
        renpy.show_screen("cr_out")
        renpy.pause(1.6, hard=True)
        renpy.hide_screen("cr_roll")
        renpy.hide_screen("cr_out")

define eplayer = Character("ТЫ", screen="end_say", who_color="#00ffcc", what_color="#00ffcc")
define esasha = Character("САША", screen="end_say", who_color="#d650be", what_color="#d650be")
define eboss = Character("НАЧАЛЬНИК", screen="end_say", who_color="#ff6b6b", what_color="#ff6b6b")
define enar = Character(None, screen="end_say", what_color="#8a949a", what_italic=True)

transform card_fade:
    alpha 0.0
    easein 2.0 alpha 1.0

screen end_say(who, what):
    zorder 100
    vbox:
        xalign 0.5
        ypos 780
        spacing 10
        xmaximum 1300
        if who is not None:
            text who id "who" font CR_FONT size 22 xalign 0.5
        text what id "what" font CR_FONT size 30 xalign 0.5 text_align 0.5

screen ending_card(title, sub):
    zorder 110
    add Solid("#000000")
    vbox:
        at card_fade
        xalign 0.5
        yalign 0.5
        spacing 26
        text title font CR_FONT size 64 color "#ffffff" kerning 10 xalign 0.5
        add Solid("#00ffcc") xysize (420, 2) xalign 0.5
        text sub font CR_FONT size 24 color "#8a949a" xalign 0.5 text_align 0.5 xmaximum 1200
