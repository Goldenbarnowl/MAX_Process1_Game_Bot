from maxapi import Router, F, Bot
from maxapi.context import MemoryContext
from maxapi.enums import ParseMode
from maxapi.filters.command import Command
from maxapi.types import MessageCreated, InputMedia, BotCommand

from config import settings, bot
from functions.name_validation import validate_name
from functions.remove_keyboards import remove_keyboard
from handlers.chapter1 import kb_chapter1_41_dict
from handlers.menu import main_menu
from keyboards.menu_kb import kb_menu1, kb_menu1_dict, kb_menu2, kb_menu2_dict, kb_menu3, kb_menu3_dict, kb_menu5_dict, \
    kb_menu5
from states.menu_states import MenuStates

introduction = Router()


@introduction.bot_started()
@introduction.message_created(Command("start"))
async def start_handler(event, context: MemoryContext):
    chat_id = event.chat.chat_id
    await bot.set_commands(
        BotCommand(
            name="start",
            description="Запуск"
        ),
        BotCommand(
            name="help",
            description="Помощь"
        ),
        BotCommand(
            name="edit_name",
            description="Изменить имя пользователя"
        ),
        BotCommand(
            name="present",
            description="Получить подарок"
        ),

    )

    data = await context.get_data()

    if data.get("briefing", 0) == 1:
        await main_menu(chat_id, context)

    else:

        media = InputMedia("media/menu/menu1.jpg")
        last_message = await bot.send_message(
            chat_id=chat_id,
            text=(
                "Приветствуем в нашей бизнес игре! Здесь ты легко и с удовольствием научишься менеджменту и аналитике процессов 🚀\n\n"
                "<blockquote>📌 <i>Дисклеймер: Все персонажи и история вымышлены, совпадения совершенно случайны.</i></blockquote>\n\n"
                "🖥️ Нажимай на <b>кнопки ниже</b> для взаимодействия.\n\n"
            ),
            attachments=[
                media,
                kb_menu1()
            ],
            parse_mode=ParseMode.HTML
        )

        await context.set_state(MenuStates.m1)
        await context.update_data(last_message=last_message)
        await context.update_data(last_media=media)


@introduction.message_created(F.message.body.text == kb_menu1_dict["button1"], MenuStates.m1)
async def menu_m2(event: MessageCreated, context: MemoryContext):
    media = InputMedia("media/menu/menu2.mp4")
    last_message = await event.message.answer(
        text=(
            "<b>🦭 Бип-буль!</b> Приветствую, <b>Оператор</b>!\n\n"
"Я —\n<b>П</b>латформа\n<b>Л</b>огистического\n<b>О</b>беспечения\n<b>М</b>ониторинга\n<b>Б</b>езопасности\n<b>И</b>сследований\n<b>Р</b>ешений\n"
"<code>П.Л.О.М.Б.И.Р</code>\n\n"
"⚓ Готов сделать вашу работу <i>на глубине</i> — комфортной и <b>безопасной</b>!"
        ),
        attachments=[
            media,
            kb_menu2()
        ],
        parse_mode=ParseMode.HTML
    )
    await context.set_state(MenuStates.m2)
    await remove_keyboard(last_message,media,context)


@introduction.message_created(F.message.body.text == kb_menu2_dict["button1"], MenuStates.m2)
async def menu_m3(event: MessageCreated, context: MemoryContext):
    media = InputMedia("media/menu/menu3.mp4")
    last_message = await event.message.answer(
        text=(
            "🐟 <b>Отличный вопрос!</b>\n\n"
"💬 Отдел корпоративной психологии установил, что этот <i>визуальный аватар</i> снижает приступы клаустрофобии и панических атак у персонала на целых <b>18.4%</b>.\n\n"
"⚓ Моя <b>фуражка</b> внушает доверие, не так ли?"
        ),
        attachments=[
            media,
            kb_menu3()
        ],
        parse_mode=ParseMode.HTML
    )
    await context.set_state(MenuStates.m3)
    await remove_keyboard(last_message,media,context)


@introduction.message_created(Command("edit_name"))
@introduction.message_created(F.message.body.text.in_([kb_menu3_dict["button1"], kb_menu3_dict["button2"]]), MenuStates.m3)
async def menu_m4(event: MessageCreated, context: MemoryContext):
    media = InputMedia("media/menu/menu4.mp4")
    last_message = await event.message.answer(
        text=(
            "⚓ <b>Моя задача</b> — управлять станцией.\n"
"🤖 Ваша задача — контролировать меня.\n\n"
"✨ Мы станем <b>отличной командой</b>!\n\n"
"🔧 Для завершения инициализации и синхронизации с вашим терминалом:\n"
"<blockquote>✨<i>Пожалуйста, напишите в чат, как я могу <b>Вас называть</b>.</i></blockquote>"
        ),
        attachments=[
            media,
        ],
        parse_mode=ParseMode.HTML
    )
    await context.set_state(
        state=MenuStates.name
    )
    await remove_keyboard(last_message,media,context)


@introduction.message_created(MenuStates.name)
async def menu_m5(event: MessageCreated, context: MemoryContext):
    name = event.message.body.text.strip()

    if not validate_name(name):
        await event.message.answer(
            "❌ Имя должно содержать только кириллицу и быть не длиннее 20 символов."
        )
        return

    await context.update_data(
        name=name
    )
    media = InputMedia("media/menu/menu5.mp4")
    last_message = await event.message.answer(
        text=(
            f"🔐 <b>{name}</b>, Ваш профиль успешно авторизован.\n\n"
"🌐 Теперь мы с вами связаны одной <i>локальной сетью</i> и великой целью науки!\n\n"
"⚠️ Если я вдруг решу по ошибке откачать кислород из жилого отсека —\n"
"вы узнаете об этом <b>первым</b>!\n\n"
"🤖 Мои юмористические алгоритмы еще находятся в стадии <b>калибровки</b>."
        ),
        attachments=[
            media,
            kb_menu5()
        ],
        parse_mode=ParseMode.HTML
    )
    await context.set_state(MenuStates.menu)
    await remove_keyboard(last_message, media, context)


@introduction.message_created(F.message.body.text.in_([kb_menu5_dict["button1"], kb_chapter1_41_dict["button1"]]), MenuStates.menu)
async def menu_m6(event: MessageCreated, context: MemoryContext):
    await main_menu(event.chat.chat_id, context)
