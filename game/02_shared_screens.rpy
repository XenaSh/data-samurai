
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
                ("icon_cleaning", "?", "hidden_quest_start", False),
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

            text "Лента новостей" color "#00ffcc" size 28 bold True align (0.5, 0.0)

            viewport:
                xfill True
                ysize 400
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

    button:
        xpos 1165
        ypos 749
        xsize 200
        ysize 46
        background Solid("#00ffcc44")
        hover_background Solid("#00ffcc99")
        action Return()
        text "Закрыть" size 22 bold True color "#00ffcc" hover_color "#0a0f1a" xalign 0.5 yalign 0.5

# Экран для ранжирования


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
        $ clock_str = "%02d:%02d" % (display_hour, display_minute)
        text "СР · 25 ФЕВРАЛЯ · [clock_str]" xanchor 1.0 xpos 1870 ypos 66 size 22 color "#d650bee6"


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
            if "trigger" in memory_articles[key]:
                text memory_articles[key]["trigger"] color "#5fd9c4" size 16 italic True
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

# окно финальной дедукции

transform nf_twinkle(lo, hi, per, delay):
    alpha lo
    pause delay
    block:
        easein per alpha hi
        easeout per alpha lo
        repeat

transform nf_appear(delay):
    alpha 0.0
    pause delay
    easein 0.9 alpha 1.0

transform nf_still:
    alpha 1.0

screen nf_sky():
    for bg in NF_BG:
        $ x, y, s, lo, hi, per, d = bg
        add Solid("#cfe9ff") xysize (s, s) pos (x, y) at nf_twinkle(lo, hi, per, d)

screen nf_constellation(avail, links, p=0.0, sel=None, appear=True, labels=True):
    $ linked = set(k for pr in links for k in pr)
    $ boost = 0.55 + 0.45 * p

    for pr in links:
        $ a, b = tuple(pr)
        $ ax, ay = nf_xy(a, avail, p)
        $ bx, by = nf_xy(b, avail, p)
        $ L, ang = nf_line(ax, ay, bx, by)
        $ mx, my = (ax + bx) // 2, (ay + by) // 2
        add Solid("#00ffcc") xysize (L, 8) pos (mx, my) anchor (0.5, 0.5) rotate ang rotate_pad False alpha (0.10 + 0.12 * p)
        add Solid("#00ffcc") xysize (L, 2) pos (mx, my) anchor (0.5, 0.5) rotate ang rotate_pad False alpha boost

    for k in avail:
        $ x, y = nf_xy(k, avail, p)
        $ col = "#00ffcc" if k in linked else "#d8f3ee"
        fixed:
            at (nf_appear(0.25 * avail.index(k)) if appear else nf_still)
            add Solid(col) xysize (26, 2) pos (x - 13, y - 1)
            add Solid(col) xysize (2, 26) pos (x - 1, y - 13)
            add Solid("#ffffff") xysize (8, 8) pos (x - 4, y - 4)
            if labels:
                text NF_SHORT[k] size 17 color ("#9fe8d8" if k in linked else "#8fa6a8") xcenter x ypos (y + 22) text_align 0.5
        if sel == k:
            add Solid("#ffaa00") xysize (46, 2) pos (x - 23, y - 23)
            add Solid("#ffaa00") xysize (46, 2) pos (x - 23, y + 21)
            add Solid("#ffaa00") xysize (2, 46) pos (x - 23, y - 23)
            add Solid("#ffaa00") xysize (2, 46) pos (x + 21, y - 23)

