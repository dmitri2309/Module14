from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from crud_functions import *
import asyncio

api = "7697838146:AAH9LHvUAwq5eQSdHBSah8hp8RApuuu1mkw"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kbt = ReplyKeyboardMarkup(resize_keyboard=True)
btn3 = KeyboardButton(text="Рассчитать")
btn4 = KeyboardButton(text="Информация")
btn5 = KeyboardButton(text="Купить")
btn6 = KeyboardButton(text="Регистрация")
kbt.row(btn3, btn4)
kbt.add(btn5)
kbt.add(btn6)

kb = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
btn2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(btn1, btn2)

product_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Продукт 1", callback_data='buying'),
         InlineKeyboardButton(text="Продукт 2", callback_data='buying'),
         InlineKeyboardButton(text="Продукт 3", callback_data='buying'),
         InlineKeyboardButton(text="Продукт 4", callback_data='buying')]
    ], resize_keyboard=True
)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


#@dp.callback_query_handler(text="Регистрация")
@dp.message_handler(text="Регистрация")
async def sign_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


#@dp.callback_query_handler(state=RegistrationState.username)
@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    users = get_all_users()
    for user in users:
        if user[1] in message.text:
            await message.answer('Пользователь существует, введите другое имя')
            await RegistrationState.username.set()
            break
    await state.update_data(username=message.text)
    await message.answer("Введите свой email")
    await RegistrationState.email.set()
        # await message.answer('Пользователь существует, введите другое имя')
        # await RegistrationState.username.set()


#@dp.callback_query_handler(state=RegistrationState.email)
@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст")
    await RegistrationState.age.set()


#@dp.callback_query_handler(state=RegistrationState.age)
@dp.message_handler(state=RegistrationState.age)
async def set_email(message, state):
    await state.update_data(age=message.text)
    add_users(RegistrationState.username, RegistrationState.email, RegistrationState.age, 1000)
    await state.finish()


products = get_all_products()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for product in products:
        with open(f'{product[0]}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=product_kb)


@dp.callback_query_handler(text='buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт')
    await call.answer()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6,25 x рост(см) - 5 x возраст(г) + 5')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kbt)


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = round((10 * float(data['weight'])) + (6.25 * float(data['height'])) - (5 * float(data['age'])) + 5, 2)
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
