import os
from flask import Flask
from threading import Thread
import telebot # Или твоя библиотека для бота

# --- НАСТРОЙКА ВЕБ-СЕРВЕРА (чтобы Render не отключал бота) ---
app = Flask('')

@app.route('/')
def home():
    return "Бот активен и работает!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# Запускаем веб-сервер в отдельном потоке
web_thread = Thread(target=run_web)
web_thread.start()

# --- ЗДЕСЬ ТВОЙ КОД БОТА ---
# Вставь сюда всё, что у тебя было (инициализацию бота и команды)
# Например:
# bot = telebot.TeleBot("ТВОЙ_ТОКЕН")
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Привет!")
# bot.infinity_polling()
