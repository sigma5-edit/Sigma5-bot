from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import logging
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# API anahtarları
TOKEN = os.getenv("TELEGRAM_TOKEN")  # ✅ .env'deki değişken adıyla eşleşmeli
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client'ı başlat
client = OpenAI(api_key=OPENAI_API_KEY)

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)  # Gereksiz HTTP loglarını gizle

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sigma5 Body işledi! Mesaj yazmaya başlayın.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": update.message.text}],
            temperature=0.7,
        )
        await update.message.reply_text(response.choices[0].message.content)
        
    except Exception as e:
        logging.error(f"Hata: {e}")
        await update.message.reply_text("⚠️ Bagyşlaň, şuwagt ýalňyşlyk ýüze çykdy.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handler'ları ekle
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
