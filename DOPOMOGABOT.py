from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

API_TOKEN = "7652734261:AAGBkXeDyiYF7b96LVWAu5cfxpKVeUzcb_k"

# Каналы, на которые пользователь должен подписаться
CHANNELS = [
    "@INFOpuls247",
    "@UA_Live24I7",
    "@Kyivofficial24l7",
    "@AirmapsofUkraine",
    "@special_new_s"
]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Стартовое сообщение
@dp.message(Command("start"))
async def send_welcome(message: Message):
    greeting_text = (
        "Вітаю!\nЯ тут для того, щоб допомогти Вам.\nВи хочете отримати інструкцію?"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Так", callback_data="instruction")]
    ])
    await message.answer(greeting_text, reply_markup=keyboard)

# Кнопка для запроса инструкции
@dp.callback_query(lambda callback: callback.data == "instruction")
async def show_channels(callback: CallbackQuery):
    message_text = (
        "Будь ласка, підпишіться на канали спонсорів для допомоги розвитку Бот Помічника."
    )
    # Список каналов для подписки
    channels_text = "\n".join([f"👉 {channel}" for channel in CHANNELS])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Підписався", callback_data="check_subs")]
    ])
    await callback.message.answer(message_text + "\n" + channels_text, reply_markup=keyboard)

# Проверка подписки на каналы
@dp.callback_query(lambda callback: callback.data == "check_subs")
async def check_subscriptions(callback: CallbackQuery):
    user_id = callback.from_user.id
    not_subscribed = []

    # Проверяем подписку на все каналы
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except Exception as e:
            not_subscribed.append(channel)

    # Если подписан на все каналы
    if not not_subscribed:
        # Ссылка на выплату и финальное сообщение
        await callback.message.answer(
            "Дякую за довіру.\nСлідкуйте за новинами в каналах спонсорах, там завжди публікується нова інформація про виплати Українцям.\nСлава Україні!"
        )
        await callback.message.answer("💰 Ваш бонус: https://t.me/vyplatigro")
    else:
        channels_text = "\n".join([f"👉 {channel}" for channel in not_subscribed])
        await callback.message.answer(f"Ви не підписані на наступні канали:\n{channels_text}")

# Оплата (по желанию можно оставить)
@dp.callback_query(lambda callback: callback.data == "pay")
async def pay_option(callback: CallbackQuery):
    await callback.message.answer("Функція оплати поки що не налаштована. Скоро вона з'явиться!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())