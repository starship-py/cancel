from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, CallbackQueryHandler, filters

# توکن ربات و ID اپراتور
TOKEN = '7199732231:AAHgdhLPwEAFzG0GYtE_cIVSsVVxncCp9oo'
OPERATOR_CHAT_ID = '6548746173'

# مراحل مکالمه
ORDER = range(1)

# دکمه‌های منو
MENU_BUTTONS = [
    [KeyboardButton('سفارش جدید')],
    [KeyboardButton('لغو')]
]

# تابع شروع
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "به ربات خوش آمدید. برای شروع سفارش، دکمه 'سفارش جدید' را فشار دهید.",
        reply_markup=ReplyKeyboardMarkup(MENU_BUTTONS, one_time_keyboard=True)
    )
    return ORDER

# تابع مدیریت سفارش
async def new_order(update: Update, context: CallbackContext) -> int:
    user_message = update.message.text

    # چک کردن سفارش جدید
    if user_message == 'سفارش جدید':
        await update.message.reply_text("لطفاً جزئیات سفارش خود را وارد کنید.")
    elif user_message == 'لغو':
        await update.message.reply_text("سفارش شما لغو شد.")
        return ConversationHandler.END
    else:
        # ارسال سفارش به اپراتور
        keyboard = [
            [
                InlineKeyboardButton("تأیید", callback_data='approve'),
                InlineKeyboardButton("رد", callback_data='deny'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=OPERATOR_CHAT_ID, 
            text=f"درخواست سفارش جدید: {user_message}", 
            reply_markup=reply_markup
        )

        await update.message.reply_text("سفارش شما ارسال شد.")
        return ConversationHandler.END

# تابع تأیید یا رد سفارش توسط اپراتور
async def handle_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'approve':
        await query.edit_message_text(text="درخواست تأیید شد.")
    elif query.data == 'deny':
        await query.edit_message_text(text="درخواست رد شد.")

# تابع لغو
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('سفارش لغو شد.')
    return ConversationHandler.END

# تابع اصلی
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_order)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_approval, pattern='^(approve|deny)$'))

    application.run_polling()

if __name__ == '__main__':
    main()
