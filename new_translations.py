from api import TranslationAPI
from db import DatabaseManager, check_translation_exists, add_translation_to_db
from requests.exceptions import RequestException
from logger_config import logger

LANGUAGES = {
    # "english": "en",
    "german": "de",
    "dutch": "nl",
    "spanish": "es",
    "french": "fr"
}


# Decorator function to print translations
def print_translations(func):
    def wrapper(text):
        translations = func(text)  # Call the original function

        for language, translation in translations.items():
            print(f"Translation to {language}: {translation}")

        return translations

    return wrapper


def translate_and_store(text):
    try:
        translations = get_translation(text)

        with DatabaseManager('translations.db') as cursor:
            if not check_translation_exists(cursor, text, translations):
                add_translation_to_db(cursor, text, translations)
                logger.info("Translation added to translations.db.")
            else:
                logger.info("Translation already exists in translations.db.")
    except Exception as e:
        # Handle any unexpected errors
        logger.error(f"An unexpected error occurred: {e}")


@print_translations
def get_translation(text):
    translator = TranslationAPI()
    translations = {}

    for language, language_code in LANGUAGES.items():
        try:
            translation = translator.translate(text, language_code)
            translations[language] = translation
        except RequestException as e:
            # Handle API request error
            logger.error(f"Error translating to {language}: {e}")
            translations[language] = "Translation not available due to an error"
        except Exception as e:
            # Handle other unexpected errors
            logger.error(f"An unexpected error occurred: {e}")
            translations[language] = "Translation not available due to an error"

    return translations


def new_translate_main():
    text = input("please enter text to translate and add to the DB")
    translate_and_store(text)
