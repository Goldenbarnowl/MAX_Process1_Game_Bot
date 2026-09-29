from maxapi.context import MemoryContext


async def edit_resources(context: MemoryContext, finance_delta=0, energy_delta=0, food_delta=0) -> None:
    """
       Изменяет текущие ресурсы игрока.

       Получает текущие значения ресурсов из MemoryContext,
       применяет переданные изменения и сохраняет обновлённые
       значения обратно в контекст.

       Каждый параметр изменения имеет свой множитель:
           - бюджет изменяется на 5 единиц;
           - энергия изменяется на 10 единиц;
           - еда изменяется на 10 единиц.

       Args:
           context (MemoryContext):
               Контекст игрока с сохранёнными ресурсами.

           finance_delta (int):
               Изменение бюджета.
               Фактическое изменение:
               finance_delta * 5.

           energy_delta (int):
               Изменение энергии.
               Фактическое изменение:
               energy_delta * 10.

           food_delta (int):
               Изменение запасов еды.
               Фактическое изменение:
               food_delta * 10.

       Returns:
           None:
               Функция изменяет данные непосредственно
               внутри MemoryContext.

       Example:
           await edit_resources(
               context,
               finance_delta=2,
               energy_delta=-1,
               food_delta=3
           )
       """
    data = await context.get_data()
    finance = data["finance"]
    energy = data["energy"]
    food = data["food"]
    finance += finance_delta*5
    energy += energy_delta*10
    food += food_delta*10
    await context.update_data(finance=finance, energy=energy, food=food)
