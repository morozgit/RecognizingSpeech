from google.cloud import dialogflow
from uuid import uuid4


def detect_intent_texts(project_id, texts):
    language_code = 'ru'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, str(uuid4()))
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response