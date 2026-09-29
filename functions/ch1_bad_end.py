from maxapi.enums import ParseMode
from maxapi.types import InputMedia

from functions.base_keyboard_maker import base_keyboard_maker
from states.chapter1_states import Chapter1States

bad_end_buttons = {"button1":"→"}
async def check_bad_end(event_object, context):
    """
       Проверяет наличие условий для плохой концовки игры.

       Функция анализирует текущие ресурсы игрока.
       Если один из критических ресурсов достигает нуля,
       отправляется соответствующая сцена окончания игры,
       меняется состояние главы и прохождение завершается.

       Проверяемые условия:
           - отсутствие еды;
           - отсутствие энергии.

       Args:
           event_object:
               Объект события MAX API, содержащий сообщение
               пользователя.

           context (MemoryContext):
               Контекст пользователя с сохранённым прогрессом
               игры.

       Returns:
           bool:
               True, если была активирована плохая концовка.
               False, если игра продолжается.

       Notes:
           Проверка выполняется только после начала игры.
           Если в данных пользователя отсутствует ключ
           "food", функция завершает работу без изменений.

       Example:
           is_end = await check_bad_end(
               event_object,
               context
           )

           if is_end:
               return
       """
    user_data = await context.get_data()

    # Игра ещё не началась
    if "food" not in user_data:
        return False

    if user_data["food"] <= 0:

        media = InputMedia("media/chapter1/no_food.png")

        await event_object.message.answer(
            text=
            "<b>Конец игры</b> 🌊\n\n"
            "Станция работает, экипаж в порядке, "
            "но еда закончилась... 😅\n\n"
            "Оператор заявил:\n"
            "<i>«Паники нет, я всё рассчитал».</i>\n\n"
            "Через минуту выяснилось, что он рассчитал "
            "только количество дней до последней пачки печенья. 🍪😂\n\n"
            "<b>Оператор уволен.</b> 👋\n"
            "<i>Новая должность: человек, который больше "
            "не отвечает за подсчёт запасов.</i>",
            attachments=[media,base_keyboard_maker(bad_end_buttons)],
            parse_mode=ParseMode.HTML
        )

        await context.set_state(Chapter1States.bad_end)
        return True


    if user_data["energy"] <= 0:

        media = InputMedia("media/chapter1/no_energy.png")

        await event_object.message.answer(
            text=
            "<b>Конец игры</b> ⚛️🌊\n\n"
            "Реактор станции остановился. 🔋\n\n"
            "Оператор сообщил:\n"
            "<i>«Не переживайте, я всё контролирую».</i>\n\n"
            "Проверка показала:\n"
            "Он контролировал только кнопку выключения. 😅\n\n"
            "<b>Реактор цел.</b> ✅\n"
            "<b>Станция цела.</b> ✅\n"
            "<b>Оператор больше не работает.</b> 👋😂",
            attachments=[media,base_keyboard_maker(bad_end_buttons)],
            parse_mode=ParseMode.HTML
        )

        await context.set_state(Chapter1States.bad_end)
        return True

    return False
