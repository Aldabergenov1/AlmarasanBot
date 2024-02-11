from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.exceptions import TelegramBadRequest
from config import TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, default_state, State
from datetime import timezone, timedelta
from menu_setter import set_main_menu
from keyboards import order_keyboard, language_keyboard, days_of_week_keyboard, days_dict


bot = Bot(TOKEN)
dp = Dispatcher()

order_dict: dict[int, dict] = {}
container_dict: dict[int, dict] = {}
selected_days = []

almaty_timezone = timezone(timedelta(hours=6))


class OrderStates(StatesGroup):
    ordering = State()


class ContainerStates(StatesGroup):
    container = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    if message.from_user.id not in order_dict:
        await message.answer(text="Я бот, организовывающий заказы второй смены и контейнеров в культурном центре Алмарасан!"
          "Для получения помощи по использованию пропиши /help")


@dp.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer("/order - Заказ второй смены на обед или ужин\n"
                         "/container - Заказ контейнера с собой\n"
                         "/delete_order - Отменить заказ второй смены на обед или ужин!!!\n"
                         "/delete_container - Отменить заказ контейнера с собой")


@dp.message(Command(commands=["delete_order"]))
async def process_delete_order(message: Message):
    order_dict[message.from_user.id].pop("nickname")
    order_dict[message.from_user.id].pop("ordder_term")
    order_dict[message.from_user.id].pop("order_date")


@dp.message(Command(commands=["list_second_term"]), StateFilter(default_state))
async def process_list_command(message: Message):
    try:
        for user_id in order_dict:
            nickname = order_dict[user_id]["nickname"]

            if order_dict[user_id]["order_term"] == "lunch":
                term = "Обед"
            elif order_dict[user_id]["order_term"] == "dinner":
                term = "Ужин"
            else:
                term = "Нет"

            date = order_dict[user_id]["order_date"]

            await message.answer(f"Никнейм: {nickname}\n"
                                 f"Вторая смена: {term}\n"
                                 f"Дата заказа второй смены: {date[-2]}:{date[-1]}, {date[2]}.{date[1]}.{date[0]}\n")

    except:
        await message.answer("Нет никого на вторую смену!")


@dp.message(Command(commands=["list_containers"]), StateFilter(default_state))
async def process_list_containers(message: Message):
    try:
        for user_id in container_dict:
            nickname = container_dict[user_id]["nickname"]
            await message.answer(f"Никнейм: {nickname}"
                                 f"Контейнеры: {[days_dict[day] for day in selected_days]}")

    except Exception as e:
        print(e)
        await message.answer("Никто контейнеры не заказывал!")


@dp.message(Command(commands=["order"]), StateFilter(default_state))
async def process_order_command(message: Message, state: FSMContext):
    order_dict.setdefault(message.from_user.id, {})
    await message.answer(text="Выберите, когда хотите заказать вторую смену",
                         reply_markup=order_keyboard)
    await state.set_state(OrderStates.ordering)


@dp.callback_query(StateFilter(OrderStates.ordering), F.data.in_(["dinner"]))
async def process_dinner_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    if callback.message.date.astimezone(almaty_timezone).hour < 20:
        order_dict[callback.from_user.id].update({
            "nickname": callback.from_user.username,
            "order_term": "dinner",
            "order_date": (callback.message.date.astimezone(almaty_timezone).year,
                           callback.message.date.astimezone(almaty_timezone).month,
                           callback.message.date.astimezone(almaty_timezone).day,
                           callback.message.date.astimezone(almaty_timezone).hour,
                           callback.message.date.astimezone(almaty_timezone).minute),
        })
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

    if callback.message.date.astimezone(almaty_timezone).hour < 13:
        order_dict[callback.from_user.id].update({
            "nickname": callback.from_user.username,
            "order_term": "lunch",
            "order_date": (callback.message.date.astimezone(almaty_timezone).year,
                           callback.message.date.astimezone(almaty_timezone).month,
                           callback.message.date.astimezone(almaty_timezone).day,
                           callback.message.date.astimezone(almaty_timezone).hour,
                           callback.message.date.astimezone(almaty_timezone).minute),
        })
        await state.set_state(default_state)

        await bot.send_message(text="Успешно записано!",
                               chat_id=callback.message.chat.id)

    else:
        await bot.send_message(text="Невозможно заказать на указанное время",
                               chat_id=callback.message.chat.id)
        await state.set_state(default_state)


@dp.message(StateFilter(OrderStates.ordering))
async def process_wrong_callback(callback: CallbackQuery):
    await callback.answer(text="Пожалуйста, выберите из предложенных вариантов!",
                          reply_markup=order_keyboard)


@dp.message(Command(commands=["container"]), StateFilter(default_state))  # Как сделать контейнер на один день???
async def process_container_command(message: Message, state: FSMContext):
    container_dict.setdefault(message.from_user.id, {})
    await message.reply(text="Выберите дни недели:",
                        reply_markup=days_of_week_keyboard)

    await state.set_state(ContainerStates.container)


@dp.callback_query(StateFilter(ContainerStates.container))
async def process_container_choosing(callback: CallbackQuery, state: FSMContext):
    markup = callback.message.reply_markup

    if callback.data == "quit":
        await callback.answer("Выбор дней завершен.")

        container_dict[callback.from_user.id].update({
            "nickname": callback.from_user.username,
            "days": selected_days
        })
        print(container_dict[callback.from_user.id])
        await callback.message.delete()

        await state.set_state(default_state)

    markup = callback.message.reply_markup

    for row in markup.inline_keyboard:
        for button in row:
            if button.callback_data == callback.data:
                if button.text.endswith("❌") and callback.data not in selected_days:
                    button.text = button.text.replace("❌", "✅")
                    selected_days.append(callback.data)
                    print(selected_days)
                elif button.text.endswith("✅") and callback.data in selected_days:
                    button.text = button.text.replace("✅", "❌")
                    selected_days.remove(callback.data)
                    print(selected_days)

    try:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            reply_markup=markup)
    except TelegramBadRequest:
        pass


if __name__ == '__main__':
    dp.run_polling(bot)
