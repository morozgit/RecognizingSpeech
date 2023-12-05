import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv, find_dotenv
import random
import vk_api as vk
from google.cloud import dialogflow

def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )

def detect_intent_texts(event, vk_api):
    project_id = 'recognizingspeech'
    session_id = 'temchmorozov'
    language_code = 'ru'
    texts = event.text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    # for text in texts:
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


def discussing_with_vk(vk_token):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
                detect_intent_texts(event, vk_api)
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
