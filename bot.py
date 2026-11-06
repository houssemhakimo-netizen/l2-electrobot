import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

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
    
    # إضافة زر استعمال الزمن وزر منصة الجامعة في أسفل القائمة الرئيسية
    keyboard.append([InlineKeyboardButton("📅 استعمال الزمن", callback_data="emploi"),
                     InlineKeyboardButton("🌐 منصة الجامعة", callback_data="university_platform")])
    keyboard.append([InlineKeyboardButton("📚 دليل الاستخدام والأرشيف", callback_data="help")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"أهلاً بك يا {user_name} في بوت L2 ElectroDZ\n"
        "إليك قائمة مواد السنة الثانية إلكترونيات للسداسي الثالث.\n\n"
        "اختر المادة المطلوبة أو الخدمة التي تحتاجها:"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_to_start":
        await start(update, context)
        return

    # زر استعمال الزمن
    if data == "emploi":
        await query.message.reply_document(
            document="AgADhh0AAo_eoFI",
            caption="📅 إليك ملف استعمال الزمن للسداسي الحالي."
        )
        return

    # زر منصة الجامعة (ملف الكانفا الجامعي)
    if data == "university_platform":
        await query.message.reply_document(
            document="AgADPSEAAt_s6VA",
            caption="🌐 ملف الكانفا الخاص بالجامعة."
        )
        return

    # --- ملفات مادة Analyse 3 ---
    if data == "analyse3_td":
        await query.message.reply_document(
            document="AgADfR0AAqGWqFI",
            caption="📝 سلسلة التمارين الأولى لمادة Analyse 03."
        )
        return

    # --- ملفات مادة Probabilités et Statistique ---
    if data == "probba_cours":
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADZhoAAq3haFI", caption="📊 ملخص محاضرة الإحصاء والاحتمالات.")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgAD-iEAAjlh8VI", caption="📊 محاضرة الإحصاء والاحتمالات (جامعة تيارت).")
        return

    if data == "probba_exams":
        await query.message.reply_document(
            document="AgADZhoAAq3haFI",
            caption="📑 ملخصات وإمتحانات مادة الإحصاء والاحتمالات."
        )
        return

    # --- ملفات مادة Vibrations et ondes ---
    if data == "vibrations_cours":
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADNSQAAnbVuVI", caption="🌊 محاضرة الاهتزازات والأمواج (Cours 02).")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADMR8AAhsvQFM", caption="🌊 محاضرة الاهتزازات والأمواج (جامعة سكيكدة).")
        return

    if data == "vibrations_td":
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADsCAAAl9iOVI", caption="📝 سلسلة التمارين الأولى (TD 01).")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADSyQAArhJsFI", caption="📝 سلسلة التمارين الثانية (TD 02).")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADQiQAAiJ2KVM", caption="📝 سلسلة التمارين الثالثة (TD 03).")
        return

    # --- ملفات مادة Électronique Fondamentale 1 ---
    if data == "electronique1_cours":
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADWx8AAs7fsVI", caption="⚡ المحاضرة الأولى (Course 1).")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADXh8AAs7fsVI", caption="⚡ محاضرة الإلكترونيات 1 (ملف إضافي).")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADbR4AArgXCFM", caption="⚡ محاضرات نظريات الدوائر (Circuit Theorems - Kirchhoff, Thevenin, Norton).")
        return

    if data == "electronique1_td":
        await query.message.reply_document(
            document="AgADXB8AAs7fsVI",
            caption="📝 سلسلة التمارين الأولى لمادة الإلكترونيات 1."
        )
        return

    # --- ملفات مادة Électrotechnique Fondamentale 1 ---
    if data == "electrotechnique1_cours":
        await query.message.reply_document(
            document="AgADUyUAAlNC8FI",
            caption="🔌 المحاضرة الشاملة لمادة الإكتروتقني 1."
        )
        return

    # --- ملفات مادة Énergie et Environnement ---
    if data == "energie_cours":
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADTB4AAuCLmFI", caption="🌱 الطاقة والبيئة - المحاضرة الأولى (Cours 1).")
        await context.bot.send_document(chat_id=query.message.chat_id, document="AgADSB4AAuCLmFI", caption="🌱 الطاقة والبيئة - الفصل الثاني (Chapitre 2).")
        return

    # --- ملفات مادة État de l'art du Génie électrique ---
    if data == "etat_art_cours":
        await query.message.reply_document(
            document="AgADSR4AAuCLmFI",
            caption="⚡ état de l'art - الفصل الأول."
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
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    # إذا ضغط على قسم فرعي لا توجد فيه ملفات مرفوعة بعد
    elif "_" in data:
        subject_key = data.split("_")[0]
        keyboard = [
            [InlineKeyboardButton("⬅️ العودة للمادة", callback_data=subject_key)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "📭 عذراً، لا يوجد شيء هنا حالياً.\nلم تقم بإضافة أي ملفات لهذا القسم بعد.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
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

    print("Bot is running")
    application.run_polling()

if __name__ == "__main__":
    main()
