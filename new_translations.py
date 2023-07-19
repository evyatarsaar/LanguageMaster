# File path for SQL statements
import sqlite3

from api import TranslationAPI

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
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()

    query = load_sql_statement("check_translation.sql")
    parameters = [text] + list(translations.values())
    cursor.execute(query, parameters)
    result = cursor.fetchone()

    conn.close()

    return result is not None


def add_translation(text, translations):
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()

    query = load_sql_statement("add_translation.sql")
    parameters = [text] + list(translations.values())
    cursor.execute(query, parameters)

    conn.commit()
    conn.close()


def load_sql_statement(file):
    with open(file, "r") as sql_file:
        return sql_file.read()


def new_translation_main_run():
    while True:
        confirm = input("Would you like to add new translation to the DB? \nyes or no").lower()
        if confirm == 'yes':
            text = input("please enter text to translate and add to the DB")
            translate_and_store(text)
        if confirm == 'no':
            print("Thank you for using the app. Goodbye!")
            break
