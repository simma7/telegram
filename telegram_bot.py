import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8336950006:AAEjPEG3Cj94EAhZhpL7Oh7S-eo_f24jZoE"

HF_API_URL = "https://Simma7-deepfake_guard.hf.space/run/predict"

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    file = None
    file_path = "input"

    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        file_path += ".jpg"

    elif update.message.audio:
        file = await update.message.audio.get_file()
        file_path += ".mp3"

    elif update.message.voice:
        file = await update.message.voice.get_file()
        file_path += ".ogg"

    elif update.message.video:
        file = await update.message.video.get_file()
        file_path += ".mp4"

    else:
        await update.message.reply_text(" Send image / audio / video")
        return

    await file.download_to_drive(file_path)

    await update.message.reply_text("⏳ Processing...")

    try:
        
        response = requests.post(
            HF_API_URL,
            json={"data": [file_path]}
        )

        result = response.json()

        # Extract output
        if "data" in result:
            output = result["data"][0]
        else:
            output = str(result)

        await update.message.reply_text(f"🔍 Result:\n{output}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_file))

print(" Bot running...")
app.run_polling()