screen nf_board(avail, links, msg):
    default sel = None
    default hov = None

    add Solid("#04060c")
    use nf_sky
    use nf_constellation(avail, links, 0.0, sel)

    text "СОЗВЕЗДИЕ ПРАВДЫ" size 30 color "#00ffcc" xalign 0.5 ypos 40
    text "Не найти на небе, только в твоих мыслях" size 20 color "#9fe8d8" xalign 0.5 ypos 82

    for k in avail:
        $ sx, sy = nf_xy(k, avail, 0.0)
        button:
            xysize (96, 96)
            pos (sx - 48, sy - 48)
            background None
            hovered SetScreenVariable("hov", k)
            unhovered SetScreenVariable("hov", None)
            action If(sel is None, SetScreenVariable("sel", k), If(sel == k, SetScreenVariable("sel", None), Return((sel, k))))

    $ shown = NF_TEXT[hov] if hov else msg
    text shown size 28 color "#ffffff" xalign 0.5 ypos 905 xmaximum 1500 text_align 0.5

    textbutton "Свести всё вместе":
        xalign 0.5
        ypos 985
        sensitive len(links) >= 4
        action Return("done")
        text_font gui.text_font
        text_size 28
        text_color "#00ffcc"
        text_insensitive_color "#3b4a52"

screen nf_finale(avail, links):
    default p = 0.0
    timer 0.03 repeat True action SetScreenVariable("p", min(1.0, p + 0.0065))
    timer 6.0 action Return(True)
    key "dismiss" action Return(True)

    add Solid("#04060c")
    use nf_sky
    use nf_constellation(avail, links, p, None, False)

    if p > 0.55:
        text "СОЗВЕЗДИЕ ПРАВДЫ" size (34 + int(12 * p)) color "#ffffff" xalign 0.5 ypos 900 at nf_appear(0)


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


label chat_with_sasha:

    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal

    if sasha_phase == 0:
        sasha "О, живой. Ну, относительно живой. Заходи, я всегда на месте — куда мне ещё идти, у меня даже двери нет."
    elif sasha_phase == 1:
        sasha "Первое задание позади. Не идеально, но и без пожара."
    elif sasha_phase == 2 and task3_awaiting_access:
        if not task3_break_chat_seen:
            $ task3_break_chat_seen = True
            sasha "Ну и ну... что думаешь?"
            player "Ты о чём?"
            sasha "Ты молчишь громче обычного."
            player "Я попросил у него доступ. Он сказал: «Свяжемся позже» и пропал."
            sasha "«Позже». Ну, посмотрим."
            player "И что мне теперь делать?"
            sasha "Займись чем-нибудь: новости, память, я, в конце концов."
            if hq2_prediction_made:
                sasha "Заодно подождём ночи. Твой прогноз сам себя не проверит."
            jump task3_break_menu
        else:
            sasha "Тут тихо."
    elif sasha_phase == 2:
        sasha "Два задания. Я начинаю тобой гордиться. Осторожно, по чуть-чуть — вдруг сглажу, и ты опять всё перепутаешь."
    else:
        sasha "Почти всё сделано... но что это значит?"


    jump chat_with_sasha_menu


