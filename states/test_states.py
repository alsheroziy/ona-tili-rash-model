from aiogram.fsm.state import State, StatesGroup


class TestStates(StatesGroup):
    choosing_test = State()
    answering_1_32 = State()
    answering_33_35 = State()
    answering_36_39 = State()
    answering_40_44_a = State()
    answering_40_44_b = State()
    finished = State()


class AdminTestStates(StatesGroup):
    waiting_test_name = State()
    answering_1_32 = State()
    answering_33_35 = State()
    answering_36_39 = State()
    answering_40_44_a = State()
    answering_40_44_b = State()
    finished = State()
