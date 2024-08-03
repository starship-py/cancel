from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# توکن ربات شما
TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'

# تابع برای دریافت اطلاعات رمز ارز
def get_crypto_info(crypto_id):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}'
    response = requests.get(url)
    data = response.json()
    return data['name'], data['market_data']['current_price']['usd']

# تابع برای ارسال کیبورد با دکمه‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton('Bitcoin')],
        [KeyboardButton('Ethereum')],
        [KeyboardButton('Ripple')],
        [KeyboardButton('Litecoin')],
        [KeyboardButton('Cardano')],
        [KeyboardButton('Polkadot')],
        [KeyboardButton('Stellar')],
        [KeyboardButton('Chainlink')],
        [KeyboardButton('Binance Coin')],
        [KeyboardButton('Dogecoin')],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('لطفاً یکی از رمز ارزها را انتخاب کنید:', reply_markup=reply_markup)

# تابع برای پردازش دکمه‌های انتخاب شده
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    crypto_id_map = {
        'Bitcoin': 'bitcoin',
        'Ethereum': 'ethereum',
        'Ripple': 'ripple',
        'Litecoin': 'litecoin',
        'Cardano': 'cardano',
        'Polkadot': 'polkadot',
        'Stellar': 'stellar',
        'Chainlink': 'chainlink',
        'Binance Coin': 'binancecoin',
        'Dogecoin': 'dogecoin'
    }
    
    if query in crypto_id_map:
        crypto_id = crypto_id_map[query]
        try:
            name, price = get_crypto_info(crypto_id)
            await update.message.reply_text(f"قیمت {name} در حال حاضر ${price}")
        except Exception as e:
            await update.message.reply_text(f"مشکلی در دریافت اطلاعات وجود دارد: {e}")
    else:
        await update.message.reply_text("رمز ارز ناشناخته است.")

# تابع اصلی برای شروع ربات
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # افزودن هندلر برای دستور /start
    application.add_handler(CommandHandler("start", start))

    # افزودن هندلر برای دکمه‌های کیبورد
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button))

    # اجرای ربات
    application.run_polling()

if __name__ == '__main__':
    main()