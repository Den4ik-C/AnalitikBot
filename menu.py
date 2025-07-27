from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню (Слой 1)
main_menu = ReplyKeyboardMarkup(
    keyboard=[  
        [KeyboardButton("📂 Личный кабинет")],
        [KeyboardButton("🔍 По номеру транзакции")],
        [KeyboardButton("📘 Инструкции"),      KeyboardButton("🔗 Ссылки")],
        [KeyboardButton("📄 FAQ")],
    ],
    resize_keyboard=True
)

# Меню личного кабинета (Слой 2.1)
cabinet_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("➕ Добавить кошелёк")],
        [KeyboardButton("💼 Криптопортфель")],
        [KeyboardButton("📊 Поверхностный анализ"), KeyboardButton("📈 Подробный анализ")],
        [KeyboardButton("🔙 Назад")],
        [KeyboardButton("⚙️ Настроки")]
    ],
    resize_keyboard=True
)


portfolio_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📁 Создать портфель")],
        [KeyboardButton("📑 Мои портфели")],
        [KeyboardButton("💳 Кошельки (вне портфелей)")],
        [KeyboardButton("🔙 Назад")]
    ],
    resize_keyboard=True
)
