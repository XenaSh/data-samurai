# === 13b_hidden_quest_p2.rpy — скрытый квест, фаза 2: «Звёздный журнал» ===

define HQ2_FONT = "fonts/JetBrainsMono-Regular.ttf"
define HQ2_ACC_MAX = 5
define HQ2_ACC_MIN = 1

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
default hq2_hint_shown = False
default hq2_viewed = []

init python:
    import math

    HQ2_N = 120
    HQ2_NOISE_MID = 3.9
    HQ2_NOISE_HIGH = 8.0

    def hq2_make_sky():
        seed = [28]
        def rnd():
            seed[0] = (seed[0] * 1664525 + 1013904223) % 4294967296
            return seed[0] / 4294967296.0
        def gauss():
            u = rnd() or 1e-9
            v = rnd()
            return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
        T = []
        Y = []
        for t in range(HQ2_N):
            if rnd() < 0.55 and t != 119:
                ph = (t % 7) / 7.0
                d = min(abs(ph - 1 / 7.0), 1 - abs(ph - 1 / 7.0))
                T.append(t)
                Y.append(10 + gauss() * 1.3 + 5.0 * math.exp(-0.5 * (d / 0.13) ** 2))
        return T, Y

    HQ2_T, HQ2_Y = hq2_make_sky()

    def hq2_period():
        return 2.0 + 14.0 * store.hq2_slider

    def hq2_rx(t):
        return int(40 + t / float(HQ2_N - 1) * 1400)

    def hq2_ry(y):
        return int(190 - (y - 6) / 13.0 * 110)

    def hq2_fy(y):
        return int(560 - (y - 6) / 13.0 * 190)

    def hq2_cuts(P):
        out = []
        k = 0
        while k * P <= HQ2_N - 1:
            out.append(hq2_rx(k * P))
            k += 1
        return out

    def hq2_fold(P, T=None, Y=None):
        if T is None:
            T = HQ2_T
            Y = HQ2_Y
        bins = 8
        pts = []
        sums = [0.0] * bins
        cnt = [0] * bins
        for t, y in zip(T, Y):
            f = (t % P) / P
            pts.append((f, y))
            b = min(bins - 1, int(f * bins))
            sums[b] += y
            cnt[b] += 1
        line = []
        for b in range(bins):
            if cnt[b]:
                line.append(((b + 0.5) / bins, sums[b] / cnt[b]))
        n = len(Y)
        mean = sum(Y) / n
        sst = sum((y - mean) ** 2 for y in Y)
        ssb = sum(sums[b] ** 2 / cnt[b] for b in range(bins) if cnt[b]) - n * mean ** 2
        k = len(line)
        ssw = sst - ssb
        score = 0.0
        if k > 1 and n > k and ssw > 0:
            score = (ssb / (k - 1)) / (ssw / (n - k))
        return pts, line, score

    def hq2_quality(score):
        if score < HQ2_NOISE_MID:
            return "размыто"
        if score < HQ2_NOISE_HIGH:
            return "проступает"
        return "чётко"

    def hq2_meter(score):
        fill = int(min(score / 20.0, 1.0) * 300)
        mark = int(HQ2_NOISE_HIGH / 20.0 * 300)
        return fill, mark

    def hq2_steps(line, x0=40, width=1400):
        rects = []
        bw = width / 8.0
        prev = None
        for fc, m in line:
            b = int(fc * 8)
            x = x0 + b * bw
            y = hq2_fy(m)
            rects.append((int(x), y - 2, int(bw), 4))
            if prev is not None and prev[0] == b - 1:
                top = min(prev[1], y)
                rects.append((int(x) - 2, top - 2, 4, abs(prev[1] - y) + 4))
            prev = (b, y)
        return rects

    def hq2_lock_kind(P):
        d = abs(P - 7.0)
        if d <= 0.10:
            return "ok"
        if d <= 0.35:
            return "near"
        if abs(P - 14.0) <= 0.5:
            return "x2"
        if abs(P - 3.5) <= 0.05:
            return "half"
        if abs(P - 7 / 3.0) <= 0.03:
            return "third"
        return "miss"

    def hq2_run_sweep():
        steps = []
        for k in range(19):
            steps.append((3.0 + 0.2 * k, 0.04))
        for k in range(31):
            steps.append((6.7 + 0.02 * k, 0.06))
        for k in range(19):
            steps.append((7.5 + 0.2 * k, 0.04))
        for P, d in steps:
            store.hq2_slider = (P - 2.0) / 14.0
            renpy.pause(d, hard=True)

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


