import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from dialogflow import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger('SupportBot')

DIALOGFLOW_PROJECT_ID = 'support-bot-devman'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialogflow_answer = detect_intent_texts(DIALOGFLOW_PROJECT_ID, update.message.from_user.id, update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=dialogflow_answer)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6317357791:AAHjiOuEKeJMpawK-Why2m-lX1JN6SSVjW0').build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
