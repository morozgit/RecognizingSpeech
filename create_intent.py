import argparse
import os
from google.cloud import dialogflow
import json
from dotenv import load_dotenv, find_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))

def main():
    load_dotenv(find_dotenv())
    project_id = os.environ.get("PROJECT_ID")
    parser = argparse.ArgumentParser(description='Скрипт загрузит тренировочные фразы')
    parser.add_argument('trainer', help='Укажите путь к файлу')
    trainer = parser.parse_args().trainer
    with open(trainer, "r") as file:
        training_phrases_json = file.read()

    training_phrases = json.loads(training_phrases_json)
    for topic, training_phrase in training_phrases.items():
        work_questions = training_phrase['questions']
        work_answer = training_phrase['answer']
        create_intent(project_id, topic, work_questions, [work_answer])

if __name__ == '__main__':
    main()