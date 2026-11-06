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

# القاموس الشامل الذي يحتوي على المعرفات
FILES = {
    "emploi": [
        ("AgADhh0AAo_eoFI", "📅 إليك ملف استعمال الزمن للسداسي الحالي.")
    ],
    "university_platform": [
        ("AgADPSEAAt_s6VA", "🌐 ملف الكانفا الخاص بالجامعة.")
    ],
    "analyse3_td": [
        ("AgADfR0AAqGWqFI", "📝 سلسلة التمارين الأولى لمادة Analyse 03.")
    ],
    "probba_cours": [
        ("AgADZhoAAq3haFI", "📊 ملخص محاضرة الإحصاء والاحتمالات."),
        ("AgAD-iEAAjlh8VI", "📊 محاضرة الإحصاء والاحتمالات (جامعة تيارت).")
    ],
    "probba_exams": [
        ("AgADZhoAAq3haFI", "📑 ملخصات وإمتحانات مادة الإحصاء والاحتمالات.")
    ],
    "vibrations_cours": [
        ("AgADNSQAAnbVuVI", "🌊 محاضرة الاهتزازات والأمواج (Cours 02)."),
        ("AgADMR8AAhsvQFM", "🌊 محاضرة الاهتزازات والأمواج (جامعة سكيكدة).")
    ],
    "vibrations_td": [
        ("AgADsCAAAl9iOVI", "📝 سلسلة التمارين الأولى (TD 01)."),
        ("AgADSyQAArhJsFI", "📝 سلسلة التمارين الثانية (TD 02)."),
        ("AgADQiQAAiJ2KVM", "📝 سلسلة التمارين الثالثة (TD 03).")
    ],
    "electronique1_cours": [
        ("AgADWx8AAs7fsVI", "⚡ المحاضرة الأولى (Course 1)."),
        ("AgADXh8AAs7fsVI", "⚡ محاضرة الإلكترونيات 1 (ملف إضافي)."),
        ("AgADbR4AArgXCFM", "⚡ محاضرات نظريات الدوائر (Circuit Theorems).")
    ],
    "electronique1_td": [
        ("AgADXB8AAs7fsVI", "📝 سلسلة التمارين الأولى لمادة الإلكترونيات 1.")
    ],
    "electrotechnique1_cours": [
        ("AgADUyUAAlNC8FI", "🔌 المحاضرة الشاملة لمادة الإكتروتقني 1.")
    ],
    "energie_cours": [
        ("AgADTB4AAuCLmFI", "🌱 الطاقة والبيئة - المحاضرة الأولى."),
        ("AgADSB4AAuCLmFI", "🌱 الطاقة والبيئة - الفصل الثاني.")
    ],
    "etat_art_cours": [
        ("AgADSR4AAuCLmFI", "⚡ état de l'art - الفصل الأول.")
    ],
}

# أداة استخراج معرف الملف تلقائياً عند إرساله للبوت
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    await update.message.reply_text(f"file_id:\n`{doc.file_id}`", parse_mode="Markdown")

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
        f"أهلاً بك يا {user_name} في بوت L2 ElectroDZ\n"
        "إليك قائمة مواد السنة الثانية إلكترونيات للسداسي الثالث.\n\n"
        "اختر المادة المطلوبة أو الخدمة التي تحتاجها:"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if data == "back_to_start":
        await start(update, context)
        return

    # إرسال الملفات بشكل آمن وسريع دون أي تعليق
    if data in FILES:
        for file_id, caption in FILES[data]:
            try:
                await context.bot.send_document(
                    chat_id=chat_id, document=file_id, caption=caption
                )
            except TelegramError as e:
                logging.error(f"Failed to send {data}: {e}")
                await context.bot.send_message(
                    chat_id=chat_id, text="⚠️ تعذر إرسال هذا الملف، تأكد من الاتصال."
                )
        return

    # إذا اختار المستخدم المادة الرئيسية
    if data in SUBJECTS:
        subject_name = SUBJECTS[data]
        buttons = []
        
        if data in ["analyse3", "probba", "electronique1", "electrotechnique1"]:
            buttons = [
                [InlineKeyboardButton("📖 Cours", callback_data=f"{data}_cours"),
                 InlineKeyboardButton("📝 Fich TD", callback_data=f"{data}_td")],
                [InlineKeyboardButton("📑 Examens & Résumés", callback_data=f"{data}_exams")]
            ]
        elif data == "python":
            buttons = [
                [InlineKeyboardButton("📖 Cours", callback_data=f"{data}_cours"),
                 InlineKeyboardButton("🔬 Fich TP", callback_data=f"{data}_tp")],
                [InlineKeyboardButton("📑 Examens & Résumés", callback_data=f"{data}_exams")]
            ]
        elif data in ["energie", "etat_art"]:
            buttons = [
                [InlineKeyboardButton("📖 Cours", callback_data=f"{data}_cours")],
                [InlineKeyboardButton("📑 Examens & Résumés", callback_data=f"{data}_exams")]
            ]
        elif data == "vibrations":
            buttons = [
                [InlineKeyboardButton("📖 Cours", callback_data=f"{data}_cours"),
                 InlineKeyboardButton("📝 Fich TD", callback_data=f"{data}_td")],
                [InlineKeyboardButton("🔬 Fich TP", callback_data=f"{data}_tp"),
                 InlineKeyboardButton("📑 Examens & Résumés", callback_data=f"{data}_exams")]
            ]
        elif data == "tp_electro_combo":
            buttons = [
                [InlineKeyboardButton("🔬 Fich TP المشترك", callback_data=f"{data}_tp")]
            ]

        buttons.append([InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="back_to_start")])
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            f"⚡ أنت الآن داخل مادة: {subject_name}\n\nاختر القسم المطلوب:",
            reply_markup=reply_markup
        )
    
    # إذا ضغط على قسم فرعي لا توجد له ملفات مرفوعة بعد
    elif "_" in data:
        subject_key = data.split("_")[0]
        keyboard = [
            [InlineKeyboardButton("⬅️ العودة للمادة", callback_data=subject_key)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "📭 عذراً، لا يوجد شيء هنا حالياً.\nلم تقم بإضافة أي ملفات لهذا القسم بعد.",
            reply_markup=reply_markup
        )
    else:
        await start(update, context)

def main():
    if not TOKEN:
        print("Error: TOKEN is not set")
        return

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # معالج استخراج الـ file_id عند إرسال أي ملف للبوت
    application.add_handler(MessageHandler(filters.Document.ALL, get_file_id))

    print("Bot is running")
    application.run_polling()

if __name__ == "__main__":
    main()
