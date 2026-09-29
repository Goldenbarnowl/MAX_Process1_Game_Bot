from maxapi.types import Attachment
from maxapi.enums import AttachmentType
from maxapi.types.attachments import StickerAttachmentPayload


def create_sticker(code: str):
    """
       Создаёт объект вложения MAX API типа sticker.

       Используется для отправки готовых стикеров без загрузки
       файлов через InputMedia.

       Args:
           code (str):
               Уникальный идентификатор стикера MAX.

       Returns:
           Attachment:
               Готовое вложение стикера для передачи
               в Message.answer().

       Example:
           sticker = create_sticker("9dea321d7")

           await message.answer(
               attachments=[sticker]
           )
       """
    return Attachment(
        type=AttachmentType.STICKER,
        payload=StickerAttachmentPayload(
            code=code,
            url=f"https://i.oneme.ru/getSmile?smileId={code}&smileType=4"
        )
    )

async def send_sticker(message):
    """
       Отправляет стикер пользователю через MAX API.

       Создаёт вложение стикера и отправляет его
       через стандартный метод Message.answer().

       Args:
           message:
               Объект Message из maxapi.

       Returns:
           None:
               Функция только выполняет отправку.

       Example:
           await send_sticker(event.message)
       """
    sticker = create_sticker(
        "9dea321d7"
    )

    await message.answer(
        attachments=[
            sticker
        ]
    )
