import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv, find_dotenv


def discussing_with_vk(vk_token):
    vk_session = vk_api.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                print('Новое сообщение:')
                if event.to_me:
                    print('Для меня от: ', event.user_id)
                else:
                    print('От меня для: ', event.user_id)
                print('Текст:', event.text)

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    load_dotenv(find_dotenv())
    vk_token = os.environ.get("VK_TOKEN")
    discussing_with_vk(vk_token)


if __name__ == '__main__':
    main()
