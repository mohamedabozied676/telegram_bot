import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging

# Replace 'YOUR_API_TOKEN' with your bot's API token
API_TOKEN = '7043298724:AAGyeN7pOTbK0lnWogg3l-GpGodCJWxjOQg'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Send me a YouTube video URL and I will download it for you!')

async def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    logger.info(f'Received URL: {url}')
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        # Create the 'downloads' directory if it does not exist
        import os
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
        
        logger.info(f'Video downloaded to: {file_path}')
        
        # Send the video to the user
        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video_file)
        
        await update.message.reply_text('Video downloaded and sent!')
    except Exception as e:
        logger.error(f'Error downloading video: {e}')
        await update.message.reply_text(f'Error: {e}')

def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    application.run_polling()

if __name__ == '__main__':
    main()