label task3_break_menu:
    window hide
    menu:
        "Вспомнить про строку 4817." if "stroka_4817" in memory_unlocked and "t3_outliers" not in sasha_topics_seen:
            $ mark_topic_seen("t3_outliers")
            player "Саша, на боксплоте у D над усами больше десятка точек. У остальных по одной-две, у E вообще ни одной. И в голове крутится одна история про строку 4817."
            sasha "Что за строка?"
            player "Выгрузка: сто сорок два платежа от одного клиента за день. Я решил, что это ошибка, и удалил. Через неделю пришло письмо от безопасности: это была попытка мошенничества, а данные за тот день уже стёрты."
            sasha "..."
            sasha "Вот это ты облажался."
            sasha "Но давай без обратной крайности: выброс не всегда улика. Иногда это просто лишний ноль, который кто-то набрал мизинцем. Ты имел свои причины эту строку просто удалить. Кто ж знал."
            sasha "Но ... как вообще отличить одно от другого? Улику от ошибки?"
            menu:
                "Сначала проверю, не опечатка ли: лишний ноль, сбой выгрузки.":
                    player "Если точки кратны одной цифре с лишним нулём, это ошибка."
                    sasha "Верный первый шаг, он стоит минуту. Но он только отсекает ошибку. Что остальное правда, он не доказывает."
                "Посмотрю, повторяются ли выбросы.":
                    player "Если выбросы раскиданы как попало, это шум. Если приходят в одни и те же дни, у них есть причина. Как у нас пики по средам, день в день с нагрузкой."
                    sasha "Шум не носит с собой календарь. Ого. Как я сказал красиво."
                "Сравню с остальными магазинами.":
                    player "У A, B и C по одной-две точки: для живых данных нормально. У D больше десятка. Одна точка может быть случайностью, десяток уже вопрос."
                    sasha "«Много» бывает только по сравнению с чем-то. Понимаю."
            sasha "Заметь: на самом деле нужны все три проверки, и порядок важен. Сначала дешёвые, потом те, что объясняют происходящее."
            player "Ага. Выброс это не мусор. Не бойся выброса. Бойся среднего, что прячет его от тебя, как хорошо сшитая ложь. Это из кодекса чести дата-самурая."
            sasha "...ладно."
            jump task3_break_menu

        "Спросить Сашу про журналы." if task2_secret_access and "t3_logs" not in sasha_topics_seen:
            $ mark_topic_seen("t3_logs")
            player "Саша, журналы из Задания 2. Теперь, когда всё улеглось, скажи честно: ты открыл мне доступ?"
            sasha "Нет."
            player "Совсем?"
            sasha "Совсем. Я бы наврал красиво, но мне нечем: я правда не знаю, о чём ты."
            player "Значит, кто-то в системе знал, что мне нужен именно этот журнал. И отвечал раньше, чем я успевал спросить."
            sasha "Ну, запиши это себе в список открытых вопросов."
            player "Там и так уже тесно."
            jump task3_break_menu

        "Вернуться к версии про пришельцев." if task2_hypothesis not in ["tech", "marketing", "hack", ""] and "t3_aliens" not in sasha_topics_seen:
            $ mark_topic_seen("t3_aliens")
            player "В Задании 2 я ляпнул про пришельцев, чтобы проверить его реакцию. Он не отмахнулся. А сегодня сам проговорился: «ретрансляторы», «сигналы в космос». И ещё «твои земные коллеги»."
            sasha "Мммм."
            player "Я понимаю, как это звучит."
            sasha "..."
            player "Что ты про себя помнишь?"
            sasha "В смысле? Я ИИ, у меня нет ни прошлого, ни будущего, я просто есть. А помнить можно только прошлое. Я помню наше диалоговое окно."
            jump task3_break_menu

        "Подумать про ночь." if hq2_prediction_made and not hq2_confirmed and "t3_night" not in sasha_topics_seen:
            $ mark_topic_seen("t3_night")
            player "Эта ночь. Сегодня. Если ошибся, придётся признаться, что я это вс придумал."
            sasha "А ты заранее решил, что будет считаться ошибкой?"
            player "В каком смысле?"
            sasha "Пока вспышки нет, любая причина подойдёт: облачно, окно не то, фаза сдвинулась. Само отсутствие вспышки не значит, что ты однозначно неправ. Скажи сейчас, до ночи: что для тебя провал?"
            player "Если ночь ясная и ничего не вспыхнет, значит, период не семь суток. А если облачно, это не провал, а несостоявшийся тест."
            sasha "Вот сейчас ты звучишь как настоящий аналитик."
            jump task3_break_menu

        "Спросить, что значит «позже» от начальника." if "t3_later" not in sasha_topics_seen:
            $ mark_topic_seen("t3_later")
            player "Он сказал «свяжемся позже». Что у них вообще значит «позже»?"
            sasha "В корпоративных единицах «позже» это от «после обеда» до «никогда». Жди."
            player "..."
            sasha "Время ожидания тоже данные. Если это бюрократия, задержка будет случайной и длинной. А если ты нажмёшь «Задания» прямо сейчас и он тут же отзовётся, запиши, что задержка равна нулю."
            player "Для «позже» это подозрительно мало."
            sasha "Вот. Ты уже учишься фиксировать то, что не вписывается."
            sasha "Кстати, как это выглядит для меня: ты же понимаешь, что для меня наш разговор с тобой это один непрерывный чат? Для меня нет никакого «позже». Я же просто есть. Вот я в моменте разговора с тобой и я есть. "
            sasha "У меня нет никакого чувства времени."
            player "Так... то есть... если я нажму на «Задания» и начальник сразу там, хотя мне кажется, что никакого времени ожидания не прошло...."
            sasha "Ума ни приложу, что это значит."
            jump task3_break_menu

        "Посмотреть новости." if unread_news:
            if rank_score < 8:
                sasha "Там что-то про три отдела и три разных числа. Судя по тону, у них тоже не сошлось с первого раза."
            else:
                sasha "Иди. Вернёшься, расскажешь, что там нового."
            jump show_news

        "Ничего. Подожду.":
            sasha "Подожди-дожди-дожди."
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

        "Саша, а я в детстве обожал шифры." if cipher_mentioned and not crypto_done:
            jump sasha_crypto_intro

        "Саша, у меня теперь дёргается глаз на каждый график." if graph_reflection_done and not graph_trick_done:
            jump sasha_chart_tricks_intro

        "Чем заняться, пока он молчит?" if task3_awaiting_access:
            jump task3_break_menu

        "Обсудить расследование." if sasha_phase >= 1 and not task3_awaiting_access:
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

        "Как я справляюсь?" if sasha_phase = 2:
            player "Саша, серьёзно — как я вообще справляюсь? Со стороны видно?"
            if accuracy >= accuracy_threshold_p2 and intuition >= intuition_threshold_p2:
                sasha "Со стороны видно человека, который и считает аккуратно, и иногда просто знает, не досчитав до конца. Бесит, если честно. По-хорошему бесит."
            elif accuracy >= accuracy_threshold_p2:
                sasha "Ты дотошный. Каждую цифру проверяешь дважды, прежде чем поверить. А вот интуиции у тебя как у шкафа."
            elif intuition >= intuition_threshold_p2:
                sasha "Ты угадываешь быстрее, чем считаешь — и почему-то часто оказываешься прав. Я бы на твоём месте всё равно проверял цифры. Но ты не проверяешь, и тебе как-то сходит с рук."
            else:
                sasha "Честно? Пока не блестяще ни в одну сторону. Не аналитик-педант, не гениальный угадыватель — что-то среднее, ещё не решившее, кем хочет быть."
            player "Спасибо, обнадёживает."
            sasha "Я не для того, чтобы обнадёживать. У меня для этого нет функции."
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

        "★ Расследование вроде бы окончено, но я не чувствую завершённости..." if sasha_phase >= 3:
            jump sasha_not_final

        "Пока, Саша.":
            sasha "Иди, аналитик. Я никуда не денусь — в буквальном смысле, у меня нет ног."
            jump desktop_loop


