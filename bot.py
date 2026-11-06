import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TOKEN")

# قائمة المواد الدراسية للسداسي الثالث
SUBJECTS = {
    "analyse3": "📐 Analyse 3",
    "probba": "📊 Probabilités et Statistique",
    "python": "💻 Programmation en Python",
    "vibrations": "🌊 Vibrations et ondulations",
    "electronique1": "⚡ Électronique Fondamentale 1",
    "electrotechnique1": "🔌 Électrotechnique Fondamentale 1",
    "energie": "🌱 Énergie et Environnement",
    "etat_art": "⚡ État de l'art du Génie électrique",
    "tp_electro_combo": "🔬 TP Électronique & Électrotechnique",
}

# سنقوم بملء هذا القاموس بالمعرفات الطويلة الصحيحة تباعاً
FILES = {}

# أمر /start - القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "زميلنا"
    
    keyboard = []
    keys = list(SUBJECTS.keys())
    for i in range(0, len(keys), 2):
        row = [InlineKeyboardButton(SUBJECTS[keys[i]], callback_data=keys[i])]
        if i + 1 < len(keys):
            row.append(InlineKeyboardButton(SUBJECTS[keys[i+1]], callback_data=keys[i+1]))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("📅 استعمال الزمن", callback_data="emploi"),
                     InlineKeyboardButton("🌐 منصة الجامعة", callback_data="university_platform")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"أهلاً بك يا {user_name} في بوت L2 ElectroDZ\n\n"
        "📥 أرسل أي ملف PDF الآن إلى هذا البوت مباشرة، وسيرد عليك بالـ `file_id` الصحيح والطويل الخاص به فوراً!"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)

# هذه هي الدالة المطلوبة: تلتقط الملف المرسل وترد بـ file_id الخاص بهذا البوت حصرياً
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if doc:
        await update.message.reply_text(
            f"✅ الـ file_id الصحيح الخاص بهذا البوت:\n\n`{doc.file_id}`",
            parse_mode="Markdown"
        )

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_start":
        await start(update, context)
        return

    if data in FILES:
        for file_id, caption in FILES[data]:
            try:
                await context.bot.send_document(
                    chat_id=query.message.chat_id, document=file_id, caption=caption
                )
            except TelegramError as e:
                logging.error(f"Failed to send {data}: {e}")
        return

    await query.message.edit_text("📭 قيد التحديث، أرسل الملفات للبوت أولاً لاستخراج المعرفات.")

def main():
    if not TOKEN:
        print("Error: TOKEN is not set")
        return

    application = Application.builder().token(TOKEN).build()
    
    # المعالجات الأساسية
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # المعالج الخاص باستخراج الـ file_id عبر بوتك حصرياً
    application.add_handler(MessageHandler(filters.Document.ALL, get_file_id))

    print("Bot is running")
    application.run_polling()

if __name__ == "__main__":
    main()
