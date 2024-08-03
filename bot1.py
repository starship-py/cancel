from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# توکن ربات
TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'

async def get_chat_id(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Chat ID: {chat_id}")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_chat_id))

    application.run_polling()

if __name__ == '__main__':
    main()
