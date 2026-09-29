from maxapi import Router, F
from maxapi.context import MemoryContext
from maxapi.enums import ParseMode
from maxapi.filters import StateFilter
from maxapi.types import MessageCreated, InputMedia

from functions.base_keyboard_maker import base_keyboard_maker
from functions.ch1_bad_end import check_bad_end
from functions.edit_resources import edit_resources
from functions.remove_keyboards import remove_keyboard
from functions.resources_print import print_resources
from handlers.menu import main_menu
from keyboards.menu_kb import kb_menu6_dict
from states.chapter1_states import Chapter1States
from states.menu_states import MenuStates

chapter1 = Router()

kb_chapter1_0_dict = {"button1" : "Выйти на связь"}
@chapter1.message_created(F.message.body.text.in_([kb_menu6_dict["button1_1"],kb_menu6_dict["button1_1"]+" ✅"]), MenuStates.menu)
async def chapter1_0(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s0)

    await context.update_data(finance=100)
    await context.update_data(food=100)
    await context.update_data(energy=100)
    await context.update_data(odyssey = 0)
    await context.update_data(trees=0)
    await context.update_data(radar=0)

    media = InputMedia("media/chapter1/ch1.mp4")

    data = await context.get_data()
    finance = data["finance"]
    energy = data["energy"]
    food = data["food"]

    last_message = await event.message.answer(
        text=(await print_resources(context)+"<b>☝ Текущий баланс ресурсов отображается прямо здесь</b>\n\n"
"Сегодня ваш <b>первый рабочий день</b>. Сейчас вы познакомишься с руководителями отделов станции. Предупреждаю сразу: у каждого из них «самый срочный» запрос, и все будут требовать ресурсы, а последствия вы увидите потом!\n\n"
"Ваша главная задача — грамотно распределять бюджет и припасы, чтобы станция работала как часы.\n\n"
"<blockquote>💡 <b>Совет :</b> Не отдавайте всё одному отделу, иначе другие останутся без поддержки!</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_0_dict),

        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_1_dict = {"button1" : "🤝 Будем знакомы"}
@chapter1.message_created(F.message.body.text == kb_chapter1_0_dict["button1"], Chapter1States.s0)
async def chapter1_1(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s1)

    media = InputMedia("media/chapter1/ch2.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context)+
            "🫡 <b>Здравия желаю, Центр.</b>\n\nЯ — <b>Владимир</b>, начальник Службы Безопасности. Будем знакомы.\n\nВы там, на Земле, должны чётко понимать одну вещь: учёные и техники, конечно, важны, но именно мы гарантируем, что эта станция функционирует как положено, а не утонет в хаосе.\n\n<blockquote>🛡️ <b>СБ на «ПРОЦЕСС-1»</b> — это порядок, железная дисциплина и холодный рассудок. Мы — щит этого комплекса.</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_1_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_2_dict = {
    "button1" : "Перекупить у стороннего подрядчика",
    "button2" : "Взять сертифицированный гидролокатор",
    "button3": "Выделить бюджет на секретный радар"}
@chapter1.message_created(F.message.body.text == kb_chapter1_1_dict["button1"], Chapter1States.s1)
async def chapter1_2(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s2)

    media = InputMedia("media/chapter1/ch3.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context)+
            "И ещё один вопрос, Оператор, чисто по моей части.\n\n"
            "Наш основной гидролокатор на днях сгорел — учёные сказали, что был какой-то аномальный всплеск ЭМИ. "
            "Без него мы в этих тёмных водах слепы, как кроты.\n\nНадо срочно брать новый у поставщиков с поверхности. "
            "Что выберем по бюджету?"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_2_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Вариант 1 — сторонний подрядчик
kb_chapter1_3_dict = {"button1": "Связаться с техническим отделом"}

@chapter1.message_created(
    F.message.body.text == kb_chapter1_2_dict["button1"],
    Chapter1States.s2
)
async def chapter1_3_1(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s3)
    await edit_resources(context, finance_delta=-1)
    await context.update_data(radar = 1)
    media = InputMedia("media/chapter1/ch2.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context)+
            "🫡 <b>Решение принято, Оператор.</b>\n\n"

            "Перекупаем гидролокатор у стороннего подрядчика. "
            "Это позволит нам сэкономить бюджет, но, честно говоря, "
            "я не в восторге от такого решения.\n\n"

            "Мы не знаем, в каком состоянии оборудование "
            "и насколько оно надёжно. Однако выбора у нас "
            "особо нет. Главное — как можно скорее вернуть "
            "станции возможность обнаруживать объекты "
            "вокруг нас.\n\n"

            "<blockquote>"
            "📦 <b>ОТЧЁТ О ПОСТАВКЕ</b>\n\n"
            "Заявка ушла поставщикам, груз поступил на станцию. "
            "Только сама железка себя не вкрутит и к сети "
            "не подключится.\n\n"
            "Свяжись с Николаем — пусть его техники забирают "
            "коробку и устанавливают эту штуку."
            "</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_3_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Вариант 2 — сертифицированный гидролокатор
@chapter1.message_created(
    F.message.body.text == kb_chapter1_2_dict["button2"],
    Chapter1States.s2
)
async def chapter1_3_2(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s3)
    await edit_resources(context, finance_delta=-2)
    await context.update_data(radar=2)
    media = InputMedia("media/chapter1/ch2.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context)+
            "🫡 <b>Вот это я понимаю, Оператор!</b>\n\n"

            "Сертифицированное оборудование — именно то, "
            "что нам нужно. Оно прошло все необходимые "
            "проверки, и мы можем рассчитывать на его "
            "стабильную работу.\n\n"

            "Конечно, придётся потратить больше средств, "
            "но безопасность станции для меня превыше всего. "
            "Теперь осталось дождаться доставки и передать "
            "оборудование техническому отделу.\n\n"

            "<blockquote>"
            "📦 <b>ОТЧЁТ О ПОСТАВКЕ</b>\n\n"
            "Заявка ушла поставщикам, груз поступил на станцию. "
            "Только сама железка себя не вкрутит и к сети "
            "не подключится.\n\n"
            "Свяжись с Николаем — пусть его техники забирают "
            "коробку и устанавливают эту штуку."
            "</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_3_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Вариант 3 — секретный радар
@chapter1.message_created(F.message.body.text == kb_chapter1_2_dict["button3"],Chapter1States.s2)
async def chapter1_3_3(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s3)
    await edit_resources(context,finance_delta=-3)
    await context.update_data(radar=3)
    media = InputMedia("media/chapter1/ch2.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context)+
            "🤨 <b>Секретный радар? Неожиданное решение, Оператор.</b>\n\n"

            "Если поставщик действительно гарантирует его "
            "возможности, это может стать серьёзным "
            "преимуществом для нашей службы.\n\n"

            "Правда, такая покупка потребует немалых средств.\n\n "
            
            "<blockquote>"
            "📦 <b>ОТЧЁТ О ПОСТАВКЕ</b>\n\n"
            "Заявка ушла поставщикам, груз поступил на станцию. "
            "Только сама железка себя не вкрутит и к сети "
            "не подключится.\n\n"
            "Свяжись с Николаем — пусть его техники забирают "
            "коробку и устанавливают эту штуку."
            "</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_3_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_4_dict = {"button1": "🤝 Будем знакомы"}
@chapter1.message_created(F.message.body.text.in_(kb_chapter1_3_dict.values()),Chapter1States.s3)
async def chapter1_4(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s4)

    media = InputMedia("media/chapter1/ch4.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "Здорово, Оператор. Я <b>Николай</b>, старший техник.\n\n"
"Да, я получил запрос на установку радара. Пока ученые пробирки перебирают, а охрана шлюзы гоняет, моя бригада держит на плаву всю станцию — от реактора до пищевых синтезаторов.\n\n"
"<blockquote>Запомни: свет горит, воздух идет и еда на столе есть только потому, что мы пашем. Встанет реактор или сдохнут насосы агропоники — всем нам конец.</blockquote>"),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_4_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_5_dict = {"button1": "Одобрить капитальный ремонт гидропоники",
                      "button2": "Забрать ресурсы у лабораторий",
                      "button3": "Временно урезать рационы экипажа",
                      "button4": "Пусть едят резервы, на ремонт денег нет"}
@chapter1.message_created(F.message.body.text.in_(kb_chapter1_4_dict.values()),Chapter1States.s4)
async def chapter1_5(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s5)

    media = InputMedia("media/chapter1/ch5.jpg")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "Слушай, раз уж мы на связи: гидропоника трещит по швам, датчики валятся, экипаж вторую неделю на сухих пайках, а оранжерея дохнет.\n\n"
"<blockquote>⚠️ <b>Если срочно не перераспределим ресурсы или не перестроим график обслуживания, мы останемся без зелени.</b></blockquote>\n\n"
"Что делаем?"),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_5_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

kb_chapter1_6_dict = {"button1": "Хорошо"}


# Вариант 1 — Капитальный ремонт гидропоники
@chapter1.message_created(
    F.message.body.text == kb_chapter1_5_dict["button1"],
    Chapter1States.s5
)
async def chapter1_6_1(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s6)
    await edit_resources(context, finance_delta=-3)
    await context.update_data(food_update=1)
    media = InputMedia("media/chapter1/ch4.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🛠️ <b>Отлично, шеф! Деньги решают всё.</b>\n\n"
            "Мои бригады уже тащат новые узлы в отсек. "
            "Через пару часов всё пересоберём — <i>жить будем!</i>"),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_6_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Вариант 2 — Забрать ресурсы у лабораторий
@chapter1.message_created(
    F.message.body.text == kb_chapter1_5_dict["button2"],
    Chapter1States.s5
)
async def chapter1_6_2(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s6)
    await edit_resources(context, finance_delta=-1, energy_delta=-1)
    await context.update_data(food_update=1)
    media = InputMedia("media/chapter1/ch4.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "⚡ <b>Слушаюсь! Рубильники перекинули.</b>\n\n"
            "У учёных свет погас — слышу, они уже вовсю орут в коридорах! "
            "Зато гидропоника загудела на полную — <i>зелень спасена!</i> 🌿"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_6_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Вариант 3 — Урезать рационы экипажа
@chapter1.message_created(
    F.message.body.text == kb_chapter1_5_dict["button3"],
    Chapter1States.s5
)
async def chapter1_6_3(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s6)
    await edit_resources(context, energy_delta=-1, food_delta=-2)
    await context.update_data(food_update=0)
    media = InputMedia("media/chapter1/ch6.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "⚠️ <b>Принято, Оператор.</b>\n\n"
            "<blockquote>🤐 <b>ЭФФЕКТИВНОСТЬ СМЕНЫ СНИЖЕНА</b></blockquote>\n\n"
            "Парни на смене, конечно, будут недовольны, работать будут хуже...\n "
            "Но раз надо для дела — перетерпим. Главное, чтоб система не легла."
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_6_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Вариант 4 — На ремонт денег нет
@chapter1.message_created(
    F.message.body.text == kb_chapter1_5_dict["button4"],
    Chapter1States.s5
)
async def chapter1_6_4(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s6)
    await edit_resources(context, food_delta=-3)
    await context.update_data(food_update=0)
    media = InputMedia("media/chapter1/ch6.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🥫 <b>Серьёзно? Ну, как знаешь...</b>\n\n"
            "Консервы-то мы доедим, но если гидропоника окончательно встанет через пару дней — "
            "<i>сам понимаешь, мы предупреждали.</i> ⚠️"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_6_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# Переход к Блоку 8 — Утренняя сводка
kb_chapter1_7_dict = {"button1": "Открыть канал связи с доктором Юрием"}

@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_6_dict.values()),
    Chapter1States.s6
)
async def chapter1_8(event: MessageCreated, context: MemoryContext):

    await context.set_state(Chapter1States.s8)

    media = InputMedia("media/chapter1/ch8.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "📊 <b>Оператор, формирую утреннюю сводку.</b>\n\n"
            "Первичные отчёты от СБ и технической службы приняты, данные обновлены на вашем терминале ☝\n\n"
            "Следующий по очереди — <b>научный сектор</b>. Доктор Юрий уже несколько минут пытается пробиться на прямую линию и, судя по индикаторам, начинает терять терпение.\n\n"
            "<blockquote>🔬 <b>НАУЧНЫЙ БЛОК:</b> Запрошен приоритетный сеанс связи.</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_7_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

# --- БЛОК 9: Знакомство с доктором Юрием ---
kb_chapter1_8_dict = {"button1": "🤝 Будем знакомы"}

@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_7_dict.values()),
    Chapter1States.s8
)
async def chapter1_9(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s9)

    media = InputMedia("media/chapter1/ch9.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🧪 <b>Добрый день, Центр.</b>\n\n"
            "Я — <b>Юрий</b>, научный руководитель. Приятно, что вы на связи.\n\n"
            "Давайте сразу проясним: на этой станции сила — не в мускулах и не в броне, а в <b>понимании</b>. Мы, учёные, собираем картину из тысяч мелких деталей: температуры, давления, состава воды, вибраций корпуса.\n\n"
            "Именно эти данные решают, будем ли мы вечно бороться с симптомами или сразу разберёмся с <i>причиной</i>.\n\n"
            "<blockquote>🔬 <b>СТАТУС НАУЧНОГО БЛОКА:</b>\n"
            "Сейчас мы держим под контролем несколько нестабильных показателей. Если хотите знать, что реально происходит под толщей воды — спрашивайте меня. Мы держим всё под наблюдением.</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_8_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- БЛОК 10: Запрос ресурсов от научного отдела ---
kb_chapter1_9_dict = {
    "button1": "Дать добро на утилизацию «Одиссея»",
    "button2": "Проанализировать график экспедиций",
    "button3": "Отказаться от одного «Мотылька»",
}

@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_8_dict.values()),
    Chapter1States.s9
)
async def chapter1_10(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s10)

    media = InputMedia("media/chapter1/ch10.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "<b>Прекрасные новости:</b> корпорация скоро доставит нам три новеньких исследовательских батискафа класса «Мотылек»!\n\n"
            "<b>Проблема в том</b>, что рабочих доков у нас всего три, и один из них намертво занят старичком «Одиссеем». \n\n"
            "Можно его пустить на запчасти. Он всё равно стоит без дела, а у нас уже есть идеи куда пустить с него детали."
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_9_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

kb_chapter1_11_dict = {"button1": "Именно так. Действуйте"}
# --- УЗЕЛ 11: Утилизация старого батискафа (Вариант 1) ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_9_dict["button1"],
    Chapter1States.s10
)
async def chapter1_11(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s11)
    await edit_resources(context, finance_delta=1, energy_delta=-1, food_delta=-1)

    media = InputMedia("media/chapter1/ch11.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🧪 <b>Разумное решение, Оператор</b>, механики в ангаре уже расчехлили "
            "плазменные резаки. А куда всё это пристроить обязательно найдётся."
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_11_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 12: Анализ графика экспедиций (Вариант 2) ---
kb_chapter1_12_dict = {
    "button1": "Выбрать гипотезу 1",
    "button2": "Выбрать гипотезу 2",
    "button3": "Выбрать гипотезу 3"
}

@chapter1.message_created(
    F.message.body.text == kb_chapter1_9_dict["button2"],
    Chapter1States.s10
)
async def chapter1_12(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s12)
    await edit_resources(context, energy_delta=-1)

    media = InputMedia("media/chapter1/ch12.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "📊 <b>Аналитика? Ох уж эта бюрократия...</b>\n\n"
    "Хорошо, уже выгружаем диаграмму Ганта. Надеюсь, вы найдете там "
    "магический четвёртый док, пока новые аппараты ещё могут ждать снаружи.\n\n"
    "<blockquote><b>📌 Гипотеза 1</b>\n"
    "Все три дока постоянно задействованы под текущие задачи. Места нет — «Одиссей» придётся разобрать на запчасти.</blockquote>\n\n"
    "<blockquote><b>📌 Гипотеза 2</b>\n"
    "График ротации сменный: хотя бы один батискаф всегда в море. Значит, один док всегда свободен — «Одиссей» можно оставить!</blockquote>\n\n"
    "<blockquote><b>📌 Гипотеза 3</b>\n"
    "Из-за плотности графика нам катастрофически не хватает мест. Нужно срочно строить 4-й док.</blockquote>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_12_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

kb_chapter1_13_dict = {"button1": "Проверенное старое надежнее нового"}
# --- УЗЕЛ 13: Отказ от «Мотылька» (Вариант 3) ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_9_dict["button3"],
    Chapter1States.s10
)
async def chapter1_13(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s13)
    await edit_resources(context, finance_delta=-1, energy_delta=-1)
    await context.update_data(odyssey=1)

    media = InputMedia("media/chapter1/ch13.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🧪 <b>Что?! Отправить новейшее оборудование обратно?!</b>\n\n"
            "Оператор, вы понимаете, что «Одиссей» — это ржавое корыто, а «Мотыльки» — это наше будущее? "
            "Мой отдел будет крайне разочарован таким подходом!"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_13_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 14: Ответвления после анализа диаграммы Ганта ---

# 14.1 Разбор «Одиссея» по результатам анализа
@chapter1.message_created(
    F.message.body.text == kb_chapter1_12_dict["button1"],
    Chapter1States.s12
)
async def chapter1_14_1(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s14)
    await edit_resources(context, finance_delta=1, energy_delta=-1, food_delta=-1)

    media = InputMedia("media/chapter1/ch9.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🧪 <b>Эх... Жаль старушку, столько лет верой и правдой.</b>\n\n"
            "Но против цифр не попрёшь. Ладно, иду подписывать бумаги на утилизацию. Пустим её на ремкомплекты..."
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_11_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# 14.2 Сменный график ротации
@chapter1.message_created(
    F.message.body.text == kb_chapter1_12_dict["button2"],
    Chapter1States.s12
)
async def chapter1_14_2(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s14g)
    await context.update_data(odyssey=1)

    media = InputMedia("media/chapter1/ch11.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🧪 <b>А ведь вы правы! Отличный глаз.</b>\n\n"
            "Из-за сменного графика один из батискафов всегда находится в рейде, а значит, в ангарах всегда "
            "пустует как минимум один док. «Одиссей» прекрасно впишется в эту ротацию без постройки новых секций. Оставляем!"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_11_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# 14.3 Строительство 4-го дока
@chapter1.message_created(
    F.message.body.text == kb_chapter1_12_dict["button3"],
    Chapter1States.s12
)
async def chapter1_14_3(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s14)
    await edit_resources(context, finance_delta=-3)
    await context.update_data(odyssey=1)
    media = InputMedia("media/chapter1/ch9.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "🧪 <b>Четвёртый док нам бы нам не помешал, наконец-то развернёмся по-человечески!</b>\n\n"
            "Правда, бухгалтерия от такой сметы в обморок упадёт, и бюджет станции затрещит по швам... но чёрт с ними, подаём заявку!"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_11_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

kb_chapter1_15_dict = {"button1": "Продолжить"}

# --- УЗЕЛ 15: Итоги аналитики (Зеленая ветка - Успешное решение) ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_11_dict["button1"],
    Chapter1States.s14g
)
async def chapter1_15_success(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s15)

    media = InputMedia("media/chapter1/ch15.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "✅ <b>Отличная работа, оператор. Вы продемонстрировали грамотный подход к анализу данных.</b>\n\n"
            "<b>Диаграмма Ганта</b> — это один из главных инструментов управления ресурсами. Её суть проста: по оси Y указываются ресурсы или задачи (в нашем случае — батискафы и доки), а по оси X — шкала времени. Длина каждого отрезка показывает продолжительность операции, а их взаиморасположение — накладки и простои.\n\n"
            "Главная ценность диаграммы в том, что она позволяет увидеть не просто «загружена ли станция», а когда именно и насколько эффективно используются мощности. Вы увидели интервалы между рейсами и поняли: благодаря сменному графику один док всегда свободен, что позволяет нам сохранить «Одиссей» без лишних затрат.\n\n"
            "<blockquote>🌊 <b>ОБНОВЛЕНИЕ СТАТУСА:</b>\n"
            "И ваше решение принято как раз вовремя. Датчики внешнего периметра фиксируют гидроакустический сигнал: тяжёлые грузовые подводные лодки подошли к станции и запрашивают открытие шлюзов. Они уже заплывают в ангар для разгрузки.</blockquote>\n\n"
            "<i>Перевожу изображение на главный экран...</i>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_15_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 15: Итоги аналитики (Серая ветка - Ошибка/Поспешное решение) ---
@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_11_dict["button1"], kb_chapter1_13_dict["button1"]]),
    StateFilter(Chapter1States.s11,Chapter1States.s13,Chapter1States.s14)
)
async def chapter1_15_error(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s15)

    media = InputMedia("media/chapter1/ch15.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "⚠️ <b>Фиксирую ошибку в аналитической секции.</b>\n\n🌊 На подводной станции принимать решения «сгоряча» и рубить с плеча — прямая угроза безопасности и нашему бюджету.\n\n⏳ В вашем решении упущен важнейший фактор — время. Когда кажется, что места или ресурсов критически не хватает, вас спасет <b>диаграмма Ганта</b>. Запомните этот инструмент, к нему придется обращаться постоянно.\n\n📊 Это база хронологического планирования. По вертикали здесь отложены ресурсы, а по горизонтали — время. Чтобы увидеть реальную картину, нужно делать «вертикальные срезы» по шкале времени в разные часы. Если в любой выбранный момент суммарно занято меньше слотов, чем есть в ангаре — значит, ресурс не перегружен, а аппараты просто работают посменно. 💡 Не нужно строить новые доки или уничтожать технику, когда достаточно грамотно распределить временные окна!\n\n<blockquote>🔔 <b>ОБНОВЛЕНИЕ СТАТУСА:</b>\nНамотайте это на ус, оператор, учиться придется на ходу. Нас ждёт следующая задача: сенсоры фиксируют швартовочные сигналы. 🚢 Грузовые подводные лодки прибывают на станцию и уже заплывают в разгрузочный ангар.</blockquote>\n\n🎥 <i>Включаю трансляцию из дока...</i>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_15_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 16: Запрос на новогодние ёлки от техников[cite: 1] ---
kb_chapter1_16_dict = {
    "button1": "Обращусь в отдел гидропоники",
    "button2": "Давайте найдем компромисс"
}


@chapter1.message_created(
    F.message.body.text == kb_chapter1_15_dict["button1"],
    Chapter1States.s15
)
async def chapter1_16(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s16)

    media = InputMedia("media/chapter1/ch16.jpg")

    last_message = await event.message.answer(
        text=(
                await print_resources(context) +
                "📦 Так-с... Ремкомплекты на месте, фильтры привезли, сухпай обновлён. <b>А где главное-то?...</b>\n\n🎄 До Нового года недалеко, а в накладной опять ни одной ёлки! Понимаю, конечно, мелочь... Тут под толщей океана не до гирлянд, да и место под грузы не резиновое.\n\n🌱 <i>Но слушай, а если мы учёных из отдела гидропоники попросим?</i> Вдруг у них найдётся пара свободных лотков и семена? Вырастим хотя бы маленькие елочки. Хоть праздником на станции запахло бы... 🍊"
                ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_16_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 17: Обращение в гидропонику за ёлками[cite: 1] ---
kb_chapter1_17_dict = {
    "button1": "Сделаем праздник людям",
    "button2": "Красиво, но слишком дорого"
}
@chapter1.message_created(
    F.message.body.text == kb_chapter1_16_dict["button1"],
    Chapter1States.s16
)
async def chapter1_17(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s17)

    media = InputMedia("media/chapter1/ch23.jpg")

    last_message = await event.message.answer(
        text=(
                await print_resources(context) +
                "🍅 <b>Осторожно, не задень стойки с экспериментальными томатами!</b> У меня тут работа кипит, графики освещения расписаны по минутам, а времени впритык...\n\n🌲 <i>Но ёлочки для суровых парней из дока? Чтобы поддержать их под километровой толщей воды?</i> Знаешь, ради такого дела я готова заморозить текущие исследования. ❄️"
                ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_17_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 18: Компромисс с роботом (Неудача)---
kb_chapter1_18_dict = {"button1": "Главное, что люди счастливы"}
@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_16_dict["button2"], kb_chapter1_17_dict["button2"]]),
    StateFilter(Chapter1States.s16, Chapter1States.s17)
)
async def chapter1_18(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s18)  # Переход к следующему общему стейту

    await edit_resources(context, finance_delta=-1)

    media = InputMedia("media/chapter1/ch18.jpg")

    last_message = await event.message.answer(
        text=(
                await print_resources(context) +
                "⚠️ <b>Идея с компромиссом сработала:</b> экипаж украсил патрульного робота праздничным декором, что повысило моральный дух смены на 14%.\n\n💥 <i>Однако мерцающая гирлянда ослепила оптические сенсоры дрона</i> — он принял её за целеуказатель угрозы, протаранил гидравлический пресс и сломал манипулятор.\n\n💸 <b>Поздравляю с праздничной атмосферой</b>, счёт от Службы Безопасности за экстренный ремонт техники уже списан с вашего бюджета."),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_18_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 19: Знакомство с проблемой планктона ---
kb_chapter1_19_dict = {
    "button1": "Выделить бюджет на инкубаторы",
    "button2": "Перевести в помощь техников",
    "button3": "Составить карту процесса"
}
@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_17_dict["button1"], kb_chapter1_18_dict["button1"]]),
    StateFilter(Chapter1States.s17, Chapter1States.s18)
)
async def chapter1_19(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s19)

    # Если пришли из успешной ветки (Сделаем праздник), списываем еду
    if event.message.body.text == kb_chapter1_17_dict["button1"]:
        await edit_resources(context, food_delta=-1)
        await context.update_data(trees = 1)

    if event.message.body.text == kb_chapter1_18_dict["button1"]:
        append_text = "<b>📡 Связь установлена...</b>\n\nРада наконец выйти с вами на контакт.\n<i>Простите, что без долгих приветствий, у нас здесь сейчас каждая минута на счету.</i>\n\n"
    else:
        append_text = ""

    media = InputMedia("media/chapter1/ch19.jpg")

    last_message = await event.message.answer(
        text=(
                await print_resources(context) + append_text +
                "🧪 <b>Мы в лаборатории вывели штамм биолюминесцентного планктона</b> — хотели запитать праздничную иллюминацию и обогрев жилых секторов.\n\n"
                "Но культура растёт катастрофически медленно, биомассе не хватает плотности! Нам жизненно необходим бюджет на закупку ещё одного каскада инкубаторов! Без них станция просто застрянет в холоде и полутьме!"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_19_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

# Варианты клавиатур для следующих узлов
kb_chapter1_20_dict = {
    "button1": "Гипотеза 1",
    "button2": "Гипотеза 2",
    "button3": "Гипотеза 3",
}

kb_chapter1_bad_dict = {"button1": "Это прискорбно"}

kb_chapter1_24_dict = {"button1": "Выйти на связь"}


# --- УЗЕЛ 20: Карта процессов ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_19_dict["button3"],
    Chapter1States.s19
)
async def chapter1_20(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s20)
    await edit_resources(context, energy_delta=-1)

    media = InputMedia("media/chapter1/ch20.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
    "📊 <b>ОПЕРАТИВНАЯ СВОДКА СТАНЦИИ «ПРОЦЕСС»</b>\n\n"
    "🔬 <i>VSM-АНАЛИЗАТОР ПЛАНКТОНА</i>\n\n"
    "👨‍💼 <b>Оператор</b>, получена свежая аналитика по производству планктона.\n\n"
    "<blockquote>📌 <b>Гипотеза 1:</b> Надо срочно докупить ещё один инкубатор ТГ-4</blockquote>\n\n"
    "<blockquote>📌 <b>Гипотеза 2:</b> Проблема в очистке осадка, вероятно, забивает фильтры</blockquote>\n\n"
    "<blockquote>📌 <b>Гипотеза 3:</b> Нужно добавить параллельную линию фильтрации</blockquote>\n\n"
    "❓ <b>Какую гипотезу вы выберете для проверки?</b>"
        ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_20_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 21_1: Покупка оборудования (Из 19 и 20 узла) ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_19_dict["button1"],
    StateFilter(Chapter1States.s19)
)
async def chapter1_21_1(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s21)
    await edit_resources(context, finance_delta=-3, energy_delta=-1)

    media = InputMedia("media/chapter1/ch21.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
    "<b>⚠️ Плохие новости</b>\n\n"
    "У меня плохие новости. Все <b>пятьдесят тысяч</b> ушли на новые каскады инкубаторов 🧪.\n\n"
    "Лаборатория забита под завязку, оборудование гудит ⚙️, чаши полны планктона 🧫... "
    "<i>но на выходе энергии всё так же мало!</i> ⚡️"),
attachments=[
            media,
            base_keyboard_maker(kb_chapter1_bad_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 21_2: Перевод техников (Из 19 узла) ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_19_dict["button2"],
    Chapter1States.s19
)
async def chapter1_21_2(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s21)
    await edit_resources(context, finance_delta=-1, energy_delta=-2, food_delta=-1)

    media = InputMedia("media/chapter1/ch21.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "<b>⚠️ Нарушение регламента</b>\n\n"
    "По регламенту работы с <i>опасными биокультурами</i> ☣️ я не имела права подпустить инженеров к инкубаторам 🧪 без прохождения курса техники безопасности!\n\n"
    "В итоге мои люди вместо планктона 🧫 занимались лекциями 📚, <b>производство упало ещё ниже</b> 📉, а из реакторного отсека на нас уже орёт их начальник!"),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_bad_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 22: Проблема в очистке осадка (Из 20 узла) ---
@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_20_dict["button1"],kb_chapter1_20_dict["button2"]]),
    Chapter1States.s20
)
async def chapter1_22(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s22)
    await edit_resources(context, finance_delta=-3, energy_delta=-1)

    media = InputMedia("media/chapter1/ch17.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "<b>💸 Финансовые потери и провал</b>\n\n"
    "Решение оказало медвежью услугу. Мы списали <b>солидный бюджет</b> 💰, но так и не расширили главное узкое место процесса.\n\n"
    "Производительность осталась <i>на нуле</i> 📉, биомасса гибнет ☣️, а станция несёт прямые финансовые потери!\n\n"
    "⏳ <b>Восемь часов на фильтрации</b> — это был наш главный тормоз. Если бы мы сократили это время хотя бы вдвое, весь поток пошёл бы быстрее, но уже слишком поздно..."),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_bad_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)

kb_chapter1_good_dict = {"button1": "Отлично!"}
# --- УЗЕЛ 23: Параллельная фильтрация - Успех (Из 20 узла) ---
@chapter1.message_created(
    F.message.body.text == kb_chapter1_20_dict["button3"],
    Chapter1States.s20
)
async def chapter1_23(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s23)
    await edit_resources(context, finance_delta=1, energy_delta=1)

    media = InputMedia("media/chapter1/ch23.jpg")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "<b>🎯 Вот это попадание!</b>\n\n"
    "<code>8 часов</code> на фильтрации — это наш главный тормоз ⏳. "
    "Если мы сократим это время хотя бы вдвое, <i>весь поток пойдет быстрее</i>.\n\n"
    "Ты смотришь в корень — давай проработаем детали и запустим пилот! 🤝"),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_good_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# --- УЗЕЛ 24: Экстренный вызов (Общий выход) ---
@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_bad_dict["button1"], kb_chapter1_good_dict["button1"]]),
    StateFilter(Chapter1States.s21, Chapter1States.s21, Chapter1States.s22, Chapter1States.s23)
)
async def chapter1_24(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s24)

    media = InputMedia("media/chapter1/ch24.png")

    last_message = await event.message.answer(
        text=(
            await print_resources(context) +
            "<blockquote>"
            "⚠️ <b>ВНИМАНИЕ, ОПЕРАТОР!</b>\n\n"
            "⏱️ <b>Каждая секунда работы станции имеет критическое значение.</b>\n\n"
            "🔄 Потоки <b>ресурсов</b>, <b>информации</b> и <b>управленческих решений</b> должны двигаться точно, быстро и <i>без задержек</i>.\n\n"
            "🗺️ Для контроля этих процессов инженеры используют <b>карту потока создания ценности (Value Stream Mapping)</b> — специальный инструмент анализа, который позволяет:\n\n"
            "🔍 <b>увидеть полный путь процесса</b> от начала до результата;\n"
            "⚠️ <b>обнаружить узкие места и задержки</b> в системе;\n"
            "♻️ <b>устранить лишние операции и потери ресурсов.</b>\n\n"
            "⚙️ Благодаря <b>VSM</b> команда станции может быстрее находить неисправности, оптимизировать работу отделов и сохранять стабильность всей системы даже в критических ситуациях."
            "</blockquote>\n\n"
            "<b>🚨 ЭКСТРЕННЫЙ ВЫЗОВ</b>\n\n"
    "📞 Оператор, <i>научный отдел</i> обрывает все линии связи, и, кажется, они там очень взволнованы.\n\n"
    "📡 <b>Требуют срочно посмотреть на радары!</b>\n"
    "🖥️ <i>Перевожу их на главный экран...</i>"),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_24_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_25_dict = {
    "button1": "Пусть инженеры займутся модификацией",
    "button2": "Отправьте «Одиссей». Готовьте экипаж"
}
@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_24_dict.values()),
    Chapter1States.s24
)
async def chapter1_25(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s25)

    data = await context.get_data()
    has_odyssey = data["odyssey"]

    # Формируем основной текст с динамической вставкой про «Одиссей»
    base_text = (
    "📡 <b>АНОМАЛЬНЫЙ ВСПЛЕСК ЭНЕРГИИ</b>\n\n"
    "Оператор, взгляните на экраны 🖥️.\nРадары глубоководного сектора только что "
    "засекли мощнейший всплеск аномальной энергии из бездны 🌊⚡.\n"
    "Это не сейсмика и точно не глубинная фауна… <i>там лежит что-то искусственное!</i>\n\n"
    "Чтобы спуститься и изучить источник, нужен батискаф 🥽.\n<blockquote>Но наши новые «Мотыльки» "
    "не рассчитаны на такое экстремальное давление. Их обшивку просто сминает "
    "на этой глубине 💥 — <b>требуется экстренная модернизация</b>.</blockquote>\n\n"
    )

    if has_odyssey:
        extra_text = (
            "⚓ Впрочем… у нас всё ещё стоит в доке старый <code>«Одиссей»</code>.\n"
    "У него <b>титановый корпус</b> 🛡️ — он пройдёт эту глубину без проблем и без лишних трат! 💵"
        )
        # Кнопка 2 доступна
        active_buttons = kb_chapter1_25_dict
    else:
        extra_text = (
            "⚙️ <i>Жаль, что «Одиссей» мы ранее пустили на металлолом и запчасти…</i>\n\n"
    "Теперь у нас нет выбора: придётся <b>вложить ресурсы</b> 💎 "
    "и экстренно укреплять <code>«Мотылёк»</code> 🛠️."
        )
        active_buttons = {"button1": kb_chapter1_25_dict["button1"]}

    full_text = base_text + extra_text

    media = InputMedia("media/chapter1/ch25.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) + full_text),
        attachments=[
            media,
            base_keyboard_maker(active_buttons),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_26_dict = {"button1": "В добрый путь!"}
@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_25_dict.values()),
    Chapter1States.s25
)
async def chapter1_26(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s26)

    # Проверяем, какую кнопку нажали в ивенте 25, и выбираем соответствующий текст и ресурсы
    if event.message.body.text == kb_chapter1_25_dict["button1"]:
        await edit_resources(context, finance_delta=-3, food_delta=-2)
        body_text = (
            "🔧 <b>УКРЕПЛЕНИЕ ОБШИВКИ</b>\n\n"
    "Понял. Инженеры уже приступают к укреплению обшивки 🛠️.\n\n"
    "<i>Это займёт время</i> ⏳, а также потребуется много ресурсов 💎…"
        )
    elif event.message.body.text == kb_chapter1_25_dict["button2"]:
        body_text = (
            "🌊 <b>ПОГРУЖЕНИЕ «ОДИССЕЯ»</b>\n\n"
    "Принято! 👨‍✈️ Экипаж уже занимает места в шлюзовой камере.\n\n"
    "⚙️ <b>Запускаем системы <code>«Одиссея»</code>…</b> 🫧"
        )
    else:
        body_text = (
            "ыыы? в 25-ом разве были кнопки кроме 1 и 2?"
        )

    media = InputMedia("media/chapter1/ch26.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              f"{body_text}"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_26_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_27_dict = {
    "button1": "Ждем, когда они починят связь"}


