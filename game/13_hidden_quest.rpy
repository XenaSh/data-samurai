# === 13_hidden_quest.rpy (сгенерировано из script.rpy, модуль: hidden_quest) ===

default hero_noticed_point_d = False




define nq_factors = {
    "g1": {"label": "Экономия на масштабе", "group": "growth"},
    "g2": {"label": "Замещение труда капиталом", "group": "growth"},
    "d1": {"label": "Чувствительность к процентным ставкам", "group": "decline"},
    "d2": {"label": "Риск операционного исполнения", "group": "decline"},
    "d3": {"label": "Риски качества менеджмента", "group": "decline"}
}


define nq_paragraphs = [
    [{"type": "text", "content": "Когда пресс-служба «Изобилия» назвала свой новый логистический комплекс «Меридиан-7», журналисты бросились искать смысл: географическую широту, тайный код, отсылку к орбитальной станции. Оказалось проще. «Звучит внушительно», признались в компании, и на этом смысловые изыскания можно было заканчивать."}],

    [{"type": "text", "content": "Внушительности комплексу, впрочем, действительно хватает."},
     {"type": "click", "id": 0, "content": "Расположенный в Подмосковье центр рассчитан на обработку до 40 тысяч заказов в сутки — втрое больше, чем нынешний флагманский склад компании, который до сих пор считался гордостью логистической службы, а теперь скромно отходит на второй план."},
     {"type": "text", "content": "У входа обещают установить семиметровую вращающуюся скульптуру из картонных коробок."},
     {"type": "click", "id": 1, "content": "«Выдающееся авангардное произведение, отражающее свою атрибуцию к доктрине солипсизма», — объяснил директор по логистике, явно гордый находкой, которая войдёт в историю корпоративного искусства."}],

    [{"type": "text", "content": "Того же директора пришлось выслушать дважды."},
     {"type": "click", "id": 2, "content": "На церемонии закладки первого камня микрофон отключился ровно на середине фразы «это будет флагман логистики будущего», и фразу пришлось повторить целиком."},
     {"type": "text", "content": "Судя по всему, будущее терпеливо и вполне готово ждать."}],

    [{"type": "text", "content": "За кулисами торжества, впрочем, скрывается вполне серьёзная математика."},
     {"type": "click", "id": 3, "content": "По расчётам компании, на единицу обработанного груза новому центру потребуется впятеро меньше сотрудников, чем на складах с ручной сортировкой:"},
     {"type": "text", "content": "автоматизация делает своё дело скромнее, чем скульптуры из коробок, но эффективнее."},
     {"type": "click", "id": 4, "content": "Часть освободившихся людей переведут на свежесозданную должность «штурман дрона». Вакансия уже висит на сайте, а из требований — уверенное владение джойстиком и полное отсутствие страха высоты, что звучит куда авантюрнее, чем «логист»."}],

    [{"type": "click", "id": 5, "content": "Сам объект обошёлся компании в 4.8 миллиарда рублей, из которых 70% — кредит на семь лет под плавающую ставку:"},
     {"type": "text", "content": "сумма, при которой квартальные отчёты «Изобилия» будут читаться с особым интересом ещё довольно долго."},
     {"type": "click", "id": 6, "content": "Возглавит его, к слову, человек со стороны: бывший СЕО крупного агрохолдинга, прославившийся созданием «органического куриного яйца премиум-класса» и теперь готовый применить те же управленческие принципы к посылкам."},
     {"type": "click", "id": 7, "content": "Совпадение ли, что почти в то же время отдел кадров компании провёл внеплановый тренинг по управлению стрессом, участники которого, по слухам, шутили, что тренинг не помешал бы и самому тренеру, остаётся на суд читателя."}],

    [{"type": "click", "id": 8, "content": "Открытие центра, к слову, уже дважды переносили: сейчас срок сдвинулся из-за того, что часть конвейерных лент застряла на таможне на четыре месяца."},
     {"type": "text", "content": "Новую дату в компании пока не называют, ограничившись формулировкой «в ближайшее время». Пресс-служба уточнила, что готова обновить график, как только груз пройдёт таможенное оформление."}],

    [{"type": "click", "id": 9, "content": "Гостям церемонии, впрочем, обещают всё же показать семиметровую скульптуру из картонных коробок — на этот раз, надеются в компании, при исправно работающем микрофоне."}]
]

