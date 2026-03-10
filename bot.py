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

    results = []

    for gstin in gst_list:

        url = f"https://gst-return-status.p.rapidapi.com/free/gstin/{gstin}"

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "gst-return-status.p.rapidapi.com"
        }

        r = requests.get(url, headers=headers)
        data = r.json()

        if data["success"]:

            name = data["data"]["tradeName"]

            returns = data["data"]["returns"][0]

            month = returns["taxp"]
            date = returns["dof"]

            results.append(f"{gstin} | {month} | {date}")

    with open("result.txt","w") as f:

        for line in results:
            f.write(line + "\n")

    await update.message.reply_document(open("result.txt","rb"))

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.Document.ALL, check))

app.run_polling()
