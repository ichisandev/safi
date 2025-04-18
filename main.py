from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
from routers import main_router

load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm an echo bot. Send me something!")

# message handler
async def response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main_router.route(update, context)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, response))
    app.add_handler(MessageHandler(filters.PHOTO, response))

    app.run_polling()

if __name__ == '__main__':
    main()