screen hq2_fold(live=True):
    zorder 30
    $ P = hq2_period()
    $ pts, line, score = hq2_fold(P)
    $ quality = hq2_quality(score)
    $ steps = hq2_steps(line)
    $ cuts = hq2_cuts(P)
    $ m_fill, m_mark = hq2_meter(score)

    fixed:
        pos (210, 30)
        xysize (1500, 690)
        add Solid("#0b1018f2")

        text "sky_log: яркость объекта по ночам" pos (28, 18) font HQ2_FONT size 20 color "#6f8a99"
        text "120 ночей, наблюдалась примерно половина" pos (1000, 20) font HQ2_FONT size 18 color "#6f8a99"
        text "ряд как есть: по горизонтали номер ночи, по вертикали яркость. Янтарные линии режут ряд на куски длиной в период" pos (28, 52) font HQ2_FONT size 16 color "#6f8a99"

        for cx in cuts:
            add Solid("#BA751766") pos (cx, 80) xysize (2, 110)
        add Solid("#1b2535") pos (40, 190) xysize (1400, 2)
        for t, y in zip(HQ2_T, HQ2_Y):
            $ dx = hq2_rx(t)
            $ dy = hq2_ry(y)
            add Solid("#4fc9b0") pos (dx - 6, dy - 1) xysize (12, 2)
            add Solid("#4fc9b0") pos (dx - 1, dy - 6) xysize (2, 12)
            add Solid("#cfe9e3") pos (dx - 2, dy - 2) xysize (4, 4)
        for n in range(0, 121, 20):
            text str(n) pos (hq2_rx(n) - 8, 196) font HQ2_FONT size 14 color "#6f8a99"
        text "ночь" pos (1390, 196) font HQ2_FONT size 14 color "#6f8a99"

        text "наша догадка: через сколько суток объект повторяется" pos (28, 226) font HQ2_FONT size 18 color "#6f8a99"
        if live:
            bar value VariableValue("hq2_slider", 1.0) pos (28, 258) xysize (1100, 26)
        else:
            bar value StaticValue(hq2_slider, 1.0) pos (28, 258) xysize (1100, 26)
        text (("%.2f" % P).replace(".", ",") + " суток") pos (1160, 248) font HQ2_FONT size 30 color "#8ff0dc"
        hbox:
            pos (1160, 296)
            spacing 8
            textbutton "-0,05" sensitive live action SetVariable("hq2_slider", max(0.0, hq2_slider - 0.05 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"
            textbutton "-0,01" sensitive live action SetVariable("hq2_slider", max(0.0, hq2_slider - 0.01 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"
            textbutton "+0,01" sensitive live action SetVariable("hq2_slider", min(1.0, hq2_slider + 0.01 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"
            textbutton "+0,05" sensitive live action SetVariable("hq2_slider", min(1.0, hq2_slider + 0.05 / 14.0)) text_font HQ2_FONT text_size 18 text_color "#cfe9e3"

        text ("картина: " + quality) pos (28, 300) font HQ2_FONT size 18 color "#8ff0dc"
        add Solid("#1b2535") pos (330, 304) xysize (300, 12)
        add Solid("#8ff0dc") pos (330, 304) xysize (max(2, m_fill), 12)
        add Solid("#e0a030") pos (330 + m_mark, 298) xysize (2, 24)
        text "порог шума" pos (330 + m_mark - 36, 322) font HQ2_FONT size 14 color "#e0a030"
        text "тот же ряд, сложенный по этому периоду: одинаковые фазы лежат друг над другом" pos (28, 340) font HQ2_FONT size 16 color "#6f8a99"

        add Solid("#1b2535") pos (40, 560) xysize (1400, 2)
        for f, y in pts:
            $ fx = int(40 + f * 1400)
            $ fy = hq2_fy(y)
            add Solid("#8ff0dc") pos (fx - 6, fy - 1) xysize (12, 2)
            add Solid("#8ff0dc") pos (fx - 1, fy - 6) xysize (2, 12)
            add Solid("#ffffff") pos (fx - 2, fy - 2) xysize (4, 4)
        for rx, ry, rw, rh in steps:
            add Solid("#BA7517") pos (rx, ry) xysize (rw, rh)
        text "0" pos (40, 568) font HQ2_FONT size 16 color "#6f8a99"
        text (("%.2f" % P).replace(".", ",") + " суток") pos (1300, 568) font HQ2_FONT size 16 color "#6f8a99"
        text "янтарная ступенька — среднее яркости в каждом из 8 столбцов" pos (500, 568) font HQ2_FONT size 16 color "#BA7517"

        button:
            pos (28, 620)
            xysize (360, 44)
            background Solid("#12303a")
            hover_background Solid("#1b3040")
            sensitive live
            action Return("lock")
            text "зафиксировать период" font HQ2_FONT size 20 color "#8ff0dc" align (0.5, 0.5)


screen hq2_halves():
    zorder 30
    $ h = len(HQ2_T) // 2
    $ pts1, line1, sc1 = hq2_fold(7.0, HQ2_T[:h], HQ2_Y[:h])
    $ pts2, line2, sc2 = hq2_fold(7.0, HQ2_T[h:], HQ2_Y[h:])
    $ steps1 = hq2_steps(line1, 40, 640)
    $ steps2 = hq2_steps(line2, 780, 640)

    fixed:
        pos (210, 30)
        xysize (1500, 690)
        add Solid("#0b1018f2")

        text "проверка: ряд пополам, каждая половина отдельно, период 7 суток" pos (28, 18) font HQ2_FONT size 20 color "#6f8a99"
        text "первая половина (ночи 0–59)" pos (40, 300) font HQ2_FONT size 18 color "#8ff0dc"
        text "вторая половина (ночи 60–119)" pos (780, 300) font HQ2_FONT size 18 color "#8ff0dc"

        add Solid("#1b2535") pos (40, 560) xysize (640, 2)
        add Solid("#1b2535") pos (780, 560) xysize (640, 2)
        for f, y in pts1:
            $ fx = int(40 + f * 640)
            $ fy = hq2_fy(y)
            add Solid("#8ff0dc") pos (fx - 6, fy - 1) xysize (12, 2)
            add Solid("#8ff0dc") pos (fx - 1, fy - 6) xysize (2, 12)
            add Solid("#ffffff") pos (fx - 2, fy - 2) xysize (4, 4)
        for f, y in pts2:
            $ fx = int(780 + f * 640)
            $ fy = hq2_fy(y)
            add Solid("#8ff0dc") pos (fx - 6, fy - 1) xysize (12, 2)
            add Solid("#8ff0dc") pos (fx - 1, fy - 6) xysize (2, 12)
            add Solid("#ffffff") pos (fx - 2, fy - 2) xysize (4, 4)
        for rx, ry, rw, rh in steps1:
            add Solid("#BA7517") pos (rx, ry) xysize (rw, rh)
        for rx, ry, rw, rh in steps2:
            add Solid("#BA7517") pos (rx, ry) xysize (rw, rh)
        text "0" pos (40, 568) font HQ2_FONT size 16 color "#6f8a99"
        text "7 суток" pos (620, 568) font HQ2_FONT size 16 color "#6f8a99"
        text "0" pos (780, 568) font HQ2_FONT size 16 color "#6f8a99"
        text "7 суток" pos (1360, 568) font HQ2_FONT size 16 color "#6f8a99"


label hidden_quest_start:
    if hq2_prediction_made and not hq2_confirmed and current_task >= 4:
        call hq2_confirmation
        jump desktop_loop
    if hidden_quest_phase2_done:
        "Нет ничего нового."
        jump desktop_loop
    if hidden_quest_phase1_done and task2_secret_access:
        jump hidden_quest2_intro
    if hidden_quest_phase1_done:
        "Ничего нового."
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
    show screen hq2_fold(False)
    with dissolve
    sasha "Ну, это явно нам неинтересно. Что мы понимаем в этих цветных точках."
    player "На самом деле, я должен признаться тебе, что я — астроном-любитель."
    player "Если честно, звёздное небо — это буквально последнее, что я помню, перед тем как очнуться здесь. И мне кажется... я готовился совершить открытие. За этим я и поехал за город, когда... всё произошло."
    "..."
    player "Меня вот ещё что интересует: зачем супермаркетам наблюдения за звёздным небом? Нет, мы обязаны это разгадать."
    sasha "Но как? На что мы вообще смотрим? Это же ерунда какая-то, как из этого сделать смысл?"
    player "Думаю, мы смотрим на такую штуку, которая называется «периодограмма»."
    sasha "Ты не сделал мне смысл."

    window hide
    menu:
        "Звучать солидно.":
            player "Ну, Санёк, это же просто. Периодограмма — это оценка спектральной плотности мощности, основанная на вычислении квадрата модуля преобразования Фурье последовательности данных."
            sasha "Тебе там учительница в школе матешу объясняла, да?"
        "Звучать искренне.":
            player "Ну, Санёк... Представь тёмную комнату, а в ней одновременно тикают все часы мира. Периодограмма — это такой слух, который слышит, какие часы тикают громче всех. Во-от."
            sasha "На таких выкрутасах формулировок меня не обучали."

    player "Ладно, давай проще. Есть такая штука — переменная звезда. У неё блеск меняется со временем: то ярче, то тусклее. Вот такие картинки астрономы и рисуют, чтобы понять, как именно."
    player "Странно... Имени своего не помню, а как с такими рядами работать — помню. Может, я и не аналитиком был, а астрономом?.."
    player "В любом случае. Одна точка — одна ночь. Выше точка — ярче объект. Часть ночей пропущена: облака, лень, поломки."
    sasha "И что тут можно понять?"
    player "Например, регулярные у нас изменения яркости или нерегулярные."
    sasha "Ну, тут явно нерегулярные."
    player "А может и нет. Смотри."

    call hq2_demo_sweep

    sasha "Стой. Вернись. Там что-то мелькнуло."
    player "Вот именно. Мелькнуло и пропало."
    player "Вообще-то настоящая периодограмма всё считает сама. Но у нас дырявый ряд и никаких инструментов, поэтому делаем то же самое руками."
    player "Смотри. Ползунок — наша догадка про период. Мы режем весь ряд на куски такой длины и налкадывает друг на друга. Попали в период — яркие ночи лягут в одно место, и вырастет горб. Не попали — каша."
    player "Янтарные линии наверху показывают, где мы режем ряд. Нижний график — результат наложения, янтарные ступеньки на нём — среднее в каждом столбце. А надпись «картина» и шкала рядом показывают, насколько точки собрались вместе. Жёлтая отметка на шкале — порог шума: ниже неё картина вполне может быть случайной."
    sasha "То есть крутим, пока не вырастет горб."
    player "Крутим и не обманываемся: «чётко» не всегда значит «верно»."
    sasha "Ну давай. Впечатли меня."

    $ hq2_wrong_locks = 0
    $ hq2_hint_shown = False
    $ hq2_slider = 0.2
    jump hidden_quest2_fold_loop


label hq2_demo_sweep:
    window hide
    $ renpy.block_rollback()
    $ hq2_slider = 1.0 / 14.0
    $ renpy.pause(0.7, hard=True)
    $ hq2_run_sweep()
    $ renpy.pause(0.6, hard=True)
    $ hq2_slider = 0.2
    window show
    return


label hidden_quest2_fold_loop:
    call screen hq2_fold(True)
    show screen hq2_fold(False)
    $ hq2_P = hq2_period()
    $ hq2_kind = hq2_lock_kind(hq2_P)
    if hq2_kind == "ok":
        jump hidden_quest2_fold_ok

    if hq2_kind == "near":
        player "Почти. Картина ещё не чёткая, подкрутим чуть-чуть."
        jump hidden_quest2_fold_loop

    $ hq2_wrong_locks += 1
    if hq2_kind == "x2":
        player "Горбов два. Значит, настоящий период вдвое короче."
    elif hq2_kind == "half":
        player "Горб один, но в каждом втором цикле на его месте нет наблюдений. Проверь период вдвое длиннее."
    elif hq2_kind == "third":
        player "Горб есть, но неделя делится на три части. Настоящий период длиннее."
    else:
        player "Каша. Точки лежат как попало."
    if hq2_wrong_locks >= 2 and not hq2_hint_shown:
        $ hq2_hint_shown = True
        sasha "Смотри на янтарные ступеньки. Они должны вздыматься одним горбом, сам сказал."
    jump hidden_quest2_fold_loop


label hidden_quest2_fold_ok:
    $ hq2_pts = hq2_points(hq2_wrong_locks)
    $ accuracy += hq2_pts
    $ hidden_quest_phase2_done = True

    hide screen hq2_fold
    player "Теперь проверим честно. Разрежем ряд пополам и сложим каждую половину отдельно."
    show screen hq2_halves
    with dissolve
    "..."
    sasha "... и обе дают горб в одном и том же месте. Это уже не шум."
    "..."
    player "Ровно семь суток. Тоже чувствуешь это?.."
    "Беспорядочные хлопья в твоих мыслях складываются в паззл."
    sasha "Совпадение? Я начинаю уставать от этого слова."
    player "У магазина и у объекта в небе один и тот же ритм. Что у них может быть общего?"
    sasha "Или кто. Яркость вообще какого объекта тут наблюдается? Это звезда?"
    player "Звезда... Саша, вряд ли это звезда. Я не знаю, что именно это такое, но оно в небе и оно горит ярче каждые семь дней."
    hide screen hq2_halves
    with dissolve

    $ unlock_achievement("zvezdochet")
    jump hq2_falsify
