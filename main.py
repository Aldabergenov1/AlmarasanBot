from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from config import TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, default_state, State

bot = Bot(TOKEN)
dp = Dispatcher()


order_button1 = InlineKeyboardButton(
    text="Заказать вторую смену на обед",
    callback_data="second_term_lunch"
)

order_button2 = InlineKeyboardButton(
    text="Заказать вторую смену на ужин",
    callback_data="second_term_dinner"
)

order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[order_button1],
                     [order_button2]]
)


class OrderStates(StatesGroup):
    ordering = State()
    end_ordering = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def start(message: Message):
    await message.answer("")


@dp.message(Command(commands=["order"]), StateFilter(default_state))
async def process_order_command(message: Message, state: FSMContext):
    await message.answer(text="Выберите, когда хотите заказать вторую смену",
                         reply_markup=order_keyboard)
    await state.set_state(OrderStates.ordering)

@dp.message(StateFilter(OrderStates.ordering), F.data.in_(['second_term_lunch', 'second_term_dinner']))
async def process_order(message: Message, state: FSMContext):



if __name__ == '__main__':
    dp.run_polling(bot)