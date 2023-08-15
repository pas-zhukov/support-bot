"""Support Bot for VK social net."""
import logging
import os
import random

from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_texts
from logshandler import TGLogsHandler

logger = logging.getLogger('VKBot')


def main():
    """Main function."""
    logging.basicConfig(level=logging.WARNING)

    load_dotenv()
    vk_bot_token = os.getenv('VK_BOT_TOKEN')
    df_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    admin_tg_bot_token = os.getenv('ADMIN_TG_BOT_TOKEN')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    if admin_tg_bot_token and admin_chat_id:
        logger.addHandler(TGLogsHandler(admin_tg_bot_token, admin_chat_id))
        logger.warning('Successfully began logging into admin chat.')

    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer_msg(event, vk_api, df_project_id)


def answer_msg(event, vk_api, df_project_id):
    """Reply to users message using DialogFlow.

    Replies only if DialogFlow response not in fallback.
    """
    dialogflow_response = detect_intent_texts(df_project_id,
                                              event.user_id,
                                              event.text)
    if not dialogflow_response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    main()
