import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_KEY = "YOUR_RAPIDAPI_KEY"

async def gst_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gst = update.message.text.strip()

    url = f"https://gst-insights-api.p.rapidapi.com/getGSTDetailsUsingGST/{gst}"

    headers = {
        "x-rapidapi-host": "gst-insights-api.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    if data["success"]:
        d = data["data"]

        msg = f"""
🏢 *{d['legalName']}*

GSTIN: `{d['gstNumber']}`
Status: {d['status']}
Business Type: {d['constitutionOfBusiness']}
Registration Date: {d['registrationDate']}

📍 Address:
{d['principalAddress']['address']['district']},
{d['principalAddress']['address']['streetcd']} - {d['principalAddress']['address']['pincode']}
"""
    else:
        msg = "❌ GST number not found"

    await update.message.reply_text(msg, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gst_lookup))

app.run_polling()
