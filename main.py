from aiogram import Bot, Dispatcher, types
import logging

from aiogram.types import ContentTypes, MenuButtonWebApp, WebAppInfo
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)

TOKEN = "5494707928:AAFujbekNwEBa7soMvkDR7FjFmVc0ntdvPY"
ADMIN_CHAT_ID = "410580186"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def on_startup(dp):
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Магазин", web_app=WebAppInfo(url="https://mcmaleev.github.io/shop-bot/"))
    )


@dp.message_handler(commands=["info", "start"])
async def info(message: types.Message):
    reply = 'Тестовый бот магазина'
    await message.answer(reply)


@dp.message_handler(commands=["testpay"])
async def info(message: types.Message):
    print(message)
    await bot.send_invoice(
        message.chat.id,
        title="Оплата тестового счета",
        description="Описание тестового счета.",
        provider_token="284685063:TEST:ZmMwYjBhYjRjN2Jk",
        currency="RUB",
        photo_url="http://d2vrvpw63099lz.cloudfront.net/checkout-elements/checkout-boy.jpg",
        photo_width=735,
        photo_height=490,
        is_flexible=False,
        prices=[
            types.LabeledPrice(label="Продукт 1", amount=250*100),
            types.LabeledPrice(label="Продукт 2", amount=150*100)
        ],
        payload="testpay=1445",
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="✅ Заплатить", pay=True)
                ],
                [
                    types.InlineKeyboardButton(
                        text="⭕ Отменить", callback_data="pay||cancel")
                ],
                [
                    types.InlineKeyboardButton(text="♻ Назад в магазин", web_app=types.WebAppInfo(
                        url="https://mcmaleev.github.io/shop-bot/"))
                ]
            ])
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def success_payment(message: types.Message):
    print(message)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await bot.send_message(chat_id=message.chat.id, text="Спасибо за заказ!")
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"НОВЫЙ ЗАКАЗ!"
                                                       f"\nИМЯ: {message['successful_payment']['order_info']['name']}"
                                                       f"\nТЕЛЕФОН: {message['successful_payment']['order_info']['phone_number']}"
                                                       f"\nШИП: {message['successful_payment']['order_info']['shipping_address']}")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
