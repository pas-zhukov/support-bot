import logging
import os
import random

from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_texts

logger = logging.getLogger('VKBot')


def main():
    logging.basicConfig(level=logging.DEBUG)

    load_dotenv()
    vk_bot_token = os.getenv('VK_BOT_TOKEN')
    df_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, df_project_id)


def echo(event, vk_api, df_project_id):
    dialogflow_answer = detect_intent_texts(df_project_id, event.user_id, event.text)
    if dialogflow_answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_answer,
            random_id=random.randint(1,1000)
        )


if __name__ == '__main__':
    main()
