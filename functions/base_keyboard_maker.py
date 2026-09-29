from maxapi.types import MessageButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def base_keyboard_maker(keyboard_dict: dict):
    """
       Создаёт inline-клавиатуру MAX API из словаря кнопок.

       Функция преобразует переданный словарь в разметку
       клавиатуры, добавляя каждую кнопку в отдельный ряд.

       Args:
           keyboard_dict (dict):
               Словарь кнопок, где:
                   - ключ — идентификатор или внутреннее имя кнопки;
                   - значение — текст, отображаемый пользователю.

               Пример:
                   {
                       "button1": "Начать",
                       "button2": "Выход"
                   }

       Returns:
           InlineKeyboardMarkup:
               Готовая клавиатура для передачи в attachments
               метода Message.answer().

       Example:
           keyboard = base_keyboard_maker(
               {
                   "start": "Начать игру",
                   "info": "Информация"
               }
           )

           await message.answer(
               text="Выберите действие:",
               attachments=[keyboard]
           )
       """
    builder = InlineKeyboardBuilder()
    for key, value in keyboard_dict.items():
        builder.row(MessageButton(text=value))
    return builder.as_markup()
