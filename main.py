import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Настройка ключей
TELEGRAM_TOKEN = "8764681262:AAF5s3BIk_5Um0KHwt1zM1-rHK2gtHoDmcs"
GEMINI_API_KEY = "AQ.Ab8RN6JqwAt4BCKLIqXBTyWWc_e4eUGWyets2m3rFQT5aGH-QQ"

# Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Блок для удержания порта (чтобы Render не выключал бота)
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Логика бота
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке запроса.")

# Запуск
if __name__ == '__main__':
    # Запускаем веб-сервер в отдельном потоке
    t = Thread(target=run_web)
    t.start()
    # Запускаем бота
    bot.infinity_polling()
