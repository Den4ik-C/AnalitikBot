from database import init_db
init_db() 
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN
from menu import main_menu, cabinet_menu, portfolio_menu
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from wallet_fsm import WalletFSM, start_wallet_add, wallet_name_entered, wallet_network_entered 
from wallet_fsm import show_user_wallets 
storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)  

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}! Добро пожаловать!",
        reply_markup=main_menu
    )

@dp.message_handler(lambda msg: msg.text == "📂 Личный кабинет")
async def cabinet_menu_handler(message: types.Message):
    await message.answer("Вы в личном кабинете. Выберите действие:", reply_markup=cabinet_menu)

@dp.message_handler(lambda msg: msg.text == "🔍 По номеру транзакции")
async def txid_handler(message: types.Message):
    await message.answer("Введите номер транзакции (TXID):")

@dp.message_handler(lambda msg: msg.text == "📘 Инструкции")
async def instructions_handler(message: types.Message):
    await message.answer("🔧 Инструкция:\n1. Добавьте кошелёк\n2. Введите транзакции\n3. Получите анализ")

@dp.message_handler(lambda msg: msg.text == "🔗 Ссылки")
async def links_handler(message: types.Message):
    await message.answer("🔗 Полезные ссылки:\n- Канал: https://https://t.me/invest_watch\n- Dexscreener: https://dexscreener.com/")

@dp.message_handler(lambda msg: msg.text == "🔙 Назад")
async def back_handler(message: types.Message):
    await message.answer("⬅️ Возврат в главное меню", reply_markup=main_menu)

@dp.message_handler(lambda msg: msg.text == "➕ Добавить кошелёк")
async def add_wallet_handler(message: types.Message):
        await start_wallet_add(message)
@dp.message_handler(lambda msg: msg.text == "📋 Мои кошельки")
async def my_wallets_handler(message: types.Message):
        await        show_user_wallets(message)
@dp.message_handler(lambda msg: msg.text == "💼 Криптопортфель")
async def portfolio_menu_handler(message: types.Message):
        await message.answer("📊 Работа с портфелями:", reply_markup=portfolio_menu)

if __name__ == "__main__":
    dp.register_message_handler(wallet_name_entered, state=WalletFSM.name)
    dp.register_message_handler(wallet_network_entered, state=WalletFSM.network)
    executor.start_polling(dp, skip_updates=True)