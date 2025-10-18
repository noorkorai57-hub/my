import os
import requests
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8435843671:AAGm1oKc1OILMQD4KYiwrL9nprMrbdVrc04")
API_URL = "https://yabes-api.pages.dev/api/ai/video/v2"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 *Welcome to Veo3 Video Bot!*\nSend me a prompt using:\n\n`/video your prompt here`\n\nExample:\n`/video a beautiful sunrise over mountains`", parse_mode="Markdown")

# Video command
async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Please provide a prompt.\nExample:\n`/video a car driving through neon streets`", parse_mode="Markdown")
        return
    
    prompt = " ".join(context.args)
    await update.message.reply_text(f"🌀 Generating video for:\n`{prompt}`\n\nPlease wait...", parse_mode="Markdown")

    try:
        # Step 1: Create video task
        create_url = f"{API_URL}?action=create&prompt={prompt}"
        create_res = requests.get(create_url).json()
        task_id = create_res.get("taskId")

        if not task_id:
            await update.message.reply_text("❌ Error creating video task.")
            return

        # Step 2: Check status
        for i in range(10):
            status_url = f"{API_URL}?action=status&taskId={task_id}"
            status_res = requests.get(status_url).json()

            if status_res.get("status") == "completed":
                video_url = status_res.get("videoUrl")
                await update.message.reply_video(video_url, caption="✅ *Your Veo3 video is ready!*", parse_mode="Markdown")
                return
            await asyncio.sleep(5)

        await update.message.reply_text("⏳ Still processing... please try again later.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("video", video))
app.run_polling()
