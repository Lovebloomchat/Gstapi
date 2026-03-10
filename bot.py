import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("RAPIDAPI_KEY")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Processing GST numbers...")

    file = await update.message.document.get_file()
    await file.download_to_drive("gst.txt")

    gst_list = open("gst.txt").read().splitlines()

    results = []

    for gstin in gst_list:

        try:

            url = f"https://gst-return-status.p.rapidapi.com/free/gstin/{gstin}"

            headers = {
                "x-rapidapi-key": API_KEY,
                "x-rapidapi-host": "gst-return-status.p.rapidapi.com"
            }

            r = requests.get(url, headers=headers, timeout=20)
            data = r.json()

            if "data" in data:

                returns = data["data"].get("returns", [])

                if len(returns) > 0:

                    latest = returns[0]

                    month = latest.get("taxp", "NA")
                    date = latest.get("dof", "NA")

                    results.append(f"{gstin} | {month} | {date}")

                else:

                    results.append(f"{gstin} | No Return Data")

        except:

            results.append(f"{gstin} | API Error")

    with open("result.txt","w") as f:

        f.write("GSTIN | Month | Filing Date\n\n")

        for line in results:
            f.write(line + "\n")

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
