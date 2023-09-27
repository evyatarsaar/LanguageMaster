import sqlite3, random
from api import TranslationAPI
from practice import practice_language
from new_translations import new_translate_main
from logger_config import logger


def main():
    print("Welcome to the Language Learning App!")
    logger.info('Starting the application...')

    while True:
        print("Choose an option:")
        print("1. Practice")
        print("2. Add New Translation")
        print("3. Quit")

        choice = input("Enter the number corresponding to your choice: ")

        if choice == '1':
            practice_language()
        elif choice == '2':
            new_translate_main()
        elif choice == '3':
            logger.info('Application closed.')
            print("Thank you for using the app. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == '__main__':
    main()
