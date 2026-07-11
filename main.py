import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Твои ключи установлены
TELEGRAM_TOKEN = "8764681262:AAF5s3BIk_5Um0KHwt1zM1-rHK2gtHoDmcs"
GOOGLE_API_KEY = "AQ.Ab8RN6JqwAt4BCKLIqXBTyWWc_e4eUGWyets2m3rFQT5aGH-QQ"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я твой бот-метафора. О чем ты хочешь сегодня подумать?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(f"Ты терапевтичный бот. Ответь на это сообщение клиента через метафору: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Прости, произошла маленькая ошибка. Попробуй еще раз.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
