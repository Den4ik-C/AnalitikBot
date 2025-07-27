from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import json
import os

class WalletFSM(StatesGroup):
    name = State()
    network = State()

WALLET_FILE = "wallets.json"

def save_wallet(user_id, wallet):
    data = {}
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as f:
            data = json.load(f)
    data.setdefault(str(user_id), []).append(wallet)
    with open(WALLET_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def start_wallet_add(message: types.Message):
    await message.answer("Введите имя кошелька:")
    await WalletFSM.name.set()

async def wallet_name_entered(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите сеть (например, TON, TRC20, ERC20):")
    await WalletFSM.next()

async def wallet_network_entered(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    wallet = {
        "name": user_data["name"],
        "network": message.text
    }
    save_wallet(message.from_user.id, wallet)
    await message.answer(f"✅ Кошелёк «{wallet['name']}» в сети {wallet['network']} добавлен!")
    await state.finish() 
from database import get_user_wallets, get_user_portfolios

async def show_user_wallets(message: types.Message):
    user_id = message.from_user.id
    wallets = get_user_wallets(user_id)

    if not wallets:
        await message.answer("❌ У вас ещё нет кошельков.")
        return

    # Загружаем портфели (чтобы подписать)
    portfolios = {str(pid): name for pid, name in get_user_portfolios(user_id)}

    text = "📋 Ваши кошельки:\n\n"
    for i, (wid, name, network, portfolio_id) in enumerate(wallets, 1):
        if portfolio_id:
            pname = portfolios.get(str(portfolio_id), "❓Неизвестный портфель")
            text += f"{i}. {name} ({network}) — 🔗 {pname}\n"
        else:
            text += f"{i}. {name} ({network}) — ❗ Без портфеля\n"

    await message.answer(text)