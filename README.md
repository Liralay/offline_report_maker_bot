# Отчетмейкер
Привет! 
Это краткое описание работы бота Отчетмейкер, который поможет тебе написать отчет после ГР смены на выставке **"Панк культура. Король и шут"**
## Начало работы
1. Найди в поиске Telegram бота <a href = "https://t.me/report_maker_yandex_offline_bot"> <span style="color:red">@</span>report_maker_yandex_offline_bot</a>.
2. Напиши команду <code>/start></code>.
3. В начале смены напиши команду <code>/newday</code>.
Бот пожелает тебе удачной смены и покажет статистику по проходам за сегодняшний день. Использование кнопок:
<code>Помогли купить билет</code>,
<code>Выдали приглосительный</code> увеличивает значение соотвествующего аргумента в сообщении.
> Если слишком часто нажимать на кнопки бот может подвиснуть. Если такое случилось поможет команда <i><code>/cancel</code></i>

 4. После закрытия прохода на выставку напиши команду <code>/report</code>.
 5. Выгрузи файл полного отчета из личного кабинета в формате Excel <code>(.xlsx)</code>. 
<table style="border-radius: 12px; margin:20px; width:40%; background-color:rgba(235, 50, 38, 0.17); font-size:15px;">
<tr valign="middle" style="vertical-align: middle;">
<td style="vertical-align: middle; padding:16px; 16px 0 0px; text-align:left;"> 
Обязательные поля:<br>
<li> Дата и время собятия
<li>ШК
<li>Сумма продажи
<li>Статус СКД билета
<li>Дата, время подажи
<li>Дата, время возврата
<li>Сканер
<li>Время сканирования
</td>
</tr></table>
6. Отправь файл боту, а после загрузки нажми <code>Давай мне скорее данные</code>

7. Выбери день 

> Месяц по умолчанию стоит текущий.
 То есть, если ты делаешь отчет в апреле, то отчет за март сделать не получится

8.<empty> Выбери время первого прохода

## Полный список команд
<ul>
<li> <code>/start</code> - начало работы бота. Приветственное сообщение
<li> <code>/newday</code> – Создание сообщения-счетчика. Обнуление прошлого счетчика 
<li> <code>/cancel</code> - Обнуление машины состояний. Переход из любого контекста программы в начало
<li> <code>/suggest</code> – Отправить привет или пожелание создателю бота 
</ul>
##Список извесных ошибок
<li> Иногда бот перестает работать. Поиск причин ведется. 

Если такое случилось, пингани, пожалуйста, <a href="https://t.me/liralay"> мне в личку.</a>
