from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from config import TOKEN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, default_state, State

bot = Bot(TOKEN)
dp = Dispatcher()



@dp.message(CommandStart(), StateFilter(default_state))
async def start(message: Message):
    await message.answer("")


#@dp.message()

