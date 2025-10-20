# ---------------- PROXY TELEGRAM BOT ----------------
import os
import io
import pandas as pd
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from gogle_Api_Interact import download_csv  # uses your Drive setup
from config import TELEGRAM_TOKEN  # your bot token from config.py

# ---------------- COMMAND HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command."""
    welcome_text = (
        "👋 Hi there!\n"
        "I'm your Proxy Data Bot.\n\n"
        "You can ask me things like:\n"
        "• give live proxies\n"
        "• send tested ones\n"
        "• show correct proxies\n\n"
        "I'll fetch and send you the latest `liveproxy.csv` from Google Drive."
    )
    await update.message.reply_text(welcome_text)


# ---------------- MESSAGE HANDLER ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle normal text messages."""
    message = update.message.text.lower().strip()

    if any(keyword in message for keyword in ["live", "tested", "correct", "working"]):
        await update.message.reply_text("⏳ Fetching latest live proxies from Drive...")

        try:
            df = download_csv("liveproxy.csv")
            if df is None or df.empty:
                await update.message.reply_text("❌ No live proxies found in Drive.")
                return

            # Convert DataFrame to CSV in-memory
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            await update.message.reply_document(
                document=csv_buffer.getvalue().encode(),
                filename="liveproxy.csv",
                caption=f"✅ Found {len(df)} live proxies. Use responsibly!"
            )
        except Exception as e:
            print(f"❌ Error fetching proxies: {e}")
            await update.message.reply_text(f"⚠️ Error fetching live proxies: {e}")
    else:
        await update.message.reply_text("🤖 Type 'give live proxies' to get the latest tested list.")


# ---------------- MAIN ENTRY POINT ----------------
def main():
    """Start the Telegram bot."""
    print("🚀 Proxy Telegram Bot starting...")

    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ TELEGRAM_TOKEN missing in config.py!")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is live. Send a message to get your proxies.")
    app.run_polling()


if __name__ == "__main__":
    main()
