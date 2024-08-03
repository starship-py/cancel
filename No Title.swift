from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
import logging

# تنظیمات اولیه
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# مراحل ثبت نام
NAME, PHONE, VERIFICATION, PAYMENT, COMPLETE = range(5)

# توکن ربات
TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'

# استارت ربات
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("فروشگاه اکانت", callback_data='store')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('به کنسل استور خوش آمدید!', reply_markup=reply_markup)

# مرحله فروشگاه
def store(update: Update, context):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("اپل ایدی", callback_data='apple_id')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('لطفاً یکی از گزینه‌های زیر را انتخاب کنید:', reply_markup=reply_markup)

# مرحله اپل ایدی
def apple_id(update: Update, context):
    query = update.callback_query
    query.message.reply_text('لطفاً نام و نام خانوادگی خود را وارد کنید:')
    return NAME

# دریافت نام
def name(update: Update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text('لطفاً شماره موبایل خود را وارد کنید:')
    return PHONE

# دریافت شماره موبایل
def phone(update: Update, context):
    context.user_data['phone'] = update.message.text
    # ارسال اطلاعات به سرور
    # اینجا باید کد ارسال اطلاعات به سرور نوشته شود
    update.message.reply_text('کد ارسال شده را وارد کنید:')
    return VERIFICATION

# دریافت کد تایید
def verification(update: Update, context):
    context.user_data['verification'] = update.message.text
    # ارسال کد تایید به سرور
    # اینجا باید کد ارسال کد تایید به سرور نوشته شود
    update.message.reply_text('لطفاً فیش واریزی خود را ارسال کنید:')
    return PAYMENT

# دریافت فیش واریزی
def payment(update: Update, context):
    # ارسال فیش به سرور
    # اینجا باید کد ارسال فیش به سرور نوشته شود
    update.message.reply_text('اپل ایدی شما در حال ساخت است.')
    return COMPLETE

# اتمام فرآیند
def complete(update: Update, context):
    update.message.reply_text('اپل ایدی شما ساخته شد. با تشکر از شما.')
    return ConversationHandler.END

# لغو فرآیند
def cancel(update: Update, context):
    update.message.reply_text('فرآیند لغو شد.')
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
            VERIFICATION: [MessageHandler(Filters.text & ~Filters.command, verification)],
            PAYMENT: [MessageHandler(Filters.document & ~Filters.command, payment)],
            COMPLETE: [MessageHandler(Filters.text & ~Filters.command, complete)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(store, pattern='store'))
    dp.add_handler(CallbackQueryHandler(apple_id, pattern='apple_id'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
