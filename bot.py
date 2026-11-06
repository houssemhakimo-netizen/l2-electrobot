import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TOKEN")

# قائمة المواد الدراسية
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

# 1. ضع المعرفات الطويلة هنا لاحقاً (اتركها فارغة أو ضع مكانها أي شيء مؤقتاً)
FILES = {
    "emploi": [("FILE_ID_HERE", "📅 ملف استعمال الزمن")],
    "vibrations_cours": [("FILE_ID_HERE", "🌊 محاضرة الاهتزازات")],
}

# أداة سحرية: أي ملف ترسله للبوت في الشات، سيرد عليك فوراً بالـ file_id الحقيقي الخاص به!
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    await update.message.reply_text(f"خذ هذا الـ file_id الطويل:\n\n`{doc.file_id}`", parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "زميلنا"
    keyboard = []
    keys = list(SUBJECTS.keys())
    for i in range(0, len(keys), 2):
        row = [InlineKeyboardButton(SUBJECTS[keys[i]], callback_data=keys[i])]
        if i + 1 < len(keys):
            row.append(InlineKeyboardButton(SUBJECTS[keys[i+1]], callback_data=keys[i+1]))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("📅 استعمال الزمن", callback_data="emploi")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"أهلاً بك يا {user_name}\nاختر المادة:"
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if data == "back_to_start":
        await start(update, context)
        return

    if data in FILES:
        for file_id, caption in FILES[data]:
            try:
                await context.bot.send_document(chat_id=chat_id, document=file_id, caption=caption)
            except TelegramError as e:
                await context.bot.send_message(chat_id=chat_id, text=f"خطأ في إرسال الملف: {e}")
        return

    if data in SUBJECTS:
        subject_name = SUBJECTS[data]
        buttons = [
            [InlineKeyboardButton("📖 Cours", callback_data=f"{data}_cours"),
             InlineKeyboardButton("📝 Fich TD", callback_data=f"{data}_td")],
            [InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="back_to_start")]
        ]
        await query.message.edit_text(f"أنت في مادة: {subject_name}", reply_markup=InlineKeyboardMarkup(buttons))
    
    elif "_" in data:
        subject_key = data.split("_")[0]
        keyboard = [[InlineKeyboardButton("⬅️ عودة", callback_data=subject_key)]]
        await query.message.edit_text("عذراً، لا يوجد ملف هنا حالياً.", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await start(update, context)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # هذه الخطوة هي التي ستعطيك المعرفات الصحيحة في تيليجرام
    application.add_handler(MessageHandler(filters.Document.ALL, get_file_id))

    print("Bot is running")
    application.run_polling()

if __name__ == "__main__":
    main()
