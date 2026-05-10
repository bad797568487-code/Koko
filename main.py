import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
BOT_TOKEN = "8566707591:AAH-sEc5zGNUPRDbsiyefot4md7HtLJ0Mj8"
GEMINI_API_KEY = "AIzaSyCRAYgEzku8MpHru0TjhDmu7pVrk2itnL4"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    await update.message.reply_text(
        "👋 ဟိုင်း သားကြီး!\n\n"
        "ငါက Node.js code တွေကို Python အဖြစ် Gemini AI သုံးပြီး ပြောင်းပေးမယ့် Bot ပါ။\n"
        "ပြောင်းချင်တဲ့ Node.js ကုဒ်တွေကို ဒီအတိုင်း ပို့ပေးလိုက်ပါ။"
    )

async def convert_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI code conversion logic"""
    user_code = update.message.text
    status_msg = await update.message.reply_text("⏳ Gemini AI က Python ပြောင်းပေးနေတယ်... ခဏစောင့်နော်...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Please convert this Node.js code to clean Python code. Give ONLY the code, no explanation:\n\n{user_code}"
            }]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        # Extract AI response
        python_code = data['candidates'][0]['content']['parts'][0]['text']

        if len(python_code) > 4000:
            with open("converted.py", "w", encoding="utf-8") as f:
                f.write(python_code)
            await update.message.reply_document(document=open("converted.py", "rb"), filename="converted.py")
        else:
            await update.message.reply_text(f"✅ Python Code ရပါပြီ:\n\n```python\n{python_code}\n```", parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Error တက်သွားတယ်: {str(e)}")
    finally:
        await status_msg.delete()

def main():
    """Application setup with v20+ syntax"""
    # Updater မဟုတ်ဘဲ Application ကို သုံးထားတယ်
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_code))

    print("Bot is starting...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
          
