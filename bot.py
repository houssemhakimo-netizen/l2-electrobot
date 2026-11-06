import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# قائمة المواد المحدثة بالكامل مع إضافة Probabilités et Statistique
SUBJECTS = {
    "analyse3": "📐 Analyse 3",
    "probba": "📊 Probabilités et Statistique",
    "python": "💻 Programmation en Python",
    "vibrations": "🌊 Vibrations et ondes",
    "electronique1": "⚡ Électronique Fondamentale 1",
    "electrotechnique1": "🔌 Électrotechnique Fondamentale 1",
    "energie": "🌱 Énergie et Environnement",
    "etat_art": "⚡ État de l'art du Génie électrique",
}

# أمر /start - القائمة الرئيسية للمواد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    keys = list(SUBJECTS.keys())
    for i in range(0, len(keys), 2):
        row = [InlineKeyboardButton(SUBJECTS[keys[i]], callback_data=keys[i])]
        if i + 1 < len(keys):
            row.append(InlineKeyboardButton(SUBJECTS[keys[i+1]], callback_data=keys[i+1]))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("📚 دليل الاستخدام والأرشيف", callback_data="help")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "أهلاً بك يا حسام في بوت **L2 ElectroDZ** 🎓\n"
        "إليك قائمة مواد السنة الثانية إلكترونيات (السداسي الثالث).\n\n"
        "اختر المادة المطلوبة لتظهر لك أقسامها المستقلة (Cours, TD, TP):"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)

# التعامل مع الأزرار وجعل كل مادة مستقلة
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_start":
        await start(update, context)
        return

    if data in SUBJECTS:
        subject_name = SUBJECTS[data]
        keyboard = [
            [
                InlineKeyboardButton("📖 Cours", callback_data=f"{data}_cours"),
                InlineKeyboardButton("📝 Fich TD", callback_data=f"{data}_td"),
            ],
            [
                InlineKeyboardButton("🔬 Fich TP", callback_data=f"{data}_tp"),
                InlineKeyboardButton("📑 Examens & Résumés", callback_data=f"{data}_exams"),
            ],
            [
                InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="back_to_start")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            f"⚡ أنت الآن داخل مادة: **{subject_name}**\n\nاختر القسم الذي تحتاجه:",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("⬅️ العودة للمادة", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "📁 سيتم رفع ملفات هذا القسم قريباً لهذه المادة يا بطل! 🚀",
            reply_markup=reply_markup
        )

def main():
    if not TOKEN:
        print("Error: TOKEN is not set!")
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
