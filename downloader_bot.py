from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
import instaloader
import os

# توکن ربات تلگرام را اینجا وارد کنید
TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'

# ایجاد شیء Instaloader
L = instaloader.Instaloader()

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Download from Instagram", callback_data='instagram')],
        [InlineKeyboardButton("Download from YouTube", callback_data='youtube')],
        [InlineKeyboardButton("Download from TikTok", callback_data='tiktok')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome to the Downloader Bot! Choose an option:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'instagram':
        await query.edit_message_text(text="Please send the Instagram post URL.")
        context.user_data['download_from'] = 'instagram'
    elif query.data == 'youtube':
        await query.edit_message_text(text="Please send the YouTube video URL.")
        context.user_data['download_from'] = 'youtube'
    elif query.data == 'tiktok':
        await query.edit_message_text(text="Please send the TikTok video URL.")
        context.user_data['download_from'] = 'tiktok'

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data.get('download_from')
    if not user_data:
        await update.message.reply_text('Please start the bot by using /start.')
        return

    url = update.message.text
    if user_data == 'instagram':
        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=post.shortcode)
            files = [f for f in os.listdir() if f.startswith(post.shortcode)]
            for file in files:
                with open(file, "rb") as f:
                    await update.message.reply_document(document=f)
            await update.message.reply_text("Instagram post downloaded successfully.")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")

    elif user_data == 'youtube':
        # YouTube download logic here
        await update.message.reply_text("YouTube download is not yet implemented.")

    elif user_data == 'tiktok':
        # TikTok download logic here
        await update.message.reply_text("TikTok download is not yet implemented.")

    # Reset the download option
    context.user_data.pop('download_from', None)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
