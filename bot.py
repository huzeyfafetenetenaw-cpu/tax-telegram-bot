import os
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Read Excel data
df = pd.read_excel("Taxdata.xlsx")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "እንኳን ደህና መጡ 👋\n\n"
        "እባክዎ TIN ቁጥርዎን ያስገቡ፦"
    )

async def handle_tin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tin = update.message.text.strip()

    result = df[df["TIN"].astype(str) == tin]

    if result.empty:
        await update.message.reply_text("❌ TIN አልተገኘም። እባክዎ ዳግመኛ ይሞክሩ።")
    else:
        row = result.iloc[0]
        message = (
            f"👤 ስም: {row['Name']}\n"
            f"💰 የሚከፈል መጠን: {row['Amount']}\n"
            f"🏦 የክፍያ ኮድ: {row['PaymentCode']}"
        )
        await update.message.reply_text(message)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tin))

    app.run_polling()

if __name__ == "__main__":
    main()