# Приглушённая "вспышка" вместо резкого чисто-белого мигания — снижает риск
# фотосенситивной реакции. Используем как замену резкому "show flash_soft with flash".
image flash_soft = Solid("#4a5568")

init python:
    def nq_hyperlink_callback(value):
        store.nq_selected_sentence = int(value)
        renpy.restart_interaction()
        return None
    config.hyperlink_callback = nq_hyperlink_callback

    def nq_pair_factor(key):
        if store.nq_selected_sentence is None:
            return
        for k in list(store.nq_pairs.keys()):
            if store.nq_pairs[k] == store.nq_selected_sentence:
                del store.nq_pairs[k]
        store.nq_pairs[key] = store.nq_selected_sentence
        store.nq_selected_sentence = None
        renpy.restart_interaction()

    def nq_color_for(sentence_id):
        if store.nq_selected_sentence == sentence_id:
            return "#ffe066"
        for k, v in store.nq_pairs.items():
            if v == sentence_id:
                return "#5fd9c4" if nq_factors[k]["group"] == "growth" else "#ff66ff"
        return "#c8d4d4"

    def nq_render_paragraph(blocks):
        parts = []
        for b in blocks:
            if b["type"] == "text":
                parts.append(b["content"])
            else:
                color = nq_color_for(b["id"])
                parts.append("{a=%d}{color=%s}%s{/color}{/a}" % (b["id"], color, b["content"]))
        return " ".join(parts)


screen news_sentence_match_screen():
    modal True
    zorder 200

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1460
        ysize 840
        background Solid("#05161a")

        vbox:
            frame:
                background Solid("#256a6a")
                xfill True
                padding (20, 11)
                text "document_reader.exe — Меридиан-7.doc" color "#08201f" size 15 bold True

            hbox:
                frame:
                    background Solid("#05161a")
                    xsize 1100
                    ysize 780
                    padding (40, 34)
                    viewport:
                        xsize 1020
                        ysize 712
                        scrollbars "vertical"
                        mousewheel True
                        vbox:
                            spacing 16
                            text "«Изобилие» открывает центр обработки заказов «Меридиан-7»" color "#eeeeee" size 22 bold True xsize 1000
                            null height 6
                            for para in nq_paragraphs:
                                text nq_render_paragraph(para) color "#c8d4d4" size 20 xsize 950 line_spacing 6

                frame:
                    background Solid("#256a6a")
                    xsize 2
                    ysize 780

                frame:
                    background Solid("#05161a")
                    xsize 356
                    ysize 780
                    padding (26, 26)
                    vbox:
                        spacing 14
                        text "ФАКТОРЫ РОСТА" color "#8fd8d0" size 12
                        null height 4
                        for key, f in nq_factors.items():
                            if f["group"] == "growth":
                                $ is_paired = key in nq_pairs
                                button:
                                    action Function(nq_pair_factor, key)
                                    background None
                                    hover_background None
                                    padding (0, 0)
                                    hbox:
                                        spacing 10
                                        if is_paired:
                                            frame:
                                                background Solid("#5fd9c4")
                                                xsize 18
                                                ysize 18
                                        else:
                                            frame:
                                                background Solid("#2a5555")
                                                xsize 18
                                                ysize 18
                                                frame:
                                                    background Solid("#05161a")
                                                    xsize 13
                                                    ysize 13
                                                    xalign 0.5
                                                    yalign 0.5
                                        text f["label"] color ("#5fd9c4" if is_paired else "#7a9a9a") size 14

                        null height 16
                        text "ФАКТОРЫ РИСКА" color "#d8b88f" size 12
                        null height 4
                        for key, f in nq_factors.items():
                            if f["group"] == "decline":
                                $ is_paired = key in nq_pairs
                                button:
                                    action Function(nq_pair_factor, key)
                                    background None
                                    hover_background None
                                    padding (0, 0)
                                    hbox:
                                        spacing 10
                                        if is_paired:
                                            frame:
                                                background Solid("#e8a655")
                                                xsize 18
                                                ysize 18
                                        else:
                                            frame:
                                                background Solid("#55442a")
                                                xsize 18
                                                ysize 18
                                                frame:
                                                    background Solid("#05161a")
                                                    xsize 13
                                                    ysize 13
                                                    xalign 0.5
                                                    yalign 0.5
                                        text f["label"] color ("#e8a655" if is_paired else "#9a8a7a") size 14

                        null height 120
                        textbutton "Заверить":
                            xsize 304
                            text_size 16
                            text_color "#0a1518"
                            background Solid("#ffe066")
                            padding (30, 14)
                            xalign 0.5
                            action Return(True)


