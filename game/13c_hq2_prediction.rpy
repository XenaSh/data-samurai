# === 13c_hq2_prediction.rpy — скрытый квест, фаза 2: «Апофения» и предсказание вспышки ===
# Зависит от 13b_hidden_quest_p2.rpy: HQ2_T, HQ2_Y, HQ2_FONT, hq2_points-логика не нужна.

define HQ2P_FALS_MAX = 3
define HQ2P_PRED_MAX = 4
define HQ2P_MIN = 1

default hq2_fals_wrong = 0
default hq2_pred_wrong = 0
default hq2_pred_hint = False
default hq2_pred_night = 0
default hq2_prediction_made = False
default hq2_confirmed = False


init python:

    def hq2p_x(t, a=80, b=133):
        return int(40 + (t - a) / float(b - a) * 1400)

    def hq2p_y(v):
        return int(420 - (v - 6) / 13.0 * 230)

    def hq2p_points(wrong, top):
        return max(HQ2P_MIN, top - wrong)


screen hq2_predict(live=True):
    zorder 30

    fixed:
        pos (210, 30)
        xysize (1500, 690)
        add Solid("#0b1018f2")

        text "sky_log: что будет дальше?" pos (28, 18) font HQ2_FONT size 20 color "#6f8a99"
        text "нажми на ночь, в которую ждёшь следующую вспышку" pos (28, 52) font HQ2_FONT size 16 color "#6f8a99"
        text "по горизонтали номер ночи, по вертикали яркость: выше точка — ярче" pos (28, 76) font HQ2_FONT size 16 color "#6f8a99"

        for t in range(120, 134):
            add Solid("#8ff0dc0d") pos (hq2p_x(t) - 12, 170) xysize (24, 250)

        for t in range(84, 134, 7):
            add Solid("#BA751766") pos (hq2p_x(t), 170) xysize (2, 250)

        if hq2_pred_hint:
            for t in range(85, 120, 7):
                add Solid("#BA751744") pos (hq2p_x(t) - 8, 170) xysize (16, 250)
            text "так ложился ритм раньше" pos (hq2p_x(85) - 20, 142) font HQ2_FONT size 14 color "#BA7517"

        add Solid("#1b2535") pos (40, 420) xysize (1413, 2)
        for t, y in zip(HQ2_T, HQ2_Y):
            if t >= 80:
                $ px = hq2p_x(t)
                $ py = hq2p_y(y)
                add Solid("#4fc9b0") pos (px - 6, py - 1) xysize (12, 2)
                add Solid("#4fc9b0") pos (px - 1, py - 6) xysize (2, 12)
                add Solid("#cfe9e3") pos (px - 2, py - 2) xysize (4, 4)

        for n in range(80, 131, 10):
            text str(n) pos (hq2p_x(n) - 8, 428) font HQ2_FONT size 14 color "#6f8a99"
        text "ночь" pos (1400, 428) font HQ2_FONT size 14 color "#6f8a99"
        text "сегодня" pos (hq2p_x(120) - 28, 142) font HQ2_FONT size 16 color "#8ff0dc"
        text "завтра" pos (hq2p_x(121) - 20, 118) font HQ2_FONT size 16 color "#6f8a99"

        if hq2_pred_night >= 120:
            $ pick_x = hq2p_x(hq2_pred_night)
            add Solid("#8ff0dc44") pos (pick_x - 13, 170) xysize (26, 250)
            text "твой выбор" pos (min(pick_x - 40, 1380), 450) font HQ2_FONT size 16 color "#8ff0dc"

        text "янтарные линии режут ряд на куски по 7 суток" pos (28, 500) font HQ2_FONT size 16 color "#BA7517"

        for t in range(120, 134):
            button:
                pos (hq2p_x(t) - 13, 170)
                xysize (26, 250)
                background None
                hover_background Solid("#8ff0dc22")
                sensitive live
                action Return(t)


screen hq2_confirm():
    zorder 30

    fixed:
        pos (210, 30)
        xysize (1500, 690)
        add Solid("#0b1018f2")

        text "sky_log: ночь 120" pos (28, 18) font HQ2_FONT size 20 color "#6f8a99"

        for t in range(84, 121, 7):
            add Solid("#BA751766") pos (hq2p_x(t, 80, 120), 170) xysize (2, 250)
        add Solid("#1b2535") pos (40, 420) xysize (1413, 2)
        for t, y in zip(HQ2_T, HQ2_Y):
            if t >= 80:
                $ px = hq2p_x(t, 80, 120)
                $ py = hq2p_y(y)
                add Solid("#4fc9b0") pos (px - 6, py - 1) xysize (12, 2)
                add Solid("#4fc9b0") pos (px - 1, py - 6) xysize (2, 12)
                add Solid("#cfe9e3") pos (px - 2, py - 2) xysize (4, 4)

        $ nx = hq2p_x(120, 80, 120)
        $ ny = hq2p_y(15.6)
        add Solid("#e0a030") pos (nx - 10, ny - 2) xysize (20, 4)
        add Solid("#e0a030") pos (nx - 2, ny - 10) xysize (4, 20)
        add Solid("#ffffff") pos (nx - 3, ny - 3) xysize (6, 6)
        add Solid("#e0a030") pos (nx - 1, 170) xysize (2, 80)
        text "ночь 120: вспышка" pos (nx - 170, 142) font HQ2_FONT size 18 color "#e0a030"
        text "ты ждал её именно здесь" pos (nx - 220, 450) font HQ2_FONT size 18 color "#8ff0dc"

        for n in range(80, 121, 10):
            text str(n) pos (hq2p_x(n, 80, 120) - 8, 428) font HQ2_FONT size 14 color "#6f8a99"


