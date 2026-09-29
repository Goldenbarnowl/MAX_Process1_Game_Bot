from maxapi.context import StatesGroup, State


class MenuStates(StatesGroup):
    m1 = State()
    m2 = State()
    m3 = State()

    name = State()
    menu = State()
    library = State()
