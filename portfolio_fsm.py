from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import json
import os

class PortfolioFSM(StatesGroup):
    name = State()

PORTFOLIO_FILE = "portfolios.json"

def save_portfolio(user_id, portfolio_name):
    data = {}
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            data = json.load(f)

    data.setdefault(str(user_id), []).append(portfolio_name)

    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Запуск FSM
async def start_portfolio_add(message: types.Message):
    await message.answer("Введите название нового портфеля:")
    await PortfolioFSM.name.set()

# Обработка ввода
async def portfolio_name_entered(message: types.Message, state: FSMContext):
    name = message.text
    save_portfolio(message.from_user.id, name)
    await message.answer(f"✅ Портфель «{name}» создан и сохранён!")
    await state.finish()
    async def show_user_portfolios(message: types.Message):
        user_id = str(message.from_user.id)
        PORTFOLIO_FILE = "portfolios.json"

        if not os.path.exists(PORTFOLIO_FILE):
            await message.answer("У вас ещё нет портфелей.")
            return

        with open(PORTFOLIO_FILE, "r") as f:
            data = json.load(f)

        portfolios = data.get(user_id, [])

        if not portfolios:
            await message.answer("У вас ещё нет портфелей.")
            return

        text = "📑 Ваши портфели:\n\n"
        for i, name in enumerate(portfolios, 1):
            text += f"{i}. {name}\n"

        await message.answer(text)