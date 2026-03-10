import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("RAPIDAPI_KEY")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    file = await update.message.document.get_file()
    await file.download_to_drive("gst.txt")

    gst_list = open("gst.txt").read().splitlines()

    result = []

    for gstin in gst_list:

        url = f"https://gst-insights-api.p.rapidapi.com/getGSTDetailsUsingGST/{gstin}"

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "gst-insights-api.p.rapidapi.com"
        }

        r = requests.get(url, headers=headers)
        data = r.json()

        if data["success"]:
            result.append(gstin)

    with open("result.txt","w") as f:

        for g in result:
            f.write(g + "\n")

    await update.message.reply_document(open("result.txt","rb"))

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.Document.ALL, check))

app.run_polling()
