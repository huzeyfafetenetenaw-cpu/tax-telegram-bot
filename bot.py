import os
import pandas as pd
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# Read Excel data
# =========================
df = pd.read_excel("Taxdata.xlsx")

# =========================
# /start command
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "እንኳን ደህና መጡ 👋\n\n"
        "እባክዎ TIN ቁጥርዎን ያስገቡ፦"
    )

# =========================
# Handle TIN input
# =========================
async def handle_tin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tin_input = update.message.text.strip()

    result = df[df["TIN"].astype(str) == tin_input]

    if result.empty:
        await update.message.reply_text(
            "❌ TIN አልተገኘም። እባክዎ እንደገና ይሞክሩ።"
        )
    else:
        row = result.iloc[0]
        message = (
            f"👤 የከፋይ ስም: {row['Taxpayer Name']}\n"
            f"📱 ስልክ: {row['Mobile Phone']}\n"
            f"🏢 የንግድ አይነት: {row['Business Activities']}\n"
            f"💰 መክፈል ያለበት ገንዘብ: {row['Amount']}"
        )
        await update.message.reply_text(message)

# =========================
# Main
# =========================
def main():
    TOKEN = os.environ.get("BOT_TOKEN")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tin))

    app.run_polling()

# =========================
if __name__ == "__main__":
    main()