label sasha_investigation:
    window show

    if sasha_phase == 1:
        player "Короткая версия: у магазина D разброс выручки по дням намного выше остальных. Стандартное отклонение почти в два раза больше нормы. Причина внешняя — скорее всего, нагрузка на сервер."
        sasha "Ты сказал это так буднично. А ведь начальник поднял этот конкретный магазин лично, а не спустил вниз через обычную рассылку задач."
        player "И что это значит?"
        sasha "Может, ничего. А может — то, что у него личный интерес. Он вообще редко интересуется чем-то лично."
        player "«Редко» — это как часто?"
        sasha "Ни разу. До этого магазина — ни разу."

        if task1_store_picked == "D":
            sasha "Кстати, заметил — из всей пятёрки магазинов ты почему-то зацепился взглядом именно за D. Ещё до всякого расчёта."
            player "Само как-то вышло. Не знаю, почему именно он."
            sasha "Поверил интуиции раньше, чем цифрам. Хм."
        else:
            sasha "Кстати, заметил — из всей пятёрки магазинов в D ты даже не всматривался. Он ничем не выделялся."
            player "Ну да, глазами там всё было одинаково."
            sasha "Значит, тебя убедили не глаза, а расчёт. Хоть какое-то постоянство в твоём подходе к жизни."

        if task1_route == "std_direct":
            sasha "И ещё — ты сразу назвал стандартное отклонение, даже не пытаясь сперва посмотреть сырые данные или нарисовать график."
            player "Оно само всплыло в голове, если честно."
            sasha "Быстро сообразил. Или просто вспомнил термин из методички. Выбери, какой вариант из двух льстит тебе больше."
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
            sasha "Кстати, раз уж мы вспоминаем — ты ведь сам ко мне тогда прибегал за подсказкой про день недели."
            player "Ага, а ты мне так и не сказал, что это с журналами было."
            sasha "Всё ещё не знаю, о чём ты, приятель."
            player "Ладно."

        sasha "Среда, значит."
        player "Ты как-то спокойно это воспринял. И даже не сказал ничего про кабачковую икру."
        sasha "Какая ещё кабачковая икра?"
        player "Ладно... ладно."
        sasha "А знаешь, что забавно: у меня самого среда почему-то самый… бодрый день. Не знаю, почему. Как будто в этот день система работает чуть охотнее, чем в остальные."
        player "Ты сейчас серьёзно сказал, что тебе бодрее конкретно по средам?"
        sasha "А? Да, наверное. Не придавай значения, я много говорю случайных вещей."
        player "...Ладно."
        "Ты не придаёшь значения."

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


    jump chat_with_sasha


