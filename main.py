import os
import telebot
import google.generativeai as genai
from google.auth.credentials import Credentials
from flask import Flask
from threading import Thread

# Твои ключи
TELEGRAM_TOKEN = "8764681262:AAF5s3BIk_5Um0KHwt1zM1-rHK2gtHoDmcs"
# Сюда вставляем тот самый твой первый ключ, который начинается на AQ.
GEMINI_API_KEY = "AQ.Ab8RN6JqwAt4BCKLIqXBTyWWc_e4eUGWyets2m3rFQT5aGH-QQ"

# Авторизуем сервисный ключ как OAuth2 токен, раз Google Cloud требует именно его
creds = Credentials(token=GEMINI_API_KEY)
genai.configure(credentials=creds)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=(
        "Ты — профессиональный психотерапевт, гипнолог и мастер терапевтических метафор. "
        "Твоя задача — написать глубокую, красивую, исцеляющую психологическую метафору по запросу пользователя. "
        "Используй его имя, его образ проблемы и телесный зажим. "
        "Текст должен быть гипнотическим, расслабляющим, метафоричным, возвращающим контакт с телом и выводящим в ресурсное состояние. "
        "В конце метафоры сделай мягкий экологичный переход к тому, что для глубоких жизненных кризисов "
        "и переписки сценариев всегда можно обратиться на личный разбор/медиацию к автору проекта — Татьяне."
    )
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

user_data = {}

QUESTIONS = [
    "Привет! Давай создадим твою личную терапевтическую метафору. Как мне к тебе обращаться? (Напиши свое имя)",
    "Какая эмоция, страх или мысль не дает тебе спокойно выдохнуть прямо сейчас?",
    "Где в теле сильнее всего чувствуется это напряжение? (Например: ком в горле, тяжесть в груди, зажим в плечах)",
    "Если бы твоя проблема была образом, предметом или стихией — как бы она выглядела?",
    "Какое состояние ты хочешь чувствовать вместо этого, когда пройдешь эту практику?"
]

@app.route('/')
def home():
    return "Метафора Силы в сети!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start_quiz(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 0, 'answers': []}
    bot.send_message(chat_id, QUESTIONS[0])

@bot.message_handler(func=lambda message: True)
def handle_quiz(message):
    chat_id = message.chat.id
    
    if chat_id not in user_data:
        start_quiz(message)
        return

    state = user_data[chat_id]
    step = state['step']
    
    state['answers'].append(message.text)
    step += 1
    state['step'] = step

    if step < len(QUESTIONS):
        bot.send_message(chat_id, QUESTIONS[step])
    else:
        bot.send_message(chat_id, "Спасибо. Твоя история принята. Я создаю твою личную метафору силы, это займет около 10 секунд...")
        
        name, emotion, body, image, target = state['answers']
        
        prompt = (
            f"Создай именную метафору для пользователя по имени {name}. "
            f"Текущая проблема/эмоция: {emotion}. "
            f"Ощущение в теле: {body}. "
            f"Образ проблемы: {image}. "
            f"Желаемое состояние в финале: {target}."
        )
        
        try:
            response = model.generate_content(prompt)
            bot.send_message(chat_id, response.text)
        except Exception as e:
            bot.send_message(chat_id, f"Ошибка API Gemini: {str(e)}")
        
        del user_data[chat_id]

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    bot.infinity_polling()
