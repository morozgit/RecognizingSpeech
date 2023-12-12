import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv, find_dotenv
import random
import vk_api as vk
from google.cloud import dialogflow
import logging
import telegram


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_texts(event, vk_api, project_id, session_id):
    project_id = project_id
    session_id = session_id
    language_code = 'ru'
    texts = event.text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def discussing_with_vk(vk_token, project_id, session_id):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_texts(event, vk_api, project_id, session_id)



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
