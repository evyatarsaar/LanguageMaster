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
            english_phrase, translation = get_random_phrase(foreign_language=language)

            print(f"English phrase: {english_phrase}")
            confirm = input("Press Enter to see the translation in your chosen language.")

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


def get_random_phrase(foreign_language, english_column_name='original_sentence'):

    foreign_language_column_name = f'{foreign_language}_translation'
    with DatabaseManager('translations.db') as cursor:
        cursor.execute(f"SELECT {english_column_name}, {foreign_language_column_name}  FROM translations")
        phrases = cursor.fetchall()

    random_phrase = random.choice(phrases)
    logger.info(f"the random phrase selected is:\n{random_phrase}")
    english_phrase = random_phrase[0]
    foreign_language_phrase = random_phrase[1]
    return english_phrase, foreign_language_phrase




