import json
from pathlib import Path

from maxapi.types import InputMedia, Attachment

CACHE_FILE = "media_cache.json"


class MediaCache:
    """
    Класс для управления кэшем медиа-вложений MAX API.

    Хранит соответствие между локальным путём к файлу
    и готовым объектом Attachment, полученным после
    успешной отправки через MAX API.

    Позволяет повторно отправлять медиа без повторной
    загрузки файла через InputMedia.

    Attributes:
        cache (dict):
            Словарь сохранённых медиа-вложений.
            Ключ — путь к файлу.
            Значение — сериализованный Attachment.
    """
    cache = {}

    @classmethod
    def load(cls):
        """
        Класс для управления кэшем медиа-вложений MAX API.

        Хранит соответствие между локальным путём к файлу
        и готовым объектом Attachment, полученным после
        успешной отправки через MAX API.

        Позволяет повторно отправлять медиа без повторной
        загрузки файла через InputMedia.

        Attributes:
            cache (dict):
                Словарь сохранённых медиа-вложений.
                Ключ — путь к файлу.
                Значение — сериализованный Attachment.
        """
        try:
            if Path(CACHE_FILE).exists():
                cls.cache = json.loads(
                    Path(CACHE_FILE).read_text()
                )
        except Exception:
            cls.cache = {}

    @classmethod
    def save(cls):
        """
               Сохраняет текущий кэш медиа в JSON-файл.

               Returns:
                   None
               """
        Path(CACHE_FILE).write_text(
            json.dumps(cls.cache, indent=4)
        )

    @classmethod
    def get(cls, path):
        """
                Получает медиа для отправки.

                Если вложение уже есть в кэше, возвращает
                готовый Attachment MAX API.

                Если вложение отсутствует, создаёт InputMedia
                для первой загрузки файла.

                Args:
                    path (str):
                        Путь к локальному медиафайлу.

                Returns:
                    Attachment | InputMedia:
                        Готовое вложение из кэша или объект
                        для загрузки нового файла.
                """
        if path in cls.cache:
            print("CACHE HIT:", path)

            return Attachment.model_validate(
                cls.cache[path]
            )

        print("CACHE MISS:", path)

        return InputMedia(path)

    @classmethod
    def remember(cls, path, attachment):
        """
                Получает медиа для отправки.

                Если вложение уже есть в кэше, возвращает
                готовый Attachment MAX API.

                Если вложение отсутствует, создаёт InputMedia
                для первой загрузки файла.

                Args:
                    path (str):
                        Путь к локальному медиафайлу.

                Returns:
                    Attachment | InputMedia:
                        Готовое вложение из кэша или объект
                        для загрузки нового файла.
                """
        cls.cache[path] = attachment.model_dump()
        cls.save()

MediaCache.load()
