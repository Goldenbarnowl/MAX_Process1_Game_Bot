import re

from maxapi.context import MemoryContext

# Словарь для маппинга значений в смайлы
REPUTATION_EMOJIS = {
    -2: '😡',
    -1: '☹️',
    0: '😐',
    1: '🙂',
    2: '😀'
}


async def calculate_reputation(data: dict, faction: str) -> int:
    """
        Рассчитывает репутацию игрока с указанной фракцией.

        Анализирует данные состояния игры и суммирует все
        значения, относящиеся к выбранной фракции.

        Учитываются только ключи формата:
            ch1_security
            ch2_scientist
            ch3_worker

        Итоговое значение ограничивается диапазоном
        от -2 до 2 для отображения уровня отношения фракции.

        Args:
            data (dict):
                Данные состояния игры из MemoryContext.

            faction (str):
                Название фракции для расчёта репутации.
                Например:
                    "security"
                    "scientist"
                    "worker"

        Returns:
            int:
                Значение репутации в диапазоне [-2, 2].

        Example:
            reputation = await calculate_reputation(
                data,
                "security"
            )
        """
    total = 0

    for key, value in data.items():
        # берём только ch1_scientist, ch2_security и т.п.
        if re.match(rf"^ch\d+_{faction}$", key):
            if isinstance(value, int):
                total += value

    return max(-2, min(2, total))

async def get_reputation_text(context: MemoryContext) -> str:
    """Формирует текст текущей репутации."""

    data = await context.get_data()

    security = await calculate_reputation(data, "security")
    scientist = await calculate_reputation(data, "scientist")
    worker = await calculate_reputation(data, "worker")

    return (
        f"📊 <b>Репутация с фракциями</b>\n"
        f"━━━━━━━━━━━━━━\n\n"
        f"🛡 <b>Охрана:</b> {REPUTATION_EMOJIS[security]}\n\n"
        f"🔬 <b>Учёные:</b> {REPUTATION_EMOJIS[scientist]}\n\n"
        f"👷 <b>Рабочие:</b> {REPUTATION_EMOJIS[worker]}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚖️ <i>Репутация показывает отношение фракций к вам.</i>\n"
        f"⚠️ <i>При провальных концовках репутация остаётся без изменений, а прогресс главы не сохраняется.</i>\n"
        f"📖 <i>Репутация изменяется в зависимости от решений, "
        f"принятых вами во время прохождения глав. "
        f"Каждый выбор влияет на доверие разных групп.</i>"
    )
