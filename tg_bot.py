"""Support Bot for Telegram."""
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts
from logshandler import TGLogsHandler

logger = logging.getLogger('TeleBot')


def main():
    """Main function."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    df_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    admin_tg_bot_token = os.getenv('ADMIN_TG_BOT_TOKEN')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    if admin_tg_bot_token and admin_chat_id:
        logger.addHandler(TGLogsHandler(admin_tg_bot_token, admin_chat_id))
        logger.warning('Successfully began logging into admin chat.')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & ~Filters.command, reply_to_msg)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


def start(update: Update, _: CallbackContext):
    """Send hello message when `/start` command is passed."""
    update.message.reply_text("Привет! Я бот поддержки, чем могу помочь?")


def reply_to_msg(update: Update, _: CallbackContext):
    """Reply to a user message using DialogFlow."""
    df_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    dialogflow_response = detect_intent_texts(df_project_id,
                                              update.message.from_user.id,
                                              update.message.text)
    dialogflow_answer = dialogflow_response.query_result.fulfillment_text
    update.message.reply_text(dialogflow_answer)


if __name__ == '__main__':
    main()
