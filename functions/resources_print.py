from maxapi.context import MemoryContext


async def print_resources(context: MemoryContext) -> str:
    """
        Формирует строку с текущими ресурсами игрока.

        Получает данные из MemoryContext и создаёт
        HTML-форматированный блок с отображением:
        бюджета, энергии и количества еды.

        Args:
            context (MemoryContext):
                Контекст пользователя с сохранённым состоянием игры.

        Returns:
            str:
                Строка с ресурсами игрока в формате HTML
                для отправки через MAX API.

        Raises:
            KeyError:
                Если в состоянии отсутствует один из необходимых
                ресурсов: finance, energy или food.

        Example:
            resources = await print_resources(context)

            await message.answer(
                text=resources,
                parse_mode=ParseMode.HTML
            )
        """
    data = await context.get_data()
    finance = data["finance"]
    energy = data["energy"]
    food = data["food"]
    output = (f"💳 <b>Бюджет:</b> {finance}%\n"
            f"⚡ <b>Энергия:</b> {energy}%\n"
            f"🥫 <b>Еда:</b> {food}%\n"
            "━━━━━━━━━━━━━━━━━━\n\n")
    return output
