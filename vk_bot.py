import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv, find_dotenv
import random
import vk_api as vk
import telegram
from tg_logs_handler import TelegramLogsHandler
from dialogflow_api import detect_intent_texts


def send_massage(event, vk_api, project_id, session_id):
    texts = event.text
    answer = detect_intent_texts(project_id, session_id, texts)
    if not answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def discussing_with_vk(vk_token, project_id, session_id):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_massage(event, vk_api, project_id, session_id)


def main():
    load_dotenv(find_dotenv())
    project_id = os.environ.get("PROJECT_ID")
    session_id = os.environ.get("SESSION_ID")
    vk_token = os.environ.get("VK_TOKEN")
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.environ.get("TG_CHAT_ID")

    bot = telegram.Bot(token=tg_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    bot.logger.warning('VK Бот запущен')
    try:
        discussing_with_vk(vk_token, project_id, session_id)
    except Exception as err:
        error = f'VK Бот упал с ошибкой {str(err)}'
        bot.logger.warning(error)


if __name__ == '__main__':
    main()
