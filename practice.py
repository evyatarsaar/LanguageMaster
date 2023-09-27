import random
import sqlite3

from db import DatabaseManager
from utils import load_sql_statement
from logger_config import logger

LANGUAGES = {
    1: "english",
    2: "german",
    3: "dutch",
    4: "spanish",
    5: "french"
}


def practice_language():
    print("Select a language to practice:")
    for num, language in LANGUAGES.items():
        print(f"{num}. {language.capitalize()}")

    while True:
        language_choice = input("Enter the number corresponding to your desired language: ")
        if language_choice.isnumeric() and int(language_choice) in LANGUAGES:
            language = LANGUAGES[int(language_choice)]
            break
        else:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            english_phrase = get_random_english_phrase()

            print(f"English phrase: {english_phrase}")
            confirm = input("Press Enter to see the translation in your chosen language.")

            translation = get_translation(english_phrase, language)
            print(f"{language.capitalize()} translation: {translation}")

            choice = input("Do you want to continue learning? \nEnter 'end' to finish learning.").lower()
            if choice == 'end':
                print("Happy learning, goodbye!")
                break
            print("\n")
            print("---------")
        except Exception as e:
            # Log the exception using the logger
            logger.error(f"An error occurred while practicing: {e}")
            raise


def get_random_english_phrase():
    with DatabaseManager('translations.db') as cursor:
        cursor.execute("SELECT original_sentence FROM translations")
        english_phrases = cursor.fetchall()

    random_phrase = random.choice(english_phrases)
    return random_phrase[0]


def get_translation(english_phrase, target_language):
    target_language += '_translation'
    with DatabaseManager('translations.db') as cursor:
        query_template = load_sql_statement("sql/get_translation.sql")
        query = query_template.format(target_language)
        cursor.execute(query, (english_phrase,))

        translation = cursor.fetchone()[0]

    return translation