define pd_sentences = [
    {"type": "text", "content": "В соответствии с внутренним регламентом раскрытия информации о существенных фактах хозяйственной деятельности, настоящим доводится до сведения заинтересованных лиц нижеследующее."},
    {"type": "click", "id": 0, "content": "В отчётном периоде Инвестиционная группа «Норд-Капитал» приобрела долю участия в размере 51% в уставном капитале Общества с ограниченной ответственностью «Розничная точка №14», осуществляющего деятельность под коммерческим обозначением «торговая точка «Д» сети «Изобилие»."},
    {"type": "text", "content": "Ранее указанная доля принадлежала региональному франчайзи на основании договора коммерческой концессии, не подлежащего раскрытию в настоящей публикации в силу режима коммерческой тайны."},
    {"type": "click", "id": 1, "content": "Сумма сделки сторонами не раскрывается, что соответствует обычной практике при сделках такого рода."},
    {"type": "click", "id": 2, "content": "Представители Инвестиционной группы «Норд-Капитал» отметили, что смена собственника не повлияет на операционную деятельность указанной торговой точки, ассортиментную политику и кадровый состав."},
    {"type": "click", "id": 3, "content": "От сети «Изобилие» комментариев получить не удалось: запрос находился на рассмотрении у пресс-службы согласно внутреннему регламенту."},
    {"type": "click", "id": 4, "content": "Сделка зарегистрирована в реестре в третьем квартале текущего года."},
    {"type": "text", "content": "Настоящая публикация подготовлена в справочных целях и не является рекомендацией к совершению каких-либо действий."}
]


init python:
    def pd_toggle(idx):
        if idx in pd_selected:
            pd_selected.discard(idx)
        else:
            pd_selected.add(idx)
        renpy.restart_interaction()


screen point_d_article_screen():
    modal True
    zorder 200

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1460
        ysize 840
        background Solid("#05161a")

        vbox:
            frame:
                background Solid("#256a6a")
                xfill True
                padding (20, 11)
                text "document_reader.exe — Корпоративный вестник.doc" color "#08201f" size 15 bold True

            hbox:
                frame:
                    background Solid("#05161a")
                    xsize 1100
                    ysize 780
                    padding (40, 34)
                    vbox:
                        spacing 16
                        text "Корпоративный вестник — раздел «Изменения в структуре собственности»" color "#eeeeee" size 22 bold True xsize 1020
                        null height 6
                        for block in pd_sentences:
                            if block["type"] == "text":
                                text block["content"] color "#c8d4d4" size 16 xsize 1020 line_spacing 6
                            else:
                                $ is_sel = block["id"] in pd_selected
                                textbutton block["content"]:
                                    text_color ("#ffe066" if is_sel else "#c8d4d4")
                                    text_size 16
                                    text_line_spacing 6
                                    xsize 1020
                                    background None
                                    hover_background None
                                    padding (0, 0)
                                    action Function(pd_toggle, block["id"])

                frame:
                    background Solid("#256a6a")
                    xsize 2
                    ysize 780

                frame:
                    background Solid("#05161a")
                    xsize 356
                    ysize 780
                    padding (26, 26)
                    vbox:
                        spacing 18
                        text "НЕИЗВЕСТНЫЙ ФАКТОР" color "#8fd8d0" size 12
                        null height 8
                        $ pd_count = len(pd_selected)
                        for i in range(4):
                            hbox:
                                spacing 10
                                if i < pd_count:
                                    frame:
                                        background Solid("#ffe066")
                                        xsize 18
                                        ysize 18
                                else:
                                    frame:
                                        background Solid("#3a5555")
                                        xsize 18
                                        ysize 18
                                        frame:
                                            background Solid("#05161a")
                                            xsize 13
                                            ysize 13
                                            xalign 0.5
                                            yalign 0.5
                                text "?" color ("#ffe066" if i < pd_count else "#3a5555") size 16
                        null height 400
                        textbutton "Заверить":
                            xsize 304
                            sensitive (pd_count >= 3)
                            text_size 16
                            text_color ("#0a1518" if pd_count >= 3 else "#5a8a8a")
                            background (Solid("#ffe066") if pd_count >= 3 else Solid("#132a2a"))
                            padding (20, 14)
                            xalign 0.5
                            action Return(True)

