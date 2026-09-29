from maxapi import F, Router
from maxapi.context import MemoryContext
from maxapi.enums import ParseMode
from maxapi.filters.command import Command
from maxapi.types import InputMedia, MessageCreated

from config import bot
from functions.base_keyboard_maker import base_keyboard_maker
from functions.remove_keyboards import remove_keyboard
from functions.reputation import get_reputation_text
from functions.send_sticker import send_sticker
from keyboards.menu_kb import kb_menu6, kb_menu6_dict
from states.menu_states import MenuStates

menu = Router()


async def main_menu(chat_id, context: MemoryContext):
    media = InputMedia("media/menu/menu3.mp4")
    await context.set_state(MenuStates.menu)

    data = await context.get_data()
    print(data)
    last_message = await bot.send_message(
        chat_id=chat_id,
        text=(
            f"✅ <b>Синхронизация завершена.</b>\n\n"
            f"🖥️ <b>Терминал готов к работе.</b>\n\n"
            f"⚙️ {data["name"]}, пожалуйста, выберите действие на панели управления,\n"
            f"чтобы официально начать вашу смену на комплексе <b>«Процесс-1»</b>."
        ),
        attachments=[
            media,
            await kb_menu6(context)
        ],
        parse_mode=ParseMode.HTML
    )
    await context.update_data(briefing=1)
    await remove_keyboard(last_message,media,context)


@menu.message_created(F.message.body.text == kb_menu6_dict["button4"], MenuStates.menu)
async def menu_reputation(event: MessageCreated, context: MemoryContext):
    await event.message.answer(
        text=(
            await get_reputation_text(context)
        ),
        parse_mode=ParseMode.HTML
    )


library_keyboard = {"button1": "Лекция 1 - Основы менеджмента", "button2" : "🎁 Получить подарок"}
@menu.message_created(F.message.body.text == kb_menu6_dict["button2"], MenuStates.menu)
async def library(event: MessageCreated, context: MemoryContext):

    media = InputMedia("media/menu/library.mp4")

    last_message = await event.message.answer(
        text=(
            "📚 <b>Учебные материалы</b> 🦭\n\n"
            "<i>Здесь собраны необходимые материалы для обучения экипажа.</i> 📖\n\n"
            "Это архив лекций подводной станции, где Вы найдёте всё необходимое "
            "для решения задач, выполнения заданий и прохождения испытаний. ⚙️\n\n"
            "🌊 <i>Изучайте внимательно: даже на глубине ошибки имеют свойство всплывать.</i>"
        ),
        attachments=[media, base_keyboard_maker(library_keyboard)],
        parse_mode=ParseMode.HTML
    )


@menu.message_created(F.message.body.text == library_keyboard["button1"], MenuStates.menu)
async def library_1(event: MessageCreated, context: MemoryContext):
    media1 = InputMedia("media/library/Лекция_1_Основы_менеджмента.pdf")
    last_message = await event.message.answer(
        text=(
            "📖 <b>Лекция 1 — Основы менеджмента</b> 🦭\n\n"
            "<i>Первая запись из архива станции посвящена управлению процессами, "
            "ресурсами и командой.</i> 🤖\n\n"
            "В этой лекции Вы узнаете:\n"
            "• <b>как принимать эффективные управленческие решения</b>;\n"
            "• <b>как правильно распределять задачи между экипажем</b>;\n"
            "• <b>как поддерживать стабильную работу станции</b> "
            "даже в сложных ситуациях. ⚙️\n\n"
            "🌊 <i>Внимание: хороший руководитель не появляется сам. "
            "Его создают знания, опыт и несколько вовремя нажатых кнопок.</i>"
        ),
        attachments=[media1],
        parse_mode=ParseMode.HTML
    )

@menu.message_created(Command("present"))
@menu.message_created(F.message.body.text == library_keyboard["button2"], MenuStates.menu)
async def library_2(event: MessageCreated, context: MemoryContext):
    ast_message = await event.message.answer(
        text=(
            "🎁 <b>Подарок от ИИ П.Л.О.М.Б.И.Р.</b> 🦭\n\n"
"<i>Оператор, для вас подготовлен специальный подарок.</i>\n\n"
"В знак благодарности за прохождение испытаний станции "
"П.Л.О.М.Б.И.Р. передаёт вам набор эксклюзивных стикеров. 🤖\n\n"
"<blockquote>🦭 <i>Используйте их в общении и помните: даже серьёзной станции "
"иногда нужен немного тюленьего настроения.</i></blockquote>\n\n📌 <i>Для возвращения в главное меню введите или нажмите /start</i>"
        ),
        parse_mode=ParseMode.HTML
    )
    await send_sticker(event.message)
