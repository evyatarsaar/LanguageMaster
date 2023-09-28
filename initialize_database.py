import sqlite3
from logger_config import logger

# List of 10 basic sentences
sentences = [
    ("Hello", "Hallo", "Hallo", "Hola", "Bonjour"),
    ("How are you?", "Wie geht es dir?", "Hoe gaat het?", "¿Cómo estás?", "Comment ça va?"),
    ("What is your name?", "Wie heißt du?", "Hoe heet je?", "¿Cómo te llamas?", "Comment tu t'appelles?"),
    ("Where are you from?", "Woher kommst du?", "Waar kom je vandaan?", "¿De dónde eres?", "D'où viens-tu?"),
    ("I love you", "Ich liebe dich", "Ik hou van je", "Te amo", "Je t'aime"),
    ("Thank you", "Danke", "Dank je", "Gracias", "Merci"),
    ("Good morning", "Guten Morgen", "Goedemorgen", "Buenos días", "Bonjour"),
    ("Goodbye", "Auf Wiedersehen", "Tot ziens", "Adiós", "Au revoir"),
    ("Yes", "Ja", "Ja", "Sí", "Oui"),
    ("No", "Nein", "Nee", "No", "Non")
]


def initialize_database():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS translations (
                        id INTEGER PRIMARY KEY,
                        original_sentence TEXT,
                        german_translation TEXT,
                        dutch_translation TEXT,
                        spanish_translation TEXT,
                        french_translation TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    for sentence in sentences:
        original, german, dutch, spanish, french = sentence
        cursor.execute('''INSERT INTO translations (original_sentence, german_translation, dutch_translation, spanish_translation, french_translation)
                          VALUES (?, ?, ?, ?, ?)''', (original, german, dutch, spanish, french))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    initialize_database()
    logger.info("Database initialized with 10 basic sentences.")