# Экран завершения фазы 1

init python:
    import random

    def scalp_tick():
        global scalp_price
        delta = (random.random() - 0.5) * 3
        scalp_price = max(60.0, min(140.0, scalp_price + delta))
        scalp_history.append(scalp_price)
        if len(scalp_history) > 20:
            scalp_history.pop(0)
        renpy.restart_interaction()

    def scalp_open(direction):
        global scalp_position, scalp_entry_price
        scalp_position = direction
        scalp_entry_price = scalp_price

    def scalp_reset_round():
        global scalp_position, scalp_entry_price, scalp_price, scalp_history
        scalp_position = None
        scalp_entry_price = 0.0
        scalp_price = 100.0
        scalp_history = [100.0]


screen scalp_screen():
    modal True
    zorder 200

    timer 0.4 repeat True action Function(scalp_tick)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1040
        ysize 740
        background Solid("#05161acc")

        vbox:
            frame:
                background Solid("#2a7a7a")
                xfill True
                padding (23, 18)
                hbox:
                    xfill True
                    text "условный тикер // воображаемые деньги" color "#08201f" size 16
                    text ("Банк: %+d" % scalp_bank) color "#08201f" size 18 bold True xalign 1.0

            frame:
                background None
                padding (44, 30)
                vbox:
                    spacing 8
                    hbox:
                        spacing 16
                        text ("%.2f" % scalp_price) color "#ffe066" size 54 font "fonts/JetBrainsMono-Regular.ttf"
                        $ scalp_delta = scalp_history[-1] - scalp_history[-2] if len(scalp_history) >= 2 else 0
                        text ("%s %.2f" % ("^" if scalp_delta >= 0 else "v", abs(scalp_delta))) color ("#3ddc84" if scalp_delta >= 0 else "#ff7878") size 20 yalign 0.5

                    null height 18

                    fixed:
                        xsize 920
                        ysize 220
                        $ hist = scalp_history[-16:]
                        $ vmin = min(hist) - 1 if hist else 0
                        $ vmax = max(hist) + 1 if hist else 1
                        $ n = len(hist)
                        $ bar_w = 920.0 / max(n, 1)
                        for i in range(1, n):
                            $ prev_v = hist[i-1]
                            $ this_v = hist[i]
                            $ y_prev = 220 - (prev_v - vmin) / (vmax - vmin) * 220
                            $ y_this = 220 - (this_v - vmin) / (vmax - vmin) * 220
                            $ bar_top = min(y_prev, y_this)
                            $ bar_bottom = max(y_prev, y_this)
                            $ bar_color = "#3ddc84" if this_v >= prev_v else "#ff7878"
                            frame:
                                background Solid(bar_color)
                                xpos int(i * bar_w)
                                ypos int(bar_top)
                                xsize max(int(bar_w * 0.6), 4)
                                ysize max(int(bar_bottom - bar_top), 4)

                    null height 150

                    if scalp_position is None:
                        hbox:
                            xalign 0.5
                            spacing 20
                            textbutton "Купить":
                                action Function(scalp_open, "long")
                                text_size 18
                                text_color "#3ddc84"
                                background Solid("#123030")
                                padding (36, 16)
                            textbutton "Шортить":
                                action Function(scalp_open, "short")
                                text_size 18
                                text_color "#ffb84d"
                                background Solid("#302010")
                                padding (36, 16)
                    else:
                        hbox:
                            xfill True
                            text (("Открыта позиция: ДЛИННАЯ по %.2f" % scalp_entry_price) if scalp_position == "long" else ("Открыта позиция: КОРОТКАЯ по %.2f" % scalp_entry_price)) color "#c8d4d4" size 16
                            $ scalp_live_diff = (scalp_price - scalp_entry_price) if scalp_position == "long" else (scalp_entry_price - scalp_price)
                            text ("%+.2f" % scalp_live_diff) color ("#3ddc84" if scalp_live_diff >= 0 else "#ff7878") size 16 xalign 1.0
                        null height 12
                        textbutton "Закрыть позицию":
                            xfill True
                            text_size 20
                            text_bold True
                            text_color "#0a1518"
                            text_xalign 0.5
                            background Solid("#ffe066")
                            padding (20, 16)
                            action Return(True)


