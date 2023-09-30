from api import TranslationAPI
translator = TranslationAPI()

text = "Hello"
target_language = "de"  # "de" for German, "es" for Spanish, "nl" for Dutch, etc.

translation = translator.translate(text, target_language)
print(translation)
