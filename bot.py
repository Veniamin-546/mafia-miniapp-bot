import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests
from config import BOT_TOKEN, WEB_APP_URL

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    web_button = InlineKeyboardButton(
        text="🃏 Играть в Мафию",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    markup.add(web_button)

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в игру Мафия! 🃏\n\n"
        "Нажми кнопку, чтобы открыть игру.\n"
        "Внутри можно донатить Stars и получать бусты: +шанс на Мафию, доп. действия и т.д.! 🔥",
        reply_markup=markup
    )

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload
    stars_amount = message.successful_payment.total_amount

    bot.send_message(user_id, f"Спасибо за {stars_amount} ⭐! Бусты активированы! 🚀")

    try:
        import json
        data = json.loads(payload)
        boost_type = data['type']
        amount = data['amount']

        requests.post(f"{WEB_APP_URL.rstrip('/')}/api/add_boost", json={
            "user_id": user_id,
            "type": boost_type,
            "amount": amount
        })
    except Exception as e:
        print("Ошибка обработки буста:", e)

print("Бот запущен и ждёт игроков...")
bot.infinity_polling()