label hidden_quest_intro:
    window show
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal
    with dissolve

    player "Я... нажал на какой-то вопросительный знак. И ничего не произошло."
    sasha "О, ты про эту кнопку. Ну и ладно, можем сами себя развлечь."

    if hero_trading_backstory_known:
        sasha "Кстати, раз уж ты вспоминал биржу — не хочешь тряхнуть стариной?"
    else:
        sasha "Слушай, а вот интересно — у тебя должно быть какое-то чутьё на числа. Давай проверим на чём-нибудь азартном. На бирже, например."

    player "О какой бирже идёт речь?"
    sasha "Криптовалютной? Сырьевой? Нам подойдёт любая, где можно скальпить."
    player "Святые угодники, {i}И криптовалюта, И скальпинг{/i} — смерти моей нервной системы хочешь."
    player "..."
    player "Я за."
    sasha "Хи-хи."
    player "Только погоди, у нас вообще есть доступ к бирже? У нас вообще есть деньги? Как мы этим займёмся прямо на рабочем месте?"
    sasha "Ну давай хотя бы симулируем. Ну, азарта ради. А то что мы сидим, в самом деле."
    sasha "Представь, что ты играешь не против рынка, а против меня. И награду тебе тоже выдам я. Она будет ценной."
    sasha "Правила простые. Выбираешь направление, ждёшь момента, жмёшь «Закрыть». Можешь среагировать сразу и соскрести копейку почти без риска. А можешь подождать и попробовать соскрести уже десять. Или всё слить, если цена развернётся раньше, чем ты решишься."
    player "А если я слишком долго тяну?"
    sasha "Тогда рискуешь смотреть, как твоя воображаемая прибыль превращается в воображаемый убыток. Азарт, в общем-то, весь тут."
    sasha "Ты же помнишь, что значат лонг и шорт?"
    player "Галя, шорты. туземун!"
    sasha "... э, ладно."
    player "Камон, Саша, не сиди на заборе!"
    sasha "... Ладно."
    sasha "Поехали."

    $ scalp_bank = 0
    show image "images/scalp_bg_darkened.png" at Transform(fit="cover", size=(1920, 1080))
    with dissolve
    window hide
    jump hidden_quest_scalp_round


label hidden_quest_scalp_round:

    $ scalp_reset_round()
    call screen scalp_screen
    window hide

    $ scalp_diff = (scalp_price - scalp_entry_price) if scalp_position == "long" else (scalp_entry_price - scalp_price)
    $ scalp_bank += int(round(scalp_diff))

    if scalp_diff > 3:
        sasha "Недурно. Банк растёт."
        window hide
    elif scalp_diff > 0:
        sasha "Соскрёб копейку. Осторожно, но честно."
        window hide
    elif scalp_diff > -3:
        sasha "Небольшой минус. Бывает."
        window hide
    else:
        sasha "Ощутимый минус. Рынок не обязан быть добрым."
        window hide

    menu:
        "Ещё раз.":
            jump hidden_quest_scalp_round
        "Забрать банк и закончить.":
            jump hidden_quest_scalp_end


