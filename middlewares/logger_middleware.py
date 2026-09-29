from typing import Callable, Any, Dict, Awaitable

from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion, MessageCreated

from logger import log_user_action


class BotMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event_object: UpdateUnion,
        data: Dict[str, Any],
    ) -> Any:

        user = getattr(
            event_object,
            "from_user",
            None
        )

        user_id = None

        if user:
            user_id = user.user_id


        # Данные для роутеров
        data["custom_data"] = {
            "user_id": user_id,
            "event": type(event_object).__name__,
        }


        # Данные для логирования
        log_data = {
            "chat_id": None,
            "text": None,
            "attachments": [],
        }


        if isinstance(event_object, MessageCreated):

            message = getattr(
                event_object,
                "message",
                None
            )

            if message:

                log_data["chat_id"] = (
                    message.recipient.chat_id
                )

                body = getattr(
                    message,
                    "body",
                    None
                )

                if body:

                    if body.text:
                        log_data["text"] = (
                            body.text[:500]
                        )


                    for attachment in body.attachments:
                        log_data["attachments"].append(
                            {
                                "type": attachment.type
                            }
                        )


        # Запись лога
        if user_id:

            log_user_action(
                user_id=user_id,
                action=type(event_object).__name__,
                **log_data
            )


        return await handler(
            event_object,
            data
        )