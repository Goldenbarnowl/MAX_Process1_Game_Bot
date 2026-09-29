from maxapi.types import Message, InputMedia

from functions.maxapi_patch import MediaCache

_original_answer = Message.answer


async def smart_answer(
    self,
    text=None,
    attachments=None,
    **kwargs
):
    """
       Умная обёртка над методом Message.answer().

       Автоматически заменяет InputMedia на сохранённые
       Attachment из кэша MAX API, если такое вложение уже
       было отправлено ранее.

       Если медиа отсутствует в кэше:
           1. Использует стандартный InputMedia.
           2. Отправляет файл через MAX API.
           3. Получает созданный Attachment.
           4. Сохраняет его для будущих отправок.

       Args:
           self:
               Объект Message из maxapi.

           text (str | None):
               Текст сообщения.

           attachments (list | None):
               Список вложений сообщения.
               Поддерживает InputMedia и готовые Attachment.

           **kwargs:
               Дополнительные параметры метода Message.answer().

       Returns:
           SendedMessage | None:
               Результат отправки сообщения через MAX API.

       Notes:
           Кэширование работает только для вложений,
           переданных через InputMedia.

           Уже готовые Attachment отправляются без изменений.
       """
    new_attachments = []
    input_medias = []

    if attachments:
        for attachment in attachments:

            if isinstance(attachment, InputMedia):
                path = str(attachment.path)

                cached = MediaCache.get(path)

                new_attachments.append(cached)
                input_medias.append(
                    (path, cached)
                )

            else:
                new_attachments.append(attachment)

    result = await _original_answer(
        self,
        text=text,
        attachments=new_attachments or attachments,
        **kwargs
    )

    # сохраняем только после успешной отправки
    if result and input_medias:
        try:
            for att in result.message.body.attachments:

                if att.type in (
                    "image",
                    "video",
                    "file"
                ):
                    for path, media in input_medias:

                        if isinstance(media, InputMedia):
                            MediaCache.remember(
                                path,
                                att
                            )

                            print(
                                "MEDIA SAVED:",
                                path
                            )

        except Exception as e:
            print("CACHE ERROR:", e)

    return result


def apply_patch():
    """
       Применяет monkey patch для метода Message.answer().

       После вызова функции все последующие отправки
       сообщений через Message.answer() будут автоматически
       проходить через smart_answer().
       """
    Message.answer = smart_answer
    print("MAX answer patched")
