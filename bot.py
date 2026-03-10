import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("RAPIDAPI_KEY")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Checking GST numbers...")

    file = await update.message.document.get_file()
    await file.download_to_drive("gst.txt")

    gst_list = open("gst.txt").read().splitlines()

    results = []

    for gstin in gst_list:

        try:

            url = f"https://gst-insights-api.p.rapidapi.com/getGSTDetailsUsingGST/{gstin}"

            headers = {
                "x-rapidapi-key": API_KEY,
                "x-rapidapi-host": "gst-insights-api.p.rapidapi.com"
            }

            r = requests.get(url, headers=headers, timeout=20)
            data = r.json()

            if data.get("success"):

                info = data.get("data", {})
                last_update = info.get("lastUpdateDate")

                if last_update:
                    results.append(gstin)

        except:
            continue

    with open("result.txt","w") as f:

        for gst in results:
            f.write(gst + "\n")

    await update.message.reply_document(open("result.txt","rb"))

app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .read_timeout(60)
    .connect_timeout(60)
    .build()
)

app.add_handler(MessageHandler(filters.Document.ALL, check))

app.run_polling()
