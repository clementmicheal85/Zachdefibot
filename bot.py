import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ===== Configuration =====
TOKEN = "7625161253:AAHnAhkQHyImRtfig0C5DqNFHuWYawfGv_4"  # TESTING ONLY - REVOKE LATER
CHANNEL_LINK = "https://t.me/your_channel"  # Change to your channel
GROUP_LINK = "https://t.me/your_group"     # Change to your group
TWITTER_LINK = "https://twitter.com/your_profile"  # Change to your Twitter

# ===== Helper Functions =====
def generate_solscan_link():
    """Generate random Solscan-like transaction link"""
    tx_id = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    return f"https://solscan.io/tx/{tx_id}?cluster=devnet"

# ===== Handlers =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🐦 Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ Done", callback_data="submit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎉 Welcome to Airdrop Bot!\n\n"
        "To participate:\n"
        "1. Join our channel\n"
        "2. Join our group\n"
        "3. Follow our Twitter\n"
        "4. Submit your Solana wallet address\n\n"
        "Click ✅ Done after completing all steps",
        reply_markup=reply_markup
    )

async def handle_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)  # Remove buttons
    await query.message.reply_text("📥 Please send your Solana wallet address:")

async def handle_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sol_address = update.message.text
    tx_link = generate_solscan_link()
    
    await update.message.reply_text(
        f"🎉 Congratulations! 1000 SOL is on its way to your wallet!\n\n"
        f"🔗 Transaction: {tx_link}\n\n"
        f"Note: This is a test bot - no actual tokens will be sent."
    )

# ===== Error Handling =====
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error: {context.error}")

# ===== Main Setup =====
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_submission, pattern="^submit$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
