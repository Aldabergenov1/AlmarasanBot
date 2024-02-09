from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from config import TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, default_state, State
from datetime import datetime, timezone, timedelta
from collections import defaultdict


bot = Bot(TOKEN)
dp = Dispatcher()

user_dict: dict[int, dict] = {}

almaty_timezone = timezone(timedelta(hours=6))

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


class OrderStates(StatesGroup):
    ordering = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer("Я бот, организовывающий заказы второй смены и контейнеров в культурном центре Алмарасан!"
                         "Для получения помощи по использованию пропиши /help")


@dp.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer("/order - Заказ второй смены на обед или ужин"
                         "/container - Заказ контейнера с собой"
                         "/delete_order - Отменить заказ второй смены на обед или ужин"
                         "/delete_container - Отменить заказ контейнера с собой")


@dp.message(Command(commands=["list"]), StateFilter(default_state))
async def process_list_command(message: Message):
    merged_dict = defaultdict(dict)
    for key, value in user_dict.items():
        merged_dict[key].update(value)

    formatted_strings = [
        f"{idx})\n" + '\n'.join([f"    {key}: {value}" for key, value in entry.items()])
        for idx, entry in enumerate(merged_dict.values(), start=1)
    ]

    for string in formatted_strings:
        print(string)
    await message.answer(f"{user_dict}")


@dp.message(Command(commands=["order"]), StateFilter(default_state))
async def process_order_command(message: Message, state: FSMContext):
    await message.answer(text="Выберите, когда хотите заказать вторую смену",
                         reply_markup=order_keyboard)
    await state.set_state(OrderStates.ordering)


@dp.callback_query(StateFilter(OrderStates.ordering), F.data.in_(["dinner"]))
async def process_dinner_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    print(callback.message.date.astimezone(almaty_timezone).hour)

    if callback.message.date.astimezone(almaty_timezone).hour < 20:
        user_dict[callback.from_user.id] = {
            "nickname": callback.from_user.username,
            "order_term": "dinner",
            "order_date": (callback.message.date.year, callback.message.date.month,
                           callback.message.date.hour, callback.message.date.minute)
        }
        print(user_dict)
        await state.set_state(default_state)

        await bot.send_message(text="Успешно записано!",
                               chat_id=callback.message.chat.id)

    else:
        await bot.send_message(text="Невозможно заказать на указанное время",
                               chat_id=callback.message.chat.id)
        await state.set_state(default_state)


@dp.callback_query(StateFilter(OrderStates.ordering), F.data.in_(["lunch"]))
async def process_lunch_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    print(callback.message.date.astimezone(almaty_timezone).hour)

    if callback.message.date.astimezone(almaty_timezone).hour < 13:
        user_dict[callback.from_user.id] = {
            "nickname": callback.from_user.username,
            "order_term": "lunch",
            "order_date": (callback.message.date.year, callback.message.date.month,
                           callback.message.date.hour, callback.message.date.minute)
        }
        print(user_dict)
        await state.set_state(default_state)

        await bot.send_message(text="Успешно записано!",
                               chat_id=callback.message.chat.id)

    else:
        await bot.send_message(text="Невозможно заказать на указанное время",
                               chat_id=callback.message.chat.id)
        await state.set_state(default_state)


@dp.message(StateFilter(OrderStates.ordering))
async def process_wrong_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text="Пожалуйста, выберите из предложенных вариантов!",
                          reply_markup=order_keyboard)


if __name__ == '__main__':
    dp.run_polling(bot)
