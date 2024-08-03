from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, filters

# توکن ربات و ID اپراتور
TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'
OPERATOR_CHAT_ID = '6548746173'

# مراحل مکالمه
LOGIN, WAITING_PASSWORD, MENU, NEW_ORDER, ORDER_HISTORY, POST_NEW = range(6)

# داده‌های نمونه برای سفارشات
orders = []

# دکمه‌های منو
MENU_BUTTONS = {
    'سفارش جدید': 'new_order',
    'تاریخچه سفارشات': 'order_history',
    'پست کردن مطلب جدید': 'post_new'
}

# تابع شروع
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "لطفا نام کاربری را وارد کنید.",
        reply_markup=ReplyKeyboardMarkup([['/cancel']], one_time_keyboard=True)
    )
    return LOGIN

# تابع ورود - نام کاربری
async def login_username(update: Update, context: CallbackContext) -> int:
    context.user_data['username'] = update.message.text
    await update.message.reply_text("لطفا رمز عبور را وارد کنید.")
    return WAITING_PASSWORD

# تابع ورود - رمز عبور
async def login_password(update: Update, context: CallbackContext) -> int:
    username = context.user_data.get('username')
    password = update.message.text
    if username == 'admin' and password == 'pass':
        keyboard = [[KeyboardButton(text=btn)] for btn in MENU_BUTTONS.keys()]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text("به پنل مدیریت خوش آمدید. لطفاً یکی از گزینه‌ها را انتخاب کنید.", reply_markup=reply_markup)
        return MENU
    else:
        await update.message.reply_text("نام کاربری یا رمز عبور نادرست است. لطفاً دوباره تلاش کنید.")
        return LOGIN

# تابع منو
async def menu(update: Update, context: CallbackContext) -> int:
    query = update.message.text
    if query == 'سفارش جدید':
        await update.message.reply_text("در حال نمایش سفارشات جدید...")
        return NEW_ORDER
    elif query == 'تاریخچه سفارشات':
        await update.message.reply_text("در حال نمایش تاریخچه سفارشات...")
        return ORDER_HISTORY
    elif query == 'پست کردن مطلب جدید':
        await update.message.reply_text("لطفا متن مطلب جدید را وارد کنید.")
        return POST_NEW
    else:
        await update.message.reply_text("گزینه نامعتبر است.")
        return MENU

# تابع نمایش سفارش جدید
async def new_order(update: Update, context: CallbackContext) -> int:
    # در اینجا باید منطق برای نمایش سفارشات جدید اضافه شود
    await update.message.reply_text("این بخش برای نمایش و مدیریت سفارشات جدید است.")
    return MENU

# تابع نمایش تاریخچه سفارشات
async def order_history(update: Update, context: CallbackContext) -> int:
    if orders:
        history = '\n'.join(orders)
        await update.message.reply_text(f"تاریخچه سفارشات:\n{history}")
    else:
        await update.message.reply_text("هیچ سفارشی ثبت نشده است.")
    return MENU

# تابع پست کردن مطلب جدید
async def post_new(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    # در اینجا باید منطق برای پست کردن مطلب جدید اضافه شود
    await update.message.reply_text(f"مطلب جدید شما ثبت شد:\n{text}")
    return MENU

# تابع اصلی
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_username)],
            WAITING_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
            NEW_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_order)],
            ORDER_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_history)],
            POST_NEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, post_new)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
