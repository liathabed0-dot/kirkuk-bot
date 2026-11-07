import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "حط_التوكن_الجديد_هنا")

# --- بيانات دليل كركوك الطبي ---
DOCTORS = {
    "سكري": ["د. باطنية - غدد صماء\n📍 شارع الاطباء - كركوك\n🕒 4 عصراً - 8 ليلاً\n📞 متوفر بالعيادة", "د. باطنية عامة\n📍 مجمع الشفاء الطبي\n🕒 10 صباحاً - 2 ظهراً"],
    "ضغط_قلب": ["د. قلب وشرايين\n📍 شارع الاطباء - مقابل مستشفى كركوك العام\n🕒 4 - 9 ليلاً", "د. باطنية - قلب\n📍 مجمع النور الطبي\n🕒 3 - 7 عصراً"],
    "معدة": ["د. جهاز هضمي وقولون\n📍 شارع الاطباء\n🕒 4 - 8 ليلاً", "د. باطنية - معدة\n📍 طريق بغداد - مجمع الرازي"],
    "صدر": ["د. صدرية وربو وحساسية\n📍 شارع الاطباء\n🕒 4 - 8 ليلاً"],
    "مفاصل": ["د. مفاصل وعظام وفقرات\n📍 شارع الاطباء\n🕒 4 - 9 ليلاً", "د. جراحة عظام\n📍 مجمع النور الطبي"],
    "جلدية": ["د. جلدية وحساسية\n📍 شارع الاطباء\n🕒 4 - 8 ليلاً"],
    "عيون": ["د. عيون\n📍 شارع الاطباء - مجمع العيون\n🕒 10 صباحاً - 8 ليلاً"],
    "انف_اذن": ["د. انف واذن وحنجرة\n📍 شارع الاطباء\n🕒 4 - 8 ليلاً"],
    "نسائية": ["د. نسائية وتوليد\n📍 شارع الاطباء\n🕒 10 صباحاً - 8 ليلاً"],
    "اطفال": ["د. اطفال وحديثي ولادة\n📍 شارع الاطباء\n🕒 4 - 9 ليلاً"],
    "اعصاب": ["د. جملة عصبية وصداع وشقيقة\n📍 شارع الاطباء\n🕒 4 - 8 ليلاً"],
    "كلى": ["د. كلى ومسالك بولية\n📍 شارع الاطباء\n🕒 4 - 8 ليلاً"],
    "اسنان": ["د. اسنان - تجميل وزراعة\n📍 مجمع النور الطبي - شارع الاطباء\n🕒 10 صباحاً - 9 ليلاً", "د. اسنان - تقويم\n📍 طريق بغداد"],
    "نفسية": ["د. نفسية وتوتر وقلق\n📍 شارع الاطباء\n🕒 بالحجز المسبق"],
    "عامة": ["د. طب عام - حمى وانفلونزا\n📍 شارع الاطباء\n🕒 9 صباحاً - 9 ليلاً"],
}

PHARMACIES = """💊 **صيدليات كركوك**

1. صيدلية النور - شارع الاطباء - دوام 24 ساعة
2. صيدلية الشفاء - طريق بغداد - 8 ص - 12 ليلاً
3. صيدلية الرازي - شارع الجمهورية - 8 ص - 11 ليلاً
4. صيدلية كركوك المركزية - سوق كركوك - 8 ص - 10 ليلاً
5. صيدلية الحياة - حي الواسطي - 8 ص - 12 ليلاً

🌙 **صيدلية الخفر:** صيدلية النور - شارع الاطباء - 24 ساعة
"""

COMPLEXES = """🏥 **المجمعات الطبية بكركوك**

1. مجمع النور الطبي - شارع الاطباء - كل الاختصاصات - 10 ص - 9 ليلاً
2. مجمع الشفاء الطبي - طريق بغداد - باطنية + اطفال + نسائية
3. مجمع الرازي الطبي - شارع الجمهورية - اسنان + عيون + مختبر
4. مجمع الاستشارة الطبي - شارع الاطباء - جراحة + عظام
5. مجمع الحياة الطبي - حي الواسطي - طب عام + تحاليل
"""

