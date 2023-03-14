from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

update_report_btn = InlineKeyboardButton("Загрузить новый отчет", callback_data="update_report")
get_report_data_btn = InlineKeyboardButton("Давай мне скорее данные", callback_data="get_data")
set_day_today_btn = InlineKeyboardButton("Сегодня", callback_data="set_day_today")
set_different_day_btn = InlineKeyboardButton("Выбрать другой день", callback_data = "set_different_day")
stop_getting_report_btn = InlineKeyboardButton("Отменить", callback_data="stop_getting_report")
weekday_first_scan_btn = InlineKeyboardButton("В 12 часов дня", callback_data="weekday_scan")
weekend_first_scan_btn = InlineKeyboardButton("В 11 часов дня", callback_data="weekend_scan")
other_first_scan_btn = InlineKeyboardButton("В другое время", callback_data="other_scan")
here_we_go_again_btn = InlineKeyboardButton("Выгрузить новый отчет", callback_data="update_report")
new_day_new_report_btn = InlineKeyboardButton("Начать новый день", callback_data="start_new_day")

inline_kb1 = InlineKeyboardMarkup(row_width = 1)
inline_kb1.add(update_report_btn).add(get_report_data_btn)

inline_kb2 = InlineKeyboardMarkup(row_width = 1)
inline_kb2.add(get_report_data_btn)

inline_kb3 = InlineKeyboardMarkup(row_width = 1)
inline_kb3.add(set_day_today_btn).add(set_different_day_btn)

inline_kb4 = InlineKeyboardMarkup(row_width = 1)
inline_kb4.add(stop_getting_report_btn)

inline_kb5 = InlineKeyboardMarkup(row_width=2)
inline_kb5.add(weekday_first_scan_btn).insert(weekend_first_scan_btn).add(other_first_scan_btn)

inline_kb6 = InlineKeyboardMarkup(row_width=1)
inline_kb6.add(here_we_go_again_btn).add(new_day_new_report_btn)

###

helped_btn = InlineKeyboardButton("Помогли купить билет", callback_data="helped+1")
gifted_tickets_btn = InlineKeyboardButton("Выдали приглосительный", callback_data="gifted_tickets+1")
people_left_btn = InlineKeyboardButton("Ушли, не стали покупать билет", callback_data="people_left+1")

counter = InlineKeyboardMarkup(row_width=1)
counter.add(helped_btn).insert(gifted_tickets_btn).insert(people_left_btn)
