from maxapi.context import MemoryContext
from maxapi.types import (
    ButtonsPayload,
    MessageButton, ChatButton, OpenAppButton,
)
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

kb_menu1_dict = {"button1" : "Хорошо!"}
def kb_menu1():
    buttons = [
        [
            MessageButton(text=kb_menu1_dict["button1"]),
        ]
    ]

    return ButtonsPayload(
        buttons=buttons
    ).pack()

kb_menu2_dict = {"button1" : "Привет. Почему ты мультяшный тюлень?"}
def kb_menu2():
    buttons = [
        [
            MessageButton(text=kb_menu2_dict["button1"]),
        ]
    ]

    return ButtonsPayload(
        buttons=buttons
    ).pack()

kb_menu3_dict = {"button1" : "И чем же ты занимаешься?", "button2": "Кто первый надел, тот капитан, да?"}
def kb_menu3():
    builder = InlineKeyboardBuilder()
    builder.row(
        MessageButton(text=kb_menu3_dict["button1"]))
    builder.row(
        MessageButton(text=kb_menu3_dict["button2"]))

    return builder.as_markup()

kb_menu5_dict = {"button1" : "Ничего страшного"}
def kb_menu5():
    buttons = [
        [
            MessageButton(text=kb_menu5_dict["button1"]),
        ]
    ]

    return ButtonsPayload(
        buttons=buttons
    ).pack()

kb_menu6_dict = {
    "button1_1": "📘 Глава 1. Менеджмент",
    "button1_2": "🧩 Глава 2. Диаграммы EPC 🏗️",
    "button2": "📚 Учебные материалы",
    "button3": "👥 О нас",
    "button4": "⭐ Репутация с фракциями"
}
async def kb_menu6(context: MemoryContext):
    builder = InlineKeyboardBuilder()
    data = await context.get_data()
    if "ch1_scientist" in data.keys():
        mark1 = " ✅"
    else:
        mark1 = ""
    builder.row(
        MessageButton(text=kb_menu6_dict["button1_1"]+mark1))
    builder.row(
        MessageButton(text=kb_menu6_dict["button2"]))
    builder.row(
    OpenAppButton(
        text=kb_menu6_dict["button3"],
        web_app="https://deep-process.bitrix24site.ru",
        contact_id=202564904
    )
    )
    builder.row(
        MessageButton(text=kb_menu6_dict["button4"])
    )

    return builder.as_markup()