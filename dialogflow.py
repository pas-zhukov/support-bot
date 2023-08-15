import logging

from google.cloud import dialogflow
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key

logger = logging.getLogger("DialogFlow")


def create_api_key(project_id: str, suffix: str) -> Key:
    """Creates and restrict an API key.

    Args:
        project_id: Google Cloud project id.
        suffix: your unique key name

    Returns:
        response: Returns the created API Key.
    """
    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    # Initialize request and set arguments.
    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    # Make the request and wait for the operation to complete.
    response = client.create_key(request=request).result()

    print(f"Successfully created an API key: {response.name}")
    # For authenticating with the API key, use the value in "response.key_string".
    # To restrict the usage of this API key, use the value in "response.name".
    return response


def detect_intent_texts(project_id: str,
                        session_id: str or int,
                        text: str,
                        language_code: str = "ru-RU") -> str:
    """Returns the result of detect intent with texts as inputs.

    Args:
        project_id (str): ID of your DialogFlow project
        session_id (str): Unique ID for specific dialogue
        text (str): Text to send to DialogFlow Agent
        language_code (str): Language code in 'en-US' format

    Returns:
        str: DialogFlow Agent answer
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

    return response.query_result.fulfillment_text


if __name__ == "__main__":
    detect_intent_texts("support-bot-devman", "test", "привет железяка", "ru-RU")