@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_26_dict.values()),
    Chapter1States.s26
)
async def chapter1_27(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s27)

    media = InputMedia("media/chapter1/ch27.mp4")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
    "Экспедиция на связи. Давление в норме, погружение штатное. Есть визуальный контакт с объектом! "
    "Подождите… приборы фиксируют аномальный электромагнитный импульс…\n\n"
    "<blockquote>У нас… сильнейшие помехи… Перехожу на резервный канал! "
    "Нави-и-гация зависла! Электроника отказ…*** Повторяю, мы теряем телеметрию, теряем…</blockquote>\n\n"
    "<i>(Раздаётся резкий щелчок, после чего в эфире повисает глухой белый шум)</i> 🔇"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_27_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_28_dict = {"button1": "→"}


@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_27_dict.values()),
    Chapter1States.s27
)
async def chapter1_28(event: MessageCreated, context: MemoryContext):
    await context.set_state(Chapter1States.s28)

    media = InputMedia("media/chapter1/ch28.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "📡 <b>ПОЛНАЯ ТИШИНА В ЭФИРЕ</b>\n\n"
    "Эфир абсолютно чист… Сигнал от батискафа пропал окончательно. "
    "Они словно растворились во мраке 🌊. Я оставил канал открытым, Оператор, вдруг они…\n\n"
    "⚠️ <b>ТРЕВОГА СИСТЕМЫ ЖИЗНЕОБЕСПЕЧЕНИЯ</b>\n"
    "Буль… Оператор, мне жаль тебя отвлекать, но ситуация критическая.\n\n"
    "<blockquote>🩸 <b>Показатели крови персонала стремительно падают!</b>\n"
    "Дежурный медик сообщает про <i>критическую нехватку витаминов</i> и… <b>эпидемию?</b></blockquote>\n\n"
    "🩺 Вывожу её на связь!"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_28_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# -----------------------------------------------------------------------------
# Кнопка 3 доступна только если есть ёлки.
# В base_keyboard_maker: если resources["trees"] == 0 (или нет переменной),
# не добавлять button3 в словарь, передаваемый в base_keyboard_maker.
# -----------------------------------------------------------------------------

kb_chapter1_29_dict = {
    "button1": "Запросить доставку медикаментов",
    "button2": "Использовать ёлки! Заварить отвар",
    "button3": "Поручить аналитикам найти решение"
}
kb_chapter1_30_dict = {"button1": "→"}

@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_28_dict["button1"], kb_chapter1_30_dict["button1"]]),
    StateFilter(Chapter1States.s28, Chapter1States.s30)
)
async def chapter1_29(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s29)

        # Формируем клавиатуру: button3 только если есть ёлки
    active_buttons = {
        "button1": kb_chapter1_29_dict["button1"],
        "button3": kb_chapter1_29_dict["button3"],
    }

    data = await context.get_data()
    trees = data["trees"]

    if trees > 0:
        active_buttons["button2"] = kb_chapter1_29_dict["button2"]

    media = InputMedia("media/chapter1/ch29.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
    "Оператор, пока всё внимание штаба было приковано к пропавшему батискафу, "
    "у нас случилась катастрофа локального масштаба. "
    "У дежурной смены уже фиксируется кровоточивость дёсен, суставные боли и дикая усталость.\n\n"
    "<blockquote>⚠️ <b>Это цинга, Оператор.</b>\n"
    "На глубине четырёх километров, без солнечного света и витаминов, "
    "экипаж ляжет через считанные дни.</blockquote>\n\n"
    "🍋 <i>Нам срочно нужен Витамин C!</i>"
              ),
        attachments=[
            media,
            base_keyboard_maker(active_buttons),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


@chapter1.message_created(
    F.message.body.text == kb_chapter1_29_dict["button3"],
    Chapter1States.s29
)
async def chapter1_30(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s30)
    await edit_resources(context, energy_delta=-1)

    media = InputMedia("media/chapter1/ch30.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "📉 <b>ПУСТАЯ ПАПКА</b>\n\n"
    "Аналитический отдел списал солидный бюджет 💸 на срочные исследования, "
    "но на стол легла <i>пустая папка</i> 📁.\n\n"
    "<blockquote>🍋 Они говорят, что нужно просто <b>съесть лимон</b>…</blockquote>\n\n"
    "Гениальная аналитика!"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_30_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_31_dict = {"button1": "Здоровье экипажа это главное"}


@chapter1.message_created(
    F.message.body.text.in_([kb_chapter1_29_dict["button1"], kb_chapter1_29_dict["button2"]]),
    Chapter1States.s29
)
async def chapter1_31(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s31)

    if event.message.body.text == kb_chapter1_29_dict["button1"]:
        await edit_resources(context, finance_delta=-2, food_delta=-1)
        body_text = (
            "✅ <b>ЗАКАЗ ФАРМ-ПРЕПАРАТОВ</b>\n\n"
    "Принято. Это сожрёт львиную долю нашего экстренного бюджета 💸 "
    "и придётся подождать…\n\n"
    "<blockquote>💊 Зато фарм-препараты поставят людей на ноги "
    "<b>быстро и без лишних экспериментов</b>.</blockquote>\n\n"
    "📦 <i>Оформляю заказ…</i>"
        )
    else:
        body_text = (
    "Хвойный отвар?! А ведь это гениально… 💡\n\n"
    "<blockquote>🍵 В свежей хвое концентрация <b>витамина C</b> в разы выше, чем в цитрусовых! "
    "Вкус у этого «чая», конечно, будет специфический, и экипаж поворчит…</blockquote>\n\n"
    "💰 <i>Но мы спасём людей и не потратим ни единой копейки из бюджета!</i>"
        )

    media = InputMedia("media/chapter1/ch31.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              f"{body_text}"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_31_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_32_dict = {"button1": "Свяжите меня со службой безопасности!"}


@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_31_dict.values()),
    Chapter1States.s31
)
async def chapter1_32(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s32)

    media = InputMedia("media/chapter1/ch32.mp4")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "🚨 <b>ВНИМАНИЕ! КРАСНЫЙ КОД!</b> 🚨\n\n"
    "Оператор, это не учебная тревога! Показания дальних сонаров зашкаливают! 📡\n\n"
    "<blockquote>🌊 <b>Из донной аномальной зоны поднялся массивный объект.</b>\n"
    "Он стремительно движется прямо на нас!</blockquote>\n\n"
    "⚠️ <i>Все системные тревоги активированы!</i>"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_32_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# -----------------------------------------------------------------------------
# ВЕТВЛЕНИЕ ПО ПЕРЕМЕННОЙ radar (1–3):
# radar=1 (плохой радар):   обязательно запускает торпеды — кнопки -1
# radar=2 (средний радар):  спрашивает согласие — кнопки 2, 3
# radar=3 (топовый радар):  Объект опознан как свой батискаф — кнопка 4
# -----------------------------------------------------------------------------
kb_chapter1_33_dict = {
    "button1": "Стой, отмена!..",
    "button2": "Огонь! Безопасность важнее",
    "button3": "Отставить огонь",
    "button4": "Отличная работа. Открывайте шлюзы"
}


@chapter1.message_created(
    F.message.body.text.in_(kb_chapter1_32_dict.values()),
    Chapter1States.s32
)
async def chapter1_33(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s33)

    data = await context.get_data()
    radar = data["radar"]

    # Кнопки, доп текст и картинка в зависимости от уровня радара
    if radar == 1:
        active_buttons = {"button1": kb_chapter1_33_dict["button1"]}
        radar_text = (
            "⚠️ <b>КРИТИЧЕСКОЕ СБЛИЖЕНИЕ</b>\n\n"
    "Оператор, объект стремительно приближается и уже находится "
    "в опасной близости от станции 🌊.\n\n"
    "<b>Протоколы безопасности обязывают меня запустить торпеды.</b>\n\n"
    "<i>Выполняю…</i>"
        )
        media = InputMedia("media/chapter1/ch33.png")
    elif radar == 2:
        active_buttons = {
            "button2": kb_chapter1_33_dict["button2"],
            "button3": kb_chapter1_33_dict["button3"]}
        radar_text = (
            "🚨 <b>НЕОПОЗНАННАЯ ЦЕЛЬ</b>\n\n"
    "Оператор, сигнатура сильно искажена радиацией ☢️ и помехами 📡.\n"
    "На таком расстоянии невозможно идентифицировать объект, и он стремительно приближается 🌊.\n\n"
    "💥 <b>Нам предписано открыть огонь.</b>\n\n"
    "<i>Есть возражения?</i>"
        )
        media = InputMedia("media/chapter1/ch33.png")
    else:  # radar == 3
        await edit_resources(context, energy_delta=-1)
        active_buttons = {"button4": kb_chapter1_33_dict["button4"]}

        radar_text = (
            "📡 <b>ОБЪЕКТ ИДЕНТИФИЦИРОВАН!</b>\n\n"
    "Секунду, подключаю наш топовый секретный радар для глубокой фильтрации "
    "аномального сигнала 🔍. Все электромагнитные искажения сняты!\n\n"
    "<blockquote>🟢 <b>Это точная сигнатура нашего батискафа!</b>\n\n"
    "Экипаж цел 👨‍✈️, системы жизнеобеспечения в норме. "
    "Похоже, у них просто отказали системы связи.</blockquote>"
        )
        media = InputMedia("media/chapter1/ch34g.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "📡 <b>ОБНАРУЖЕНИЕ ОБЪЕКТА</b>\n\n"
    "Радары безопасности только что засекли крупный объект 🌊.\n\n"
    "<blockquote>⚠️ <b>Он стремительно поднимается со дна прямо к нашему сектору!</b>\n\n"
    "<i>Система уже расшифровывает данные радара…</i> 🔍</blockquote>\n\n"
              f"{radar_text}"
              ),
        attachments=[
            media,
            base_keyboard_maker(active_buttons),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_34_1_dict = {"button1": "Начинайте спасательную операцию."}
@chapter1.message_created(
    F.message.body.text == kb_chapter1_33_dict["button1"],
    Chapter1States.s33
)
async def chapter1_34_1(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s34)

    media = InputMedia("media/chapter1/ch34b.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "💥 <b>КРИТИЧЕСКАЯ ОШИБКА</b>\n\n"
              "Объект подбит и стремительно теряет высоту, уходя ко дну… 🌊\n\n"
              "<blockquote>⚠️ <b>Система определила объект. Это наш батискаф.</b>\n\n"
              "Чёртов старый радар… Эх, вот если бы смогли его засечь раньше!</blockquote>\n\n"
              "🛡️ Укреплённый корпус выдержал взрыв, но они <b>полностью обесточены</b> и застряли на самом дне."
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_34_1_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_34_2_dict = {
    "button1": "Начинайте спасательную операцию"}


@chapter1.message_created(
    F.message.body.text == kb_chapter1_33_dict["button2"],
    Chapter1States.s33
)
async def chapter1_34_2(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s34)

    media = InputMedia("media/chapter1/ch34b.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "💥 <b>ПРИНЯТО… ПРЯМОЕ ПОПАДАНИЕ</b>\n\n"
    "Объект подбит и стремительно теряет высоту, уходя ко дну… 🌊\n\n"
    "<blockquote>🚨 <b>Система определила объект. Это наш батискаф!</b>\n\n"
    "Укреплённый корпус выдержал взрыв 🛡️, но они <b>полностью обесточены</b> "
    "и застряли на самом дне.</blockquote>"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_34_2_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_34_3_dict = {"button1": "Готовьте инженеров и приёмную команду"}


@chapter1.message_created(
    F.message.body.text == kb_chapter1_33_dict["button3"],
    Chapter1States.s33
)
async def chapter1_34_3(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s34)

    media = InputMedia("media/chapter1/ch34g.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "🛡️ <b>ОТБОЙ ТРЕВОГИ</b>\n\n"
    "Принято… Но если неопределённый объект приблизится слишком близко, "
    "я всё равно буду вынужден…\n\n"
    "<blockquote>🟢 <b>Система определила объект: это наш батискаф!</b>\n\n"
    "<i>Отбой тревоги!</i> ⚓</blockquote>"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_34_3_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_36_dict = {"button1": "Что это?"}


@chapter1.message_created(F.message.body.text.in_(
    [kb_chapter1_34_1_dict["button1"], kb_chapter1_34_2_dict["button1"], kb_chapter1_34_3_dict["button1"],
     kb_chapter1_33_dict["button4"]]), StateFilter(Chapter1States.s33, Chapter1States.s34))
async def chapter1_36(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s36)
    if event.message.body.text in ([kb_chapter1_34_1_dict["button1"], kb_chapter1_34_2_dict["button1"]]):
        await edit_resources(context, finance_delta=-3, food_delta=-1)

    media = InputMedia("media/chapter1/ch36.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "📦 <b>ДОСТАВКА АРТЕФАКТА</b>\n\n"
    "Тяжёлые гидрозамки шлюза с шипением разжимаются. "
    "Мощные лебёдки со скрипом вытягивают из грузового отсека батискафа массивный контейнер.\n\n"
    "🔮 Внутри него пульсирует <b>загадочный артефакт</b> — гладкий монолит из тёмного металла, "
    "покрытый <i>мерцающими прожилками свечения</i>.\n\n"
    "⚡ Электрика ангара на секунду притухает, реагируя на его поле…"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_36_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_37_dict = {"button1": "Хорошие новости!"}


@chapter1.message_created(F.message.body.text.in_(kb_chapter1_36_dict.values()), Chapter1States.s36)
async def chapter1_37(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s37)

    media = InputMedia("media/chapter1/ch37.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "🤩 <b>НАХОДКА ВЕКА!</b>\n\n"
    "Невероятно… Вы только посмотрите на эти показатели! 📊\n"
    "Это не просто древняя аномалия — <b>структура металла полностью противоречит известным законам физики</b>.\n\n"
    "⚡ Сплав генерирует чистую энергию буквально из ничего. Оператор, это настоящая находка века!\n\n"
    "🔬 <i>Мы обязаны произвести исследования этого удивительного материала. "
    "Что касается перебоев, думаю, мы сможем это решить в ближайшее время.</i>"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_37_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_38_dict = {"button1": "→"}


@chapter1.message_created(F.message.body.text.in_(kb_chapter1_37_dict.values()), Chapter1States.s37)
async def chapter1_38(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s38)
    await edit_resources(context, energy_delta=-2)

    media = InputMedia("media/chapter1/ch38.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
              "🚨 <b>КРИТИЧЕСКИЙ СБОЙ!</b>\n\n"
    "⚡ <i>Внезапно свет на станции начинает мигать. Экраны покрываются рябью…</i>\n\n"
    "👾 Спрайт ИИ-Тюленчика искажается глитчами, он издаёт <b>жалобный механический скрежет</b> "
    "и распадается на пиксели.\n\n"
    "🔔 <b>ЗВУЧИТ СИРЕНА!</b>"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_38_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_39_dict = {"button1": "→"}


@chapter1.message_created(F.message.body.text.in_(kb_chapter1_38_dict.values()), Chapter1States.s38)
async def chapter1_39(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s39)

    media = InputMedia("media/chapter1/ch39.png")

    last_message = await event.message.answer(
        text=(await print_resources(context) +
    "📞 <b>СРОЧНЫЙ ВИДЕОВЫЗОВ — НАЧАЛЬНИК СЛУЖБЫ БЕЗОПАСНОСТИ</b>\n\n"
    "Что вы наделали! Вы вызвали коллапс на станции!\n\n"
    "<blockquote>⚠️ <b>ЭМ-поле выжигает сеть. ИИ отключён, жизнеобеспечение в ручном режиме!</b></blockquote>\n\n"
    "Оператор, мы должны немедленно засунуть эту бомбу замедленного действия обратно в контейнер и отправить на поверхность, пока мы тут все не сварились!"
              ),
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_39_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


# кнопка 3 доступна только при финансах > 20
kb_chapter1_40_dict = {
    "button1": "Оставить артефакт в лаборатории",
    "button2": "Отправить артефакт в Центр",
    "button3": "Построить изоляционную камеру"
}


@chapter1.message_created(F.message.body.text.in_(kb_chapter1_39_dict.values()), Chapter1States.s39)
async def chapter1_40(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(Chapter1States.s40)

    media = InputMedia("media/chapter1/ch40.png")

    text = (
            await print_resources(context) +
    "Вы с ума сошли?! Отправить её бюрократам наверх? "
    "Это лишит нас шанса понять природу аномалии!\n\n"
    "<b>Оператор, не слушайте его!</b> 🛑"
    )

    data = await context.get_data()
    if data["finance"] < 90:
        active_keyboard = {
            "button1":kb_chapter1_40_dict["button1"], "button2":kb_chapter1_40_dict["button2"]
        }
    else:
        active_keyboard = kb_chapter1_40_dict

    last_message = await event.message.answer(
        text=text,
        attachments=[
            media,
            base_keyboard_maker(active_keyboard),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


kb_chapter1_41_dict = {"button1": "Закончить главу"}


@chapter1.message_created(
    F.message.body.text == kb_chapter1_40_dict["button1"],
    Chapter1States.s40
)
async def chapter1_41_1(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(MenuStates.menu)
    data = await context.get_data()
    if data["food_update"] == 1:
        await context.update_data(ch1_scientist=1, ch1_security=-1, ch1_worker=-1)
    else:
        await context.update_data(ch1_scientist=1, ch1_security=-1, ch1_worker=-1)
    media = InputMedia("media/chapter1/ch41_1.png")

    text = (
            await print_resources(context) +
    "Вы спятили. Если хотите играть с огнём — играйте! "
    "Но восстанавливать сожжённую электронику и поднимать ИИ с колен вы будете за счёт своего бюджета. "
    "<b>Мои люди к этому не притронутся.</b> 🛑"
    )

    last_message = await event.message.answer(
        text=text,
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_41_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


@chapter1.message_created(
    F.message.body.text == kb_chapter1_40_dict["button2"],
    Chapter1States.s40
)
async def chapter1_41_2(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(MenuStates.menu)
    data = await context.get_data()
    if data["food_update"] == 1:
        await context.update_data(ch1_scientist=-1, ch1_security=1, ch1_worker=1)
    else:
        await context.update_data(ch1_scientist=-1, ch1_security=1, ch1_worker=-1)
    media = InputMedia("media/chapter1/ch41_2.png")

    text = (
            await print_resources(context) +
            "Вы просто трус, Оператор.\n\n"
    "💔 <b>Вы отдали величайшее открытие столетия клеркам, которые запрут его в ангаре до скончания времён…</b>"
    )

    last_message = await event.message.answer(
        text=text,
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_41_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


@chapter1.message_created(
    F.message.body.text == kb_chapter1_40_dict["button3"],
    Chapter1States.s40
)
async def chapter1_41_3(event: MessageCreated, context: MemoryContext):
    if await check_bad_end(event, context):
        return

    await context.set_state(MenuStates.menu)
    data = await context.get_data()
    if data["food_update"] == 1:
        await context.update_data(ch1_scientist=1, ch1_security=1, ch1_worker=1)
    else:
        await context.update_data(ch1_scientist=1, ch1_security=1, ch1_worker=-1)
    media = InputMedia("media/chapter1/ch41_3.png")

    text = (
            await print_resources(context) +
    "⚡ <b>КОМПРОМИСС: ИЗОЛЯЦИОННАЯ КАМЕРА</b>\n\n"
    "🛡️ <b>Начальник СБ (удивлённо):</b> «Вы готовы слить весь наш резервный фонд "
    "на свинцовые экраны и независимый контур питания? Что ж… если эта штука будет "
    "сидеть в клетке и не фонить на мои системы — меня это устроит.»\n\n"
    "🔬 <b>Учёный (в восторге):</b> «Идеальный компромисс!\n\n"
    "<blockquote>🧪 <b>Изолированная среда позволит нам безопасно считывать данные. Оператор, вы гений!</b></blockquote>"
    )

    last_message = await event.message.answer(
        text=text,
        attachments=[
            media,
            base_keyboard_maker(kb_chapter1_41_dict),
        ],
        parse_mode=ParseMode.HTML
    )
    await remove_keyboard(last_message, media, context)


@chapter1.message_created(Chapter1States.bad_end)
async def bad_end(event: MessageCreated, context: MemoryContext):
    await main_menu(event.chat.chat_id, context)
