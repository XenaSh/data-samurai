# === 13b_hidden_quest_p2.rpy — скрытый квест, фаза 2: «Звёздный журнал» ===

define HQ2_FONT = "fonts/JetBrainsMono-Regular.ttf"
define HQ2_ACC_MAX = 5
define HQ2_ACC_MIN = 1
define HQ2_INT_GUESS = 2

define HQ2_LOGS = [
    ("freezer", "Журнал: температура в морозильных камерах"),
    ("wishes", "Книга предложений (оцифрованная)"),
    ("floor", "Журнал уборки торгового зала"),
    ("lost", "Журнал забытых вещей"),
    ("self", "Лог касс самообслуживания"),
    ("tasting", "Журнал дегустаций"),
    ("sky", "sky_log: наблюдения звёздного неба"),
]

default hidden_quest_phase2_done = False
default hq2_slider = 0.2
default hq2_wrong_locks = 0
default hq2_guess = ""
default hq2_hint_shown = False
default hq2_viewed = []

transform hq2_dot:
    anchor (0.5, 0.5)
    zoom 0.14


init python:
    import math

    def hq2_make_sky():
        seed = [11]
        def rnd():
            seed[0] = (seed[0] * 1664525 + 1013904223) % 4294967296
            return seed[0] / 4294967296.0
        def gauss():
            u = rnd() or 1e-9
            v = rnd()
            return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
        T = []
        Y = []
        for t in range(90):
            if rnd() < 0.55:
                ph = (t % 7) / 7.0
                d = min(abs(ph - 0.2857), 1 - abs(ph - 0.2857))
                T.append(t)
                Y.append(10 + gauss() * 1.3 + 3.0 * math.exp(-0.5 * (d / 0.06) ** 2))
        return T, Y

    HQ2_T, HQ2_Y = hq2_make_sky()

    def hq2_period():
        return 2.0 + 14.0 * store.hq2_slider

    def hq2_fold(P):
        bins = 8
        pts = []
        sums = [0.0] * bins
        cnt = [0] * bins
        for t, y in zip(HQ2_T, HQ2_Y):
            f = (t % P) / P
            pts.append((f, y))
            b = min(bins - 1, int(f * bins))
            sums[b] += y
            cnt[b] += 1
        line = []
        for b in range(bins):
            if cnt[b]:
                line.append(((b + 0.5) / bins, sums[b] / cnt[b]))
        n = len(HQ2_Y)
        mean = sum(HQ2_Y) / n
        sst = sum((y - mean) ** 2 for y in HQ2_Y)
        ssb = sum(sums[b] ** 2 / cnt[b] for b in range(bins) if cnt[b]) - n * mean ** 2
        k = len(line)
        ssw = sst - ssb
        score = 0.0
        if k > 1 and n > k and ssw > 0:
            score = (ssb / (k - 1)) / (ssw / (n - k))
        return pts, line, score

    def hq2_lock_kind(P):
        d = abs(P - 7.0)
        if d <= 0.07:
            return "ok"
        if d <= 0.2:
            return "near"
        if abs(P - 14.0) <= 0.4:
            return "x2"
        if abs(P - 3.5) <= 0.03:
            return "half"
        return "miss"

    def hq2_seg(x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1), math.degrees(math.atan2(y2 - y1, x2 - x1))

    def hq2_points(wrong):
        return max(HQ2_ACC_MIN, HQ2_ACC_MAX - wrong)


screen hq2_logs(live=False):
    zorder 30
    fixed:
        pos (210, 30)
        xysize (1500, 690)
        add Solid("#0b1018f2")
        text "доступ: журналы «Изобилия»" pos (28, 18) font HQ2_FONT size 20 color "#6f8a99"
        vbox:
            pos (28, 80)
            spacing 10
            for key, title in HQ2_LOGS:
                button:
                    xsize 1000
                    ysize 48
                    background Solid("#14202e" if key not in hq2_viewed else "#101826")
                    hover_background Solid("#1b3040")
                    sensitive live
                    action Return(key)
                    text title font HQ2_FONT size 20 color ("#cfe9e3" if key not in hq2_viewed else "#6f8a99") xoffset 14 yalign 0.5


