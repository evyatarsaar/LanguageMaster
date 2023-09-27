from api import TranslationAPI
from db import DatabaseManager, check_translation_exists, add_translation_to_db

LANGUAGES = {
    # "english": "en",
    "german": "de",
    "dutch": "nl",
    "spanish": "es",
    "french": "fr"
}


def translate_and_store(text):
    translations = get_translation(text)

    if not translation_exists(text, translations):
        add_translation(text, translations)
        print("Translation added to translations.db.")
    else:
        print("Translation already exists in translations.db.")


def get_translation(text):
    translator = TranslationAPI()
    translations = {}

    for language, language_code in LANGUAGES.items():
        translation = translator.translate(text, language_code)
        translations[language] = translation

    return translations


def translation_exists(text, translations):
    with DatabaseManager('translations.db') as cursor:
        return check_translation_exists(cursor, text, translations)


def add_translation(text, translations):
    with DatabaseManager('translations.db') as cursor:
        add_translation(cursor, text, translations)


def new_translation_main_run():
    while True:
        confirm = input("Would you like to add new translation to the DB? \nyes or no").lower()
        if confirm == 'yes':
            text = input("please enter text to translate and add to the DB")
            translate_and_store(text)
        if confirm == 'no':
            print("Thank you for using the app. Goodbye!")
            break
