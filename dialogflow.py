"""Functions for interacting with DialogFlow API."""
import os
from argparse import ArgumentParser
import json
import logging
import validators

from dotenv import load_dotenv
from google.cloud import dialogflow
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
import requests


logger = logging.getLogger("DialogFlow")


def create_api_key(project_id: str, suffix: str) -> Key:
    """Creates and restrict an API key.

    Args:
        project_id: Google Cloud project id.
        suffix: your unique key name

    Returns:
        response: Returns the created API Key.
    """
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response


def detect_intent_texts(project_id: str,
                        session_id: str or int,
                        text: str,
                        language_code: str = "ru-RU") -> dialogflow.DetectIntentResponse:
    """Return the result of detect intent with text as input.

    Returns False if DialogFlow Bot is in Fallback.

    Args:
        project_id (str): ID of your DialogFlow project
        session_id (str): Unique ID for specific dialogue
        text (str): Text to send to DialogFlow Agent
        language_code (str): Language code in 'en-US' format

    Returns:
        DetectIntentResponse: DialogFlow Agent response
    """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    logger.debug("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    logger.debug("Query text: {}".format(response.query_result.query_text))
    logger.debug(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    logger.debug("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    return response


def create_intent(project_id: str,
                  display_name: str,
                  training_phrases_parts: list[str],
                  message_texts: list[str]):
    """Create an intent of the given intent type.

    Args:
        project_id (str): ID of your DialogFlow project
        display_name (str): The Name of Intent
        training_phrases_parts (list[str]): List of phrases you expect from users
        message_texts (list[str]): List of answers for this intent

    """
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(display_name=display_name,
                               training_phrases=training_phrases,
                               messages=[message])
    response = intents_client.create_intent(request={"parent": parent, "intent": intent})
    logger.debug("Intent created: {}".format(response))


if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    arg_parser = ArgumentParser(
        description='Скрипт для автозагрузки интентов в агента DialogFlow'
    )
    arg_parser.add_argument(
        'jf',
        help="Путь/ссылка к Вашему json-файлу.",
        type=str,
        default='https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    )
    args = arg_parser.parse_args()
    file_source = args.jf

    if validators.url(file_source):
        response = requests.get(file_source)
        response.raise_for_status()
        training_questions = response.json()
    else:
        try:
            with open(file_source, 'rb') as file:
                training_questions = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError('File not found! Check the JSON source path!')

    for topic, intent in training_questions.items():
        questions = intent['questions']
        answer = intent['answer']
        create_intent(project_id, topic, questions, [answer])