label hq2_falsify:
    hide screen hq2_halves
    "Ты закрываешь журнал. Или отключаешься от него. Или... как ты вообще это делаешь?"
    scene bg_terminal with dissolve
    window show
    sasha "Аналитик, а не пал ли ты жертвой апофении?"
    player "Чего?"
    sasha "Ну, апофения. Это когда мозг сам достраивает закономерность там, где её нет. Ты вот по сути что сделал: наугад подбирал период, пока у тебя не вырос «горб». А не мог ли горб вырасти сам, случайно?"
    player "... Дай мне подумать над этим. Как мне доказать или опровергнуть, что мой вывод реален, а не шум?"
    $ hq2_fals_wrong = 0
    jump hq2_falsify_menu


label hq2_falsify_menu:
    window hide
    menu:
        "Перебрать ещё периодов: вдруг найдётся картина получше.":
            $ hq2_fals_wrong += 1
            sasha "Xем больше перебираешь, тем красивее горб найдётся и в шуме. Это апофения и есть."
            jump hq2_falsify_menu
        "Сравнить с соседним объектом.":
            $ hq2_fals_wrong += 1
            sasha "В логе других объектов нет. Сравнивать не с чем."
            jump hq2_falsify_menu
        "Поверить: горб же красивый.":
            $ hq2_fals_wrong += 1
            player "Красивый же. Ну... красивый."
            sasha "Даже и не знаю, что сказать на такое."
            jump hq2_falsify_menu
        "Предсказать следующую вспышку и подождать.":
            $ accuracy += hq2p_points(hq2_fals_wrong, HQ2P_FALS_MAX)
            player "Гипотеза чего-то стоит, только если могла провалиться. Предскажем, что будет дальше, и посмотрим."
            sasha "Ага. Принцип фальсифицируемости."
            player "Вот-вот, а ты думал, чего физика так любит эксперименты? Эксперимент нужен не только чтобы узнать, что будет если то и то. Эксперимент это возможность сделать предсказание на основе своей теории и проверить, бьётся ли оно с реальностью."
            jump hq2_predict_loop_start


label hq2_predict_loop_start:
    $ hq2_pred_wrong = 0
    $ hq2_pred_hint = False
    $ hq2_pred_night = 0
    jump hq2_predict_loop


label hq2_predict_loop:
    call screen hq2_predict(True)
    show screen hq2_predict(False)
    $ hq2_pred_night = _return
    if hq2_pred_night == 120:
        jump hq2_predict_ok

    $ hq2_pred_wrong += 1
    $ hq2_pred_hint = True
    if hq2_pred_night > 120:
        sasha "Ты мне тут хотел следующую выспышку предсказать, а не любую."
    else:
        sasha "Не сходится с твоей же картинкой."
    sasha "Посмотри, где вспышки были раньше."
    jump hq2_predict_loop

    if hq2_pred_night == 121:
        $ hq2_pred_hint = True
        sasha "Близко: это хвост вспышки, но пик у неё раньше. Ритм считай по пикам."
        jump hq2_predict_loop

label hq2_predict_ok:
    $ accuracy += hq2p_points(hq2_pred_wrong, HQ2P_PRED_MAX)
    $ hq2_prediction_made = True
    player "Сегодня. Следующая вспышка должна быть сегодня."
    sasha "Сегодня? То есть прямо сейчас? Ты хоть понимаешь, что это значит?"
    player "Если я прав, ночью объект вспыхнет. Если нет, моя гипотеза мертва."
    sasha "Тогда нам остаётся только ждать."
    sasha "Что ж... давай поработаем, так и время пройдет быстрее."
    hide screen hq2_predict
    jump desktop_loop


label hq2_confirmation:
    if not hq2_prediction_made or hq2_confirmed:
        return
    $ hq2_confirmed = True
    window show
    show screen hq2_confirm
    with dissolve
    sasha "Он вспыхнул. Ночью. Ровно тогда, когда ты сказал."
    player "..."
    "Здесь что-то важно. Что-то очень важно."
    player "..."
    "Тихая ночь за городом. Что ты искал? Почему ты приехал туда, самурай? Что говорит тебе твоя катана — разум твой?"
    hide screen hq2_confirm
    with dissolve
    return