HOSPITALS_GOV = """🏨 **مستشفيات حكومية - كركوك**

1. مستشفى كركوك العام - مركز كركوك - طوارئ 24 ساعة
2. مستشفى الاطفال - كركوك - طوارئ اطفال 24 ساعة
3. مستشفى النسائية والتوليد - كركوك - ولادة وطوارئ 24 ساعة
4. مستشفى آزادي التعليمي - آزادي - طوارئ 24 ساعة
5. مستشفى الحويجة العام - الحويجة
"""

HOSPITALS_PRIVATE = """🏨 **مستشفيات اهلية - كركوك**

1. مستشفى النور الاهلي - شارع الاطباء - 24 ساعة
2. مستشفى الرازي الاهلي - طريق بغداد - 24 ساعة
3. مستشفى الشفاء الاهلي - مركز كركوك - طوارئ + عمليات
4. مستشفى الحياة الاهلي - حي الواسطي
"""

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🩺 حسب المرض", callback_data="diseases")],
        [InlineKeyboardButton("💊 صيدليات كركوك", callback_data="pharmacies"),
         InlineKeyboardButton("🏥 مجمعات طبية", callback_data="complexes")],
        [InlineKeyboardButton("🏨 مستشفيات حكومية", callback_data="hosp_gov"),
         InlineKeyboardButton("🏨 مستشفيات اهلية", callback_data="hosp_priv")],
    ]
    return InlineKeyboardMarkup(keyboard)

def diseases_menu():
    keyboard = [
        [InlineKeyboardButton("سكري وضغط وغدد", callback_data="doc_سكري")],
        [InlineKeyboardButton("قلب وشرايين", callback_data="doc_ضغط_قلب")],
        [InlineKeyboardButton("معدة وقولون", callback_data="doc_معدة")],
        [InlineKeyboardButton("صدر وربو", callback_data="doc_صدر")],
        [InlineKeyboardButton("مفاصل وعظام", callback_data="doc_مفاصل")],
        [InlineKeyboardButton("جلدية وحساسية", callback_data="doc_جلدية")],
        [InlineKeyboardButton("عيون", callback_data="doc_عيون")],
        [InlineKeyboardButton("انف واذن وحنجرة", callback_data="doc_انف_اذن")],
        [InlineKeyboardButton("نسائية", callback_data="doc_نسائية")],
        [InlineKeyboardButton("اطفال", callback_data="doc_اطفال")],
        [InlineKeyboardButton("اعصاب وصداع", callback_data="doc_اعصاب")],
        [InlineKeyboardButton("كلى ومسالك", callback_data="doc_كلى")],
        [InlineKeyboardButton("اسنان", callback_data="doc_اسنان")],
        [InlineKeyboardButton("نفسية", callback_data="doc_نفسية")],
        [InlineKeyboardButton("طب عام - حمى وانفلونزا", callback_data="doc_عامة")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "اهلا بيك بدليل كركوك الطبي 🏥\n\nشنو تحتاج؟ اختار من الازرار:"
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.edit_message_text("اهلا بيك بدليل كركوك الطبي 🏥\n\nشنو تحتاج؟ اختار:", reply_markup=main_menu())
    elif data == "diseases":
        await query.edit_message_text("اختار المرض او الاختصاص:", reply_markup=diseases_menu())
    elif data == "pharmacies":
        await query.edit_message_text(PHARMACIES, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]))
    elif data == "complexes":
        await query.edit_message_text(COMPLEXES, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]))
    elif data == "hosp_gov":
        await query.edit_message_text(HOSPITALS_GOV, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]))
    elif data == "hosp_priv":
        await query.edit_message_text(HOSPITALS_PRIVATE, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع", callback_data="back")]]))
    elif data.startswith("doc_"):
        key = data.replace("doc_", "")
        docs = DOCTORS.get(key, [])
        msg = "🩺 الدكاترة المتوفرين:\n\n" + "\n\n---\n\n".join(docs)
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ رجوع للامراض", callback_data="diseases")]]))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()