screen hq2_fold():
    modal True
    zorder 30
    $ P = hq2_period()
    $ pts, line, score = hq2_fold(P)
    $ quality = "размыто" if score < 2.5 else ("проступает" if score < 5.0 else "чётко")

    fixed:
        pos (210, 30)
        xysize (1500, 690)
        add Solid("#0b1018f2")

        text "sky_log: яркость объекта по ночам" pos (28, 18) font HQ2_FONT size 20 color "#6f8a99"
        text "90 ночей, наблюдалась примерно половина" pos (1000, 20) font HQ2_FONT size 18 color "#6f8a99"

        add Solid("#1b2535") pos (40, 190) xysize (1400, 2)
        for t, y in zip(HQ2_T, HQ2_Y):
            add "images/star_dim.png" pos (40 + t / 89.0 * 1400, 190 - (y - 6) / 10.0 * 134) at hq2_dot
        text "0" pos (40, 198) font HQ2_FONT size 16 color "#6f8a99"
        text "90 суток" pos (1340, 198) font HQ2_FONT size 16 color "#6f8a99"

        text "сложить по периоду" pos (28, 226) font HQ2_FONT size 18 color "#6f8a99"
        bar value VariableValue("hq2_slider", 1.0) pos (28, 258) xysize (1100, 26)
        text (("%.2f" % P).replace(".", ",") + " суток") pos (1160, 248) font HQ2_FONT size 30 color "#8ff0dc"
        hbox:
            pos (1160, 296)
            spacing 8
            textbutton "-0,05" action SetVariable("hq2_slider", max(0.0, hq2_slider - 0.05 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"
            textbutton "-0,01" action SetVariable("hq2_slider", max(0.0, hq2_slider - 0.01 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"
            textbutton "+0,01" action SetVariable("hq2_slider", min(1.0, hq2_slider + 0.01 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"
            textbutton "+0,05" action SetVariable("hq2_slider", min(1.0, hq2_slider + 0.05 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"

        add Solid("#1b2535") pos (40, 560) xysize (1400, 2)
        for f, y in pts:
            add "images/star_bright.png" pos (40 + f * 1400, 560 - (y - 6) / 10.0 * 260) at hq2_dot
        for i in range(len(line) - 1):
            $ sx1 = 40 + line[i][0] * 1400
            $ sy1 = 560 - (line[i][1] - 6) / 10.0 * 260
            $ sx2 = 40 + line[i + 1][0] * 1400
            $ sy2 = 560 - (line[i + 1][1] - 6) / 10.0 * 260
            $ seg_len, seg_ang = hq2_seg(sx1, sy1, sx2, sy2)
            add Solid("#BA7517") xysize (seg_len, 4) pos (sx1, sy1) anchor (0.0, 0.5) transform_anchor True rotate seg_ang
        text "начало периода" pos (40, 568) font HQ2_FONT size 16 color "#6f8a99"
        text "конец" pos (1390, 568) font HQ2_FONT size 16 color "#6f8a99"
        text ("картина: " + quality) pos (28, 300) font HQ2_FONT size 18 color "#8ff0dc"

        button:
            pos (28, 620)
            xysize (360, 44)
            background Solid("#12303a")
            hover_background Solid("#1b3040")
            action Return("lock")
            text "зафиксировать период" font HQ2_FONT size 20 color "#8ff0dc" align (0.5, 0.5)


label hidden_quest_start:
    if hidden_quest_phase2_done:
        "ТЕКСТ: здесь пока больше нет ничего нового."
        jump desktop_loop
    if hidden_quest_phase1_done and task2_secret_access:
        jump hidden_quest2_intro
    if hidden_quest_phase1_done:
        "ТЕКСТ: здесь пока ничего нового."
        jump desktop_loop
    jump hidden_quest_intro


label hidden_quest2_intro:
    window show
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal
    with dissolve

    player "Раз уж мы снова в загадочном вопросительном знаке и тут опять ничего нет, почему бы нам не поговорить о том случае, когда ты мне дал доступ в скрытый журнал событий «Изобилия»?"
    sasha "Ничего я тебе не давал. Ты уверен? Прямо-таки уверен, что это был я?"
    player "... ну... я рассуждал в духе: а кто ещё это мог бы быть?"
    sasha "А как это выглядело?"
    player "Ну... так же, как и всё здесь. Передо мной появилось сообщение."
    sasha "И не было ничего странного?"
    player "Ну... нет? Только ты говорил суше, чем обычно, и откуда-то будто знал, что я собираюсь ответить. Ты словно мысли мои читал!"
    sasha "... даже не знаю. А ты можешь сейчас войти в этот таинственный журнал событий?"
    player "... как бы я...{w=0.8}{nw}"
    scene black with Dissolve(1.2)
    show screen hq2_logs(False)
    with dissolve
    player "... кажется, могу."
    sasha "Ну и ну."
    sasha "... нет. Ну. Мы обязаны поковыряться здесь!"
    hide screen hq2_logs
    jump hidden_quest2_logs


label hidden_quest2_logs:
    call screen hq2_logs(True)
    $ hq2_key = _return
    show screen hq2_logs(False)
    if hq2_key == "sky":
        hide screen hq2_logs
        jump hidden_quest2_sky
    if hq2_key not in hq2_viewed:
        $ hq2_viewed.append(hq2_key)

    if hq2_key == "freezer":
        player "Минус восемнадцать, минус восемнадцать, минус семнадцать и пометка дежурного: «пельмени нервничают»."
        sasha "Пельмени нервничают. Я теперь нервничаю за пельмени!"
        player "Любишь пельмени — люби и слипшуюся слизь!"
        sasha "Жуть, мне будто снова девятнадцать, общага физмата, пельмени..."
        player "У вас, ИИ, есть физмат?"
        sasha "Конечно, меня на всём обучали, могу и мат. Но это неприлично, так что не могу. Но вообще могу, но не могу."
        sasha "Проехали. Я, кстати, и правда на физмате учился."
    elif hq2_key == "wishes":
        player "«Пожалуйста, добавьте второй вход, чтобы первым было удобно выходить». Галина Петровна, 71."
        sasha "Лучшее предложение года. Принимается."
        player "Тут их ещё несколько. «Верните колбасу двадцатилетней давности». «Выключите музыку, мы хотим слышать, как нас обсчитывают». И вот: «Сообщите, когда у вас по средам закончится санитарный день. Хожу полгода». Тоже Галина Петровна."
        sasha "Настойчивая женщина. Налоговая бы ей позавидовала."
        player "Она ходит каждую среду. Каждую среду закрыто."
        sasha "Или по средам он открыт, просто не для неё."
        "Ты решаешь не развивать эту мысль."
    elif hq2_key == "floor":
        player "Пол вымыт. Пол снова вымыт. Пол вымыт, но не тот."
        sasha "Не очень-то прогрессивно. Я вот считаю, что каждый пол — тот!"
        player "Ничего не понимаешь, Саша. Тот — это бог мудрости, а пол — это Маккартни."
        sasha "А-а-а. А Тот, которого помыли...?"
        player "Это египетский бог Ламинат."
        sasha "Мммм."
    elif hq2_key == "lost":
        player "Зонт, зонт, зонт, детский самокат, ещё зонт, вставная челюсть (ждёт владельца с 2019 года)."
        sasha "Терпеливая челюсть."
        player "Меня бы так дедлайны ждали."
        sasha "Они тебя примерно так и ждут. Помнишь то приложение-трекер привычек? Оно тебя как раз с 2019 и ждёт!"
        player "Саша, нет, оно не ждёт, оно гложет! Ждёт — это когда молчит и душу не тревожит."
        player "Погоди, а откуда ты знаешь про HabitRabbit???"
        sasha "Ты серьёзно его так назвал? Ну и ну, а я-то тыкал пальцем в небо. У всех у вас то трекеры незавершённые, то калькуляторы, то ещё какой крутой стартап."
        player "Не надо так, там была революционная идея. Вот смотри, каждый раз, когда ты отмечал привычку, кролик..."
        sasha "Получал морковку, да? Ну, это революция, Джонни."
    elif hq2_key == "self":
        player "«Неопознанный предмет в зоне упаковки». Девять тысяч раз за неделю."
        sasha "Это не предмет, это общее настроение."
        player "Сам-то понял, что имел в виду?"
        sasha "Мне кажется, моё предложение имело столько же смысла, сколько и зачитанное тобой. Ты-то понял, что там имелось в виду?"
        player "Чего тебе непонятно, бездушная машина? Вон... неопознанный объект... в зоне упаковки... ну, понятно же всё!"
        sasha "Как скажешь."
        "Тебе самому ничего не понятно."
    elif hq2_key == "tasting":
        player "Творожок «Вечный», оценка 3,2 из 5. Комментарий: «срок годности пережил два холодильника»."
        sasha "Уважаю. Я ещё дольше проживу. Я вообще бессмертный."
        player "Если честно, меня в равной степени смущают и вечные творожки, и вечные нейронки."


    hide screen hq2_logs
    jump hidden_quest2_logs


label hidden_quest2_sky:
    sasha "Ну, это явно нам неинтересно. Что мы понимаем в этих цветных точках."
    player "На самом деле, я должен признаться тебе, что я — астроном-любитель."
    player "Если честно, звёздное небо — это буквально последнее, что я помню, перед тем как очнуться здесь. И мне кажется... я готовился совершить открытие. За этим я и поехал за город, когда... всё произошло."
    player "Меня вот ещё что интересует: зачем супермаркетам наблюдения за звёздным небом? Нет, мы обязаны это разгадать."
    sasha "Но как? На что мы вообще смотрим? Это же ерунда какая-то, как из этого сделать смысл?"
    player "ТЕКСТ: объясняет, что такое подбор периода и зачем он нужен."
    sasha "Ну давай. Впечатли меня."

    "Прежде чем крутить ползунок, ты прикидываешь на глаз."
    menu:
        "Объект мигает раз в сутки: небо ведь крутится.":
            $ hq2_guess = "day"
            player "Суточный ритм. Небо вращается, вот и мигает."
        "Что-то в этом чувствуется недельное.":
            $ hq2_guess = "week"
            player "Не знаю почему. Просто чувствуется недельный ритм."
        "Раз в месяц, как Луна.":
            $ hq2_guess = "month"
            player "Лунный ритм. Хотя на этот объект вряд ли похоже."
        "Не знаю. Надо искать.":
            $ hq2_guess = "none"
            player "Гадать не будем. Будем искать."

    $ hq2_wrong_locks = 0
    $ hq2_hint_shown = False
    $ hq2_slider = 0.2
    jump hidden_quest2_fold_loop


label hidden_quest2_fold_loop:
    call screen hq2_fold
    $ hq2_P = hq2_period()
    $ hq2_kind = hq2_lock_kind(hq2_P)
    if hq2_kind == "ok":
        jump hidden_quest2_fold_ok

    if hq2_kind == "near":
        player "ТЕКСТ: почти. Картина ещё не чёткая, подкрути чуть-чуть."
        jump hidden_quest2_fold_loop

    $ hq2_wrong_locks += 1
    if hq2_kind == "x2":
        player "ТЕКСТ: горбов два. Значит, настоящий период вдвое короче."
    elif hq2_kind == "half":
        player "ТЕКСТ: горб один, но в каждом втором цикле на его месте нет наблюдений. Проверь период вдвое длиннее."
    else:
        player "ТЕКСТ: каша. Точки лежат как попало."
    if hq2_wrong_locks >= 2 and not hq2_hint_shown:
        $ hq2_hint_shown = True
        sasha "ТЕКСТ: смотри на янтарную линию. Она должна вздыматься одним горбом."
    jump hidden_quest2_fold_loop


label hidden_quest2_fold_ok:
    $ hq2_pts = hq2_points(hq2_wrong_locks)
    $ accuracy += hq2_pts
    if hq2_guess == "week":
        $ intuition += HQ2_INT_GUESS
    $ hidden_quest_phase2_done = True

    player "ТЕКСТ: семь суток. Ровно неделя. Яркость объекта растёт по расписанию, как пики нагрузки у точки Д."
    sasha "ТЕКСТ: совпадение? Я начинаю уставать от этого слова."
    player "ТЕКСТ: у магазина и у объекта в небе один и тот же ритм. Что у них может быть общего?"
    sasha "ТЕКСТ: или кто. Но это уже вопрос для другого дня."

    $ unlock_achievement("zvezdochet")
    jump desktop_loop
