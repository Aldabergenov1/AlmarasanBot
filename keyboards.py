from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

russian_button = InlineKeyboardButton(
    text="Выбрать русский язык 🇷🇺",
    callback_data="lang_rus"
)

espanol_button = InlineKeyboardButton(
    text="Seleccionar el idioma español 🇪🇸",
    callback_data="lang_esp"
)

english_button = InlineKeyboardButton(
    text="Choose english language 🇬🇧",
    callback_data="lang_eng"
)

language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[russian_button],
                     [espanol_button],
                     [english_button]]
)

order_button1 = InlineKeyboardButton(
    text="Заказать вторую смену на обед",
    callback_data="lunch"
)

order_button2 = InlineKeyboardButton(
    text="Заказать вторую смену на ужин",
    callback_data="dinner"
)

order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[order_button1],
                     [order_button2]]
)

days_dict = {'mon': 'Понедельник', 'tue': 'Вторник',
             'wed': 'Среда', 'thu': 'Четверг',
             'fri': 'Пятница', 'sat': 'Суббота', 'sun': 'Воскресенье'}


mon_button = InlineKeyboardButton(
    text="Понедельник ❌",
    callback_data="mon"
)
tue_button = InlineKeyboardButton(
    text="Вторник ❌",
    callback_data="tue"
)
wed_button = InlineKeyboardButton(
    text="Среда ❌",
    callback_data="wed"
)
thu_button = InlineKeyboardButton(
    text="Четверг ❌",
    callback_data="thu"
)
fri_button = InlineKeyboardButton(
    text="Пятница ❌",
    callback_data="fri"
)
sat_button = InlineKeyboardButton(
    text="Суббота ❌",
    callback_data="sat"
)
sun_button = InlineKeyboardButton(
    text="Воскресенье ❌",
    callback_data="sun"
)
quit_button = InlineKeyboardButton(
    text="Завершить выбор",
    callback_data="quit"
)

days_of_week_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [mon_button], [tue_button], [wed_button],
    [thu_button], [fri_button], [sat_button],
    [sun_button], [quit_button]
])


menu_order_button = InlineKeyboardButton(
    text="Заказать вторую смену на обед или ужин",
    callback_data="/order"
)

menu_container_button = InlineKeyboardButton(
    text="Заказать контейнер",
    callback_data="/container"
)

menu_list_button = InlineKeyboardButton(
    text="Показать всех кто заказал",
    callback_data="/list"
)

# menu = ReplyKeyboardMarkup(inline_keyboard=)