label hidden_quest_scalp_end:
    hide image "images/scalp_bg_darkened.png"
    with dissolve
    $ intuition += scalp_bank

    if scalp_bank >= 5:
        sasha "Забираешь [scalp_bank]. Не буду врать — впечатлён."
        player "Кто бы мог подумать, что во мне живёт биржевой хищник."
    elif scalp_bank > 0:
        sasha "Забираешь [scalp_bank]. Неплохо для несуществующих денег."
    elif scalp_bank == 0:
        sasha "Ушёл при своих. Тоже результат, в своём роде."
    elif scalp_bank > -5:
        sasha "Небольшой минус. Рынок редко бывает добрым с первого раза."
    else:
        sasha "Серьёзный минус, если что — я не шутил про ставки."
        player "Хорошо, что деньги воображаемые. Мою самооценку так легко не восстановить."

    player "А где мой приз за отвагу? Мне искать его на воображаемом счёте?"
    player "Ты обещал приз!"
    sasha "Уже загрузил в твою модель, не переживай."
    player "Что?"
    sasha "Ну, в твой профиль. Всему своё время."
    "Ты вспоминаешь, что начальник тоже упоминал какой-то профиль."
    "... может ли пробежать по спине, которую ты не чувствуешь, холодок?"
    player "Тортика не будет? Нет никакого тортика?"
    sasha "Может, он есть, но ты предпочёл бы, чтобы его не было, хи-хи."
    "Тебе становится неуютно."
    player "Так... сменим тему."

    jump hidden_quest_stocks_intro


label hidden_quest_stocks_intro:
    player "Знаешь, я вообще не любитель скальпинга. Я — долгосрочный инвестор!"
    sasha "Минуту назад ты был «Галя, шорты, туземун». Но ладно, слушаю."
    player "Это всё моя бабушка, её дурное влияние!"
    player "На самом деле, я взрослый рассудительный человек."
    player "Скальпинг — это азарт. А настоящие деньги делаются на терпении. Смотришь на компанию целиком, читаешь отчёты, корчишь умное лицо, ходишь важный на годовые собрания акционеров."
    player "Ну, сам-то я ещё ни на одно не ходил... не звали."
    player "Но принцип такой."
    sasha "Фундаментальный анализ. В духе дедушки Баффета: покупай не акцию, а бизнес, который за ней стоит."
    player "И-и-именно. Смотришь на отчётность, на то, кто владеет компанией, что происходит внутри, а не на то, куда ткнулась стрелочка за последнюю секунду."
    sasha "А на практике ты это как реализуешь-то? Читаешь новости и бросаешь монетку над заголовком?"
    "Тебе неприятно признавать, но пару раз как будто бы так и было."
    player "Ну нет, какие ещё монетки."
    player "Ищешь новости о компании и оцениваешь, что из них реально влияет на её стоимость. Сделки, слияния, запуски новых месторождений, геополитика."
    sasha "Звучит мутно. Как карты таро: видишь картинки в газетах и пытаешься истолковать, что бы оно такого тайного могло значить."
    sasha "На деле, какую бы новость ты не нашёл, рынок уже заложил всё в цену."
    sasha "А если тебе кажется, что лишь ты один видишь истину, которая сокрыта от всех других... Товарищ, это не слишком по-аналитически."
    player "Это потому что ты мыслишь как трейдер, Саша. Да, краткосрочные тренды уже заложены в цену. Я же пытаюсь по новостям понять, будет ли компания перспективна через двадцать лет."
    sasha "Астрология какая-то. Ты просто обязан показать мне, как по-твоему это работает, иначе не поверю."
    player "Неси новости и я раскидаю тебе всё по полочкам!"

    jump hidden_quest_news_stream


label hidden_quest_news_stream:
    $ nq_selected_sentence = None
    $ nq_pairs = {}

    call screen news_sentence_match_screen

    jump hidden_quest_news_debrief


