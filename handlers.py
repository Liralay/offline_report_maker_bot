import os
from aiogram import types
from aiogram.dispatcher import FSMContext
import pandas as pd
from datetime import datetime
import keyboards as nav

from main import dp, bot
from config import admin_id
from states import ReportStates

helped = 0
gifted_tickets = 0
people_left = 0
today_is =  datetime.now().strftime("%d/%m")
main_message_text = f"Удачной смены!\n\nСегодня({today_is}):\n\
1) Помогли купить билет: {helped} раз(а)\n\
2) Выдали {gifted_tickets} приглосительных(ый)\n\
3) {people_left} людей ушли и не стали покупать билет"

@dp.message_handler(commands=["start"], state = "*")
async def start(message: types.Message):
    await message.answer("Привет. Я помогу тебе заполнить табличку с отчетом на событии 'Панк-культура. Король и Шут'. \n\n\
Список моих команд можно посмотреть в меню - синей кнопочке рядом с нашим чатом ☺️")

file = None

@dp.message_handler(commands=['suggest'], state="*")
async def suggest_idea(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Если у тебя есть идея для функционала этого бота или ты просто хочешь передать привет -- напиши сообщение ниже:\n\n/cancel для отмены")
    await ReportStates.waiting_for_suggestion.set()

@dp.message_handler(state=ReportStates.waiting_for_suggestion)
async def listening_to_you(message: types.Message, state: FSMContext):
    message_text = message.text
    if message_text != "/cancel":
        await bot.send_message(chat_id = admin_id, text = message_text)
        await state.reset_state()
        await message.reply("Спасибо. Отправил сообщение админу")
    else:
        await state.finish()
        await message.answer("Отменено")


@dp.message_handler(commands=["cancel"], state="*")
async def kill_process(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отменено")



@dp.message_handler(commands=['newday'], state="*")
async def new_day(message: types.Message):
    global helped
    global gifted_tickets
    global people_left
    global main_message_id
    helped = 0
    gifted_tickets = 0
    people_left = 0
    await bot.send_message(chat_id=message.from_user.id, text=main_message_text, reply_markup = nav.counter)
    try:
        main_message_id = message.message_id + 1
    except:
        pass


@dp.message_handler(commands=['report'], state = "*")
async def get_report_handler(message: types.Message):
    if file is None:
        await bot.send_message(chat_id = message.from_user.id, text = "Пожалуйста, отправьте файл для отчета.", reply_markup=nav.inline_kb4)
        await ReportStates.waiting_for_report.set()
    else:
        await bot.send_message(chat_id = message.from_user.id, text= f"Дата отправки последней версии отчета: {created}.", reply_markup = nav.inline_kb1)

@dp.message_handler(content_types = types.ContentTypes.DOCUMENT, state = ReportStates.waiting_for_report)
async def process_report(message: types.Message, state: FSMContext):
    global created
    if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path 
        await bot.download_file(file_path, "report.xlsx")
        dt =  datetime.now()
        created = dt.strftime("%d/%m %H:%M")
        await bot.send_message(chat_id = message.from_user.id, text= f"Файл получен и сохранен в {file_path}", reply_markup = nav.inline_kb2)
        await state.finish()
    else:
        await bot.send_message(chat_id = message.from_user.id, text= "Ошибка: пожалуйста, отправьте файл.", reply_markup=nav.inline_kb4)

@dp.message_handler(content_types = types.ContentTypes.TEXT, state = None)
async def process_report_error(message: types.Message):
    await bot.send_message(chat_id = message.from_user.id, text= "Я бы очень хотел тебя понять, но я пока слишком глупенький.\n\
Можешь пообщаться с моим старшим братом <a href=\"chat.openai.com\">ChatGPT</a>")

@dp.message_handler(state = ReportStates.getting_hour)
async def different_time (message: types.Message):
    global hour
    hour = message.text
    if hour is int:
        if int(hour)//10 == 0:
            hour = int(("0" + str(hour)))
        await ReportStates.preparing_data.set()
    else:
        await message.answer("Отправьте только число.\nНапример: 12")

@dp.message_handler(state=ReportStates.getting_day)
async def different_day(message: types.Message):
    global day
    global month
    month = datetime.now().strftime("%m")
    day = message.text
    try:
        if int(day)//10 == 0:
            day = int(("0" + str(day)))
    except Exception as e:
        await message.answer("Отправьте только число.\nНапример: 12", e)
    

    await bot.send_message(chat_id=message.from_user.id, text="В каком часу был первый проход?\n\n\
<i>Обычно выставка открывается в 12 в будни и в 11 в выходные и праздники</i>", reply_markup=nav.inline_kb5)
    
    

@dp.message_handler(state = ReportStates.preparing_data)
async def preparing_final_data (message: types.Message):

    global file
    first_scan = f"2023-{int(month)}-{int(day)} {hour}:00:00+03"
    end_of_the_day = f'2023-{int(month)}-{int(day)} 22:00:00+03'

    await bot.edit_message_text("Думаю...", message.from_user.id, message.message.message_id)

    df = pd.read_excel("report.xlsx")
    df['Время сканирования'] = pd.to_datetime(df['Время сканирования'], format='%Y-%m-%d %H:%M:%S+03', errors='coerce')
    df =  df[df['Время сканирования'] >=  pd.to_datetime(first_scan, format='%Y-%m-%d %H:%M:%S+03')]
    df =  df[df['Время сканирования'] <=  pd.to_datetime(end_of_the_day, format='%Y-%m-%d %H:%M:%S+03')]
    df =  df[df['Статус СКД билета'] == 'Внутри']
    df =  df[df['Дата/время возврата'].isna()]
    free_tickets =  (df['Сумма продажи'] == 0).sum()

    if '31.05.2023 22:00:00' in df['Дата/время события'].values:
        count = ((df['Дата/время события'] == '31.05.2023 22:00:00')).sum()
    else:
        count = 0
    num_rows = df.shape[0]
    await bot.delete_message(message.from_user.id,message.message.message_id)
    await bot.send_message(chat_id = message.from_user.id, text=f"Готово! Вот твой отчет:\n\nПроходов по бесплатным билетам: \
<code>{free_tickets}</code>\nКоличество проходов по билетам пресейла: <code>{count - free_tickets}\
</code>\nВсего проходов за сегодня: <code>{num_rows}</code>\n\
Помогли купить билет: <code>{helped}</code>\n\
Выдали приглосительных: <code>{gifted_tickets}</code>\n\
Людей ушли, не стали покупать билет: <code>{people_left}</code>", reply_markup=nav.inline_kb6)
    file_path = os.path.join(os.path.dirname(__file__), "report.xlsx")
    os.remove(file_path)


@dp.callback_query_handler(text = "update_report", state = "*")
async def got_wrong_report(message: types.Message, state: FSMContext):
    global file
    file = None
    await get_report_handler(message)


@dp.callback_query_handler(text = "start_new_day", state = "*")
async def start_new_day(message: types.Message):
    await new_day(message)

@dp.callback_query_handler(text = "get_data", state = "*")
async def getting_data_from_file (message: types.Message):
    await bot.delete_message(message.from_user.id,message.message.message_id)
    await bot.send_message(chat_id = message.from_user.id, text= "За какой день нужен отчет?", reply_markup = nav.inline_kb3)

@dp.callback_query_handler(text = "set_day_today", state = "*")
async def today_data (message: types.Message):
    global day
    global month
    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%m")
    await bot.send_message(chat_id=message.from_user.id, text="В каком часу был первый проход?\n\n\
<i>Обычно выставка открывается в 12 в будни и в 11 в выходные и праздники</i>", reply_markup=nav.inline_kb5)

@dp.callback_query_handler(text = "weekend_scan", state = "*")
async def weekend_scan_f (message: types.Message):
    global hour
    hour = 11
    await preparing_final_data(message)

@dp.callback_query_handler(text = "other_scan", state = "*")
async def other_scan_f (message: types.Message):
    global hour
    await bot.send_message(chat_id = message.from_user.id, text = "Напишите, во сколько часов сегодня было произведено первое сканирование")
    await preparing_final_data(message)

@dp.callback_query_handler(text = "weekday_scan", state = "*")
async def weekday_scan_f (message: types.Message):
    global hour
    hour = 12
    await preparing_final_data(message)
    

@dp.callback_query_handler(text = "set_different_day", state = "*")
async def set_day (message: types.Message):
    await bot.delete_message(message.from_user.id,message.message.message_id)
    await bot.send_message(chat_id = message.from_user.id, text = "Введите день, за который хотите получить отчет.")
    await ReportStates.getting_day.set()

@dp.callback_query_handler(text = "stop_getting_report", state = ReportStates.waiting_for_report)
async def cancel_process_report_f(message : types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id,message.message.message_id)
    await state.finish()
    await message.answer(message.from_user.id)
    await bot.send_message(chat_id = message.from_user.id, text = "Отменено")

@dp.callback_query_handler(text = "helped+1")
async def helped_1(message : types.Message):
    global helped
    helped += 1
    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=main_message_id, text=f"Удачной смены!\n\nСегодня({today_is}):\n\
1) Помогли купить билет: {helped} раз(а)\n\
2) Выдали {gifted_tickets} приглосительных(ый)\n\
3) {people_left} людей ушли и не стали покупать билет", reply_markup=nav.counter)@dp.callback_query_handler(text = "gifted_tickets+1")
    except:
        pass
@dp.callback_query_handler(text = "gifted_tickets+1")    
async def gift_1(message : types.Message):
    global gifted_tickets
    gifted_tickets += 1
    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=main_message_id, text=f"Удачной смены!\n\nСегодня({today_is}):\n\
1) Помогли купить билет: {helped} раз(а)\n\
2) Выдали {gifted_tickets} приглосительных(ый)\n\
3) {people_left} людей ушли и не стали покупать билет", reply_markup=nav.counter)
    except:
        pass
    
@dp.callback_query_handler(text = "people_left+1")
async def left_1(message: types.Message):
    global people_left
    people_left += 1
    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=main_message_id, text=f"Удачной смены!\n\nСегодня({today_is}):\n\
1) Помогли купить билет: {helped} раз(а)\n\
2) Выдали {gifted_tickets} приглосительных(ый)\n\
3) {people_left} людей ушли и не стали покупать билет", reply_markup=nav.counter)
    except:
        pass