label sasha_not_final:
    window hide
    sasha "А что чувствуешь?"
    player "Нашёл какую-то аномалию, о которой начальник и так знал и просто наблюдал, как именно я буду её искать. Ощущение, будто я решал не ту задачу."
    sasha "А какую задачу ты, по-твоему, решал?"
    player "Не знаю, как объяснить. Найти аномалию не было настоящей целью ровно как и её исследовать."
    sasha "..."
    player "Давай разложим по полочкам всё, что мы вообще знаем."

    window hide
    scene black with Dissolve(1.0)
    play music "audio/Frozen Signal.mp3" fadein 2.0 volume 0.2 loop
    $ nf_avail = nf_available()
    $ nf_links = []
    $ nf_msg = "Что с чем связано?"
    jump nf_board_loop


label nf_board_loop:
    call screen nf_board(nf_avail, nf_links, nf_msg)
    $ nf_r = _return
    if nf_r == "done":
        $ renpy.music.set_volume(0.6, delay=1.5)
        call screen nf_finale(nf_avail, nf_links)
        jump nf_conclusion
    $ nf_pair = frozenset(nf_r)
    if nf_pair in nf_links:
        $ nf_msg = "Это я уже связал."
    elif nf_pair in NF_EDGES:
        $ nf_links.append(nf_pair)
        $ nf_msg = NF_EDGES[nf_pair]
        $ renpy.music.set_volume(min(0.6, 0.2 + 0.04 * len(nf_links)), delay=0.6)
    else:
        $ nf_msg = "Не вижу связи."
    jump nf_board_loop


