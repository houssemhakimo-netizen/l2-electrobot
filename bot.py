import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في L2 ElectroBot! البوت يعمل بنجاح.")

if __name__ == '__main__':
    TOKEN = os.environ.get("TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    app.run_polling()
