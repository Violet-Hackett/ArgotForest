import subprocess
import requests

# CMD arguments for setting up local host
LIBRE_CMD = ["libretranslate", "--host", "127.0.0.1", "--port", "5000"]
SERVER_ADDRESS = "http://127.0.0.1:5000/translate"

# Run locally hosted libretranslate server in another process
print("Starting libretranslate server...")
server = subprocess.Popen(
    LIBRE_CMD,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

MAX_ALTERNATIVES = 6
def get_translations(text: str, source_language: str, target_language: str) -> list[str]:
    """
    Gets all translations of the text from the source language to the target language, sorted by relevancy
    
    :param text: Text to translate
    :type text: str
    :param source_language: Abbreviation of the source language
    :type source_language: str
    :param target_language: Abbreviation of the target language
    :type target_language: str
    :return: Ordered list of relevant translations in the target language
    :rtype: list[str]
    """

    # Get server translation response
    response = requests.post(
        SERVER_ADDRESS,
        data={
            "q":text,
            "source": source_language,
            "target": target_language,
            "alternatives": MAX_ALTERNATIVES
        }
    )

    return [response.json()['translatedText']] + response.json()['alternatives']

def terminate_server():
    """
    Terminates the locally hosted libretranslate server
    """
    server.terminate()
    server.wait()