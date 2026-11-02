import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "9225900507:AAFPt2y-zJBvdgWwd_zm3TACqQ51_ThcguU"

async def start(update, context):
    await update.message.reply_text("هلا! اني بوت دليل اطباء كركوك 😊 كلي شنو تحتاج؟ مثلا اكتب: دكتور قلبية")

async def reply(update, context):
    t = update.message.text.lower()
    if "قلب" in t:
        m = "❤️ د. احمد محمد - شارع الاطباء 07701234567"
    elif "اطفال" in t:
        m = "👶 د. هيمن رشيد - مجمع النور"
    elif "اسنان" in t:
        m = "🦷 د. محمد علي - عيادة الابتسامة"
    else:
        m = "🏥 دليل اطباء كركوك:\nقلبية - اطفال - اسنان - جلدية - عيون - نسائية - عظام\nكلي شنو تريد؟"
    await update.message.reply_text(m)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()