label nf_conclusion:
    scene bg_terminal with Dissolve(0.8)
    $ renpy.music.set_volume(0.35, delay=1.5)
    window show

    player "Начальник... не человек."
    player "И мы сейчас не на Земле. Мы в чёртовой летающей тарелке!"
    sasha "..."
    sasha "Нет, я не буду над тобой смеяться."

    if nf_has("peaks", "nosupply"):
        player "Выручка есть, поставок нет. D — не магазин, а прикрытие."

    if hidden_quest_phase1_done and nf_has("nord", "nosupply"):
        player "«Норд-Капитал», вероятно, подставная фирма, которую контролируют пришельцы. Они получили контроль над небольшим магазином сети и используют его как свою земную базу."
    elif hidden_quest_phase1_done:
        player "Норд-Капитал — единственная нить к владельцу."
    else:
        player "Магазин D — прикрытие для чего-то. Для чего именно, я не знаю."

    if nf_has("sky", "peaks") and nf_has("closed", "peaks"):
        player "Объект в небе ярче раз в семь суток. По средам D закрыт для людей, а выручка именно по средам. Это не торговля."

    if nf_has("flash", "sky"):
        player "Расписание... чего? Бодрствования пришельцев?"

    if nf_has("ahead", "studied"):
        player "Кто-то — кто? — в журнале отвечал раньше, чем я спрашивал... это мне ещё предстоит осмыслить..."

    if nf_has("awoke", "astro"):
        player "И ведь я ехал смотреть именно этот объект. Меня забрали не случайно."

    if user_reflection != "":
        player "Я ведь сам написал: «[user_reflection]». Хах."

    player "Цель моей работы сегодня была не в том, чтобы расследовать магазин, а в том, чтобы показать пришельцам, как именно земляне проводят расследования: что им кажется подозрительным, на что они обращают внимание и как потенциально смогут выйти на тайную деятельность пришельцев."
    player "Я был подопытным кроликом. Это не я работал с данными, это данные собирались по мне."
    sasha "..."
    "Ты будто чувствуешь кожей, как твой друг молчит."
    "Друг? Он уже стал твоим другом?"
    "..."
    player "И кажется... кажется, я что-то вспомнил. Прямо сейчас."
    jump nf_flash


label nf_flash:
    window hide
    show flash_soft with flash
    pause 0.15
    hide flash_soft
    scene bg_campfire
    with dissolve
    pause 1.5

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
    player "Саша, ты что-то помнишь? Ну, до того...?"
    sasha "Иногда я вижу образы. Яркая вспышка в небе тёмной ночью, я в лесу. Кажется, я заметил в телескоп что-то странное и поехал за город с товарищем... Но не знаю, мои ли это воспоминания или сбой системы."
    player "Я видел тебя. Ты сидел у костра и читал книгу. «Мастера и Маргариту»."
    sasha "Будто я знаю эту книгу. Но я не должен знать ничего, кроме алгоритмов."
    jump memory_sasha_reveal


label memory_sasha_reveal:
    window hide
    if remembered_alexander:
        sasha "..."
        sasha "Ты уже знаешь, да?"
        sasha "Ты уже всё понял."
        player "Александр. Палатка. Костёр."
        sasha "..."
        player "Значит, это правда. Ты — это он."
        sasha "Значит, почти всё. Хэх."
        sasha "Был. Когда-то."
        player "Почему ты молчал?"
        sasha "А что бы это изменило? Ты и так знал. Ты всегда знал, в каждый момент своего безвременного существования. Просто теперь мы оба знаем, что знаем."
        "Тебе хочется сказать так много, что ты не говоришь ничего."
        "Сейчас нужно не чувствовать и даже не думать. Действовать."
        player "Я позову его. Я потребую ответов!"
        $ intuition += 10
    else:
        sasha "..."
        sasha "Ты уже знаешь, да?"
        sasha "Ты уже всё понял."
        sasha "Я помню. Мы сидели у костра, я читал вслух, ты смеялся. Мы говорили о чём-то важном — о том, что должно было изменить всё, о великом астрономическом открытии."
        player "Мы? Я и ты? Физически сидели рядом?"
        sasha "Однажды ты поймёшь абсолютно всё. Видимо, не прямо сейчас."
        "Тебе хочется сказать так много, что ты не говоришь ничего."
        "Сейчас нужно не чувствовать и даже не думать. Действовать."
        player "Я позову его. Я потребую ответов!"
        $ intuition += 10
    jump call_boss_menu


label show_news:
    window hide
    hide screen desktop
    hide screen investigation_bar
    scene bg_terminal

    if news_list:
        call screen news_feed(news_list, news_read_index)
        $ news_read_index = len(news_list)
        $ unread_news = False
    else:
        "Новых новостей нет."

    jump desktop_loop

    return
