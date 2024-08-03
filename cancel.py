import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات توکن و شناسه چت
TOKEN = os.getenv("TOKEN")
OPERATOR_CHAT_ID = os.getenv("OPERATOR_CHAT_ID")

if not TOKEN:
    raise ValueError("توکن بات در فایل .env مشخص نشده است.")
if not OPERATOR_CHAT_ID:
    raise ValueError("شناسه چت اپراتور در فایل .env مشخص نشده است.")

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! من بات شما هستم.')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('عملیات لغو شد.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('برای کمک به من پیام بدهید.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("help", help_command))

    logger.info("بات در حال اجرا است...")
    application.run_polling()

if __name__ == '__main__':
    main()
