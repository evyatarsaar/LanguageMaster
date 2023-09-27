import sqlite3, random
from api import TranslationAPI
from practice import practice_main_run
from new_translations import new_translation_main_run
from logger_config import logger


def main():
    print("Welcome to the Language Learning App!")
    logger.info('Starting the application...')
    practice_main_run()
    new_translation_main_run()


if __name__ == '__main__':
    main()
