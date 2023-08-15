import logging
import os


from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def main():
    logging.basicConfig(level=logging.DEBUG)

    load_dotenv()
    vk_bot_token = os.getenv('VK_BOT_TOKEN')

    vk_session = vk_api.VkApi(token=vk_bot_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()