label hidden_quest_news_debrief:
    sasha "Ну, показывай, что у тебя получилось."

    $ g1_pick = nq_pairs.get("g1")
    if g1_pick == 0:
        player "Сорок тысяч заказов в сутки, втрое больше прежнего — это экономия на масштабе."
        sasha "Чем больше объём, тем дешевле обходится каждая единица? Классика."
    elif g1_pick is not None:
        player "Экономия на масштабе — вот, держи."
        sasha "Это ты сейчас про что вообще прочитал? Там ни слова про объём производства."
        player "Ну... Звучало масштабно."
    else:
        sasha "Странно, что ты не выделил экономию на масштабе. Она там прямо в первых цифрах — сорок тысяч заказов, втрое больше прежнего центра."
        player "Пропустил, кажется."

    $ g2_pick = nq_pairs.get("g2")
    if g2_pick == 3:
        player "Нашёл про сотрудников на единицу груза. Не больше объёма, но меньше людей на тот же объём. Разные механизмы экономии."
        sasha "Ммм... кажется, твоё гадание на кофейной гуще как-то работает."
    elif g2_pick is not None:
        sasha "Замещение труда капиталом... это что-то из Маркса? Почему ты указал этот фактор именно так — там ни слова про людей и автоматизацию."
        player "Показалось похоже."
        sasha "На что?"
        player "На умное."
    else:
        sasha "Замещение труда капиталом — это что-то из Маркса, если вдруг интересно. Почему ты вообще не подкрепил этот тезис? Ах, да, потому что ты таролог!"

    $ d1_pick = nq_pairs.get("d1")
    if d1_pick == 5:
        player "Посмотри про 4.8 миллиарда под плавающую ставку — я специально зацепился за «плавающую». Кто знает, куда эта плавающая уплывёт."
        sasha "Кажется, понимаю. Фиксированная ставка это предсказуемый риск. Плавающая ставка это та, которая может вырасти сама, без всякой вины компании."
    elif d1_pick is not None:
        sasha "Чувствительность к процентным ставкам — а ты мне принёс что-то вообще без единой цифры про кредит. Так дела не делаются."
        player "Я по духу текста ориентировался, не по цифрам."
        sasha "Дух текста зарплату не платит."
    else:
        sasha "Кстати, там был кредит под плавающую, а не фиксированную ставку. Ожидал, что ты это отметишь. А так ты меня не убедил."

    $ d2_pick = nq_pairs.get("d2")
    if d2_pick == 8:
        player "Посмотри на перенос сроков дважды. Застрявшие на таможне ленты — это риск исполнения."
        sasha "Хм... согласен, звучит разумно."
    elif d2_pick is not None:
        sasha "Риск операционного исполнения — а ты мне принёс что-то невразумительное. Это риск чего, эстетического исполнения? Как этот фрагмент из новости связан с риском?"
        player "Ладно, это было слабое звено в моей логике, признаю."
    else:
        sasha "А перенос сроков дважды подряд ты как оценил? Не вижу, чтобы ты это отметил, а я вот бы отметил."

    $ d3_pick = nq_pairs.get("d3")
    if d3_pick == 6:
        player "Касаемо управленческих рисков... Я поставил на нового директора, бывшего СЕО агрохолдинга. Ритейл и агробизнес это ведь разные звери."
        sasha "Спорно, но не безосновательно. Хотя человек может быть отличным управленцем именно потому, что мыслит не как типичный ритейлер — так тоже бывает."
    elif d3_pick == 7:
        player "Касаемо управленческих рисков... Я отметил тренинг по стрессу. Пяткой чую, что стресс из-за плохого менеджмента."
        sasha "Могло быть совпадением. А могло быть симптомом. Проблема ровно в том, что по одному предложению это не различить, но я уважаю мнение твоей пятки."
    elif d3_pick == 2:
        player "Касаемо управленческих рисков... Я выделил курьёз с микрофоном. Если директор не может провести простую церемонию гладко, что говорить об управлении складом на 4.8 миллиарда?"
        sasha "Это, если честно, натяжка. Один неловкий момент на публике это ещё не диагноз менеджменту."
    elif d3_pick is not None:
        sasha "Управленческий риск — а ты мне принёс сюда что-то совсем не про менеджмент. Три кандидата в статье, и ты умудрился найти четвёртый, несуществующий."
        player "Творческий подход."
        sasha "Творческий в смысле «Хочу творю, хочу вытворяю»."
    else:
        sasha "Что, великий трейдер не сумел найти информацию по потенциальным управленческим рискам?"
        player "Что нашёл, то и показал."
        sasha "Ну, показал ты очень неубедительно."

    sasha "Ну хорошо. Так следует ли вообще инвестировать в «Изобилие»? Я так и не понял."
    player "Смотря какой у тебя риск-профиль. И горизонт инвестирования. И как ты относишься к плавающим ставкам, если уж на то пошло."
    sasha "Это не ответ, а список вопросов!!!"
    player "Это и есть ответ. Настоящий аналитик никогда не говорит «да» или «нет» без уточняющих вопросов — иначе он не аналитик, а гадалка."
    sasha "Ты только что назвал нашу работу бессмысленной."
    player "Так да, и за что мне только деньги платят?.."
    sasha "Святые небеса, ты всё это время скрывал, что тебе платят деньги!"

    sasha "Кстати, погляди, какую новость я откопал в местном журнале, пока ты тут разбирался. Вдруг сочтёшь любопытной."

    $ correct_count = 0
    if nq_pairs.get("g1") == 0:
        $ correct_count += 1
        $ accuracy += 1
    if nq_pairs.get("g2") == 3:
        $ correct_count += 1
        $ accuracy += 1
    if nq_pairs.get("d1") == 5:
        $ correct_count += 1
        $ accuracy += 1
    if nq_pairs.get("d2") == 8:
        $ correct_count += 1
        $ accuracy += 1

    $ d3_attempted = d3_pick is not None
    $ d3_valid = d3_pick in (6, 7, 2)
    if d3_valid:
        $ intuition += 2

    if correct_count == 4 and d3_valid:
        $ unlock_achievement("razlozhil_po_polkam")
    elif correct_count == 0 and not d3_attempted:
        $ unlock_achievement("priznalsya_a_ne_pritvorilsya")

    label hidden_quest_point_d_article:
    $ pd_selected = set()
    call screen point_d_article_screen


    if current_task >= 2:
        player "Погоди... это же точка Д. Та самая, с которой я и так работаю для Начальника."
        sasha "Хм. Забавное совпадение — или нет?"
        player "Смена владельца в третьем квартале. А аномалия, которую я расследую... когда она вообще началась?"
        sasha "Не помню точную дату, если честно. Но если совпадёт — это уже не совпадение, а корреляция. А корреляция  это повод спросить «почему»."
        player "«Норд-Капитал». Никогда о них не слышал."
        sasha "Я тоже. Хотя, казалось бы, у меня доступ к базам данных получше, чем у большинства новостных изданий."
        player "Может, это вообще ничего не значит. Обычная сделка, просто совпала по времени. Или даже не совпала, мы же не знаем."
        sasha "Может быть. А может, ты сейчас держишь в руках первую нитку к тому, чтобы понять, почему точка Д ведёт себя так, как ведёт."
        player "Ладно. Запомню. На будущее."
        sasha "Думаю, тут больше нет ничего любопытного."
        $ hero_noticed_point_d = True
        $ unlock_memory("chistiye_dannye_secret")
    else:
        player "И... что в этом такого? Обычная смена владельца, таких новостей десятки."
        sasha "Согласен, звучит как ничего. Может, оно и есть ничего."
        player "Тогда почему ты вообще решил мне это показать?"
        sasha "Потому что оно было написано так, чтобы его никто не заметил. А меня, если ты не забыл, специально обучали замечать то, что не хочет быть замеченным."
        sasha "Просто оцени этот стиль. Кто-то явно не хотел, чтобы сие осили."
        player "Звучит как повод для паранойи, а не для инвестиционного решения."
        sasha "Согласен. Это просто заметка на будущее — вдруг однажды пригодится."
        player "Ладно, отложу в долгий ящик."
        sasha "У меня, между прочим, ящиков не бывает, у меня только память. Отложу это в... где у меня память?"
        player "Конкретно это пойдет во внешнее хранилище. В какую-нибудь БД до востребования."
        sasha "Ммм... ладно, пошли займёмся чем-нибудь другим, пока я осмысляю свою память."

    $ hidden_quest_phase1_done = True
    $ game_minutes_total += renpy.random.randint(20, 115)
    jump desktop_loop
