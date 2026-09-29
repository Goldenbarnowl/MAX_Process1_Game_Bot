from maxapi import Router
from maxapi.context import MemoryContext
from maxapi.enums import ParseMode
from maxapi.filters.command import Command
from maxapi.types import MessageCreated

last_stand = Router()

@last_stand.message_created(Command("help"))
async def help_func(event: MessageCreated, context: MemoryContext):
    last_message = await event.message.answer(
        text="📚 <b>Справка по боту</b> 🤖\n\n"
"<i>Этот бот создан для обучения и проверки ваших знаний.</i>\n\n"
"📖 В разделе <b>«Учебные материалы»</b> вы можете изучать лекции, "
"получать новые знания и знакомиться с полезной информацией.\n\n"
"🎮 В разделе с уровнями вы можете пройти игровые испытания, "
"проверить свои знания и применить полученную информацию на практике.\n\n"
"📩 Если у вас есть предложения, вопросы или замечания, "
"форма обратной связи находится в конце раздела <b>«О нас»</b>.\n\n"
"⚙️ <b>Доступные команды:</b>\n\n"
"🔹 <code>/start</code> — открыть главное меню\n"
"🔹 <code>/help</code> — показать справку по боту\n"
"🔹 <code>/edit_name</code> — изменить имя пользователя\n\n"
"<i>Изучайте материалы, проходите уровни и развивайте свои знания вместе с ботом.</i> 🚀",
        parse_mode=ParseMode.HTML,
    )

@last_stand.message_created()
async def last_stand_router(event: MessageCreated, context: MemoryContext):
    """
       Обрабатывает сообщения, которые не были распознаны
       другими обработчиками.

       Отправляет пользователю сообщение-заглушку
       о возникших помехах.

       Используется как последний обработчик цепочки
       для случаев, когда входящее сообщение не подходит
       ни под один сценарий игры.

    """

    last_message = await event.message.answer(
        text="*Сообщение не распознано, помехи*",
    )
