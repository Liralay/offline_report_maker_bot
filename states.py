from aiogram.dispatcher.filters.state import StatesGroup, State

class ReportStates(StatesGroup):
    waiting_for_suggestion = State()
    waiting_for_report = State()
    waiting_for_day = State()
    waiting_for_hour = State()
    getting_hour = State()
    getting_day = State()
    preparing_data = State()
    