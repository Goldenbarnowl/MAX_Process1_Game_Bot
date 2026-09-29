from maxapi.context import MemoryContext


async def remove_keyboard(last_message, media, context: MemoryContext):
    """
        Удаляет клавиатуру у предыдущего сообщения и сохраняет
        текущее сообщение с медиа в контексте пользователя.

        Функция используется для обновления состояния интерфейса:
        старое сообщение редактируется без кнопок, после чего
        новое сообщение и его медиа сохраняются для дальнейшего
        управления.

        Args:
            last_message:
                Новое сообщение, которое необходимо сохранить
                как активное.

            media:
                Медиа-вложение текущего сообщения.

            context (MemoryContext):
                Контекст пользователя с сохранёнными данными игры.

        Returns:
            None:
                Функция выполняет редактирование сообщения
                и обновление данных контекста.

        Notes:
            Если в контексте отсутствует предыдущее сообщение
            или медиа, редактирование может завершиться ошибкой.
            Обновление текущих данных выполняется всегда
            благодаря блоку finally.

        Example:
            await remove_keyboard(
                last_message,
                media,
                context
            )
        """
    try:
        data = await context.get_data()
        last_message_edit = data.get("last_message")
        last_media = data.get("last_media")
        await last_message_edit.message.edit(
            attachments=[last_media]
        )
    finally:
        await context.update_data(last_message=last_message)
        await context.update_data(last_media=media)
