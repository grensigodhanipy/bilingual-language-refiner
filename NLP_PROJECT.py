from googletrans import Translator
import enchant
from nltk.corpus import wordnet

def translate_word(word, source_lang, target_lang):
    translator = Translator()
    translated = translator.translate(word, src=source_lang, dest=target_lang)
    return translated.text

def suggest_english_word(word):
    english_dict = enchant.Dict("en_US")
    suggestions = english_dict.suggest(word)
    
    synonyms = []
    for suggestion in suggestions:
        synsets = wordnet.synsets(suggestion)
        for synset in synsets:
            for lemma in synset.lemmas():
                synonym = lemma.name()
                if synonym != suggestion:  # Ensure the synonym is not the same as the original word
                    synonyms.append(synonym)

    return suggestions, synonyms

def process_sentence(sentence, source_lang, target_lang):
    words = sentence.split()
    processed_words = []

    for word in words:
        english_dict = enchant.Dict("en_US")
        if not english_dict.check(word):  # Check if the word is not in the English dictionary
            english_word = translate_word(word, source_lang, target_lang)
            suggestions, synonyms = suggest_english_word(english_word)
            processed_words.append((word, english_word, suggestions, synonyms))
        else:
            processed_words.append(word)

    return processed_words

def highlight_and_suggest(sentence):
    processed_words = process_sentence(sentence, 'gu', 'en')  # Translate from Gujarati to English
    highlighted_sentence = []

    for item in processed_words:
        if isinstance(item, tuple):
            original_word, english_word, suggestions, synonyms = item
            highlighted_word = f'\033[1;31m{original_word}\033[m'
            highlighted_sentence.append((highlighted_word, english_word, suggestions, synonyms))
        else:
            highlighted_sentence.append(item)

    return highlighted_sentence

def main():
    input_sentence = input("Enter a sentence in English with Gujarati words: ")
    highlighted_and_suggested = highlight_and_suggest(input_sentence)

    for item in highlighted_and_suggested:
        if isinstance(item, tuple):
            highlighted_word, english_word, suggestions, synonyms = item
            print(f"Highlighted: {highlighted_word} | Translated English: {english_word} | Suggestions: {suggestions} | Synonyms: {synonyms}")
        else:
            print(item)

if __name__ == "__main__":
    print("Welcome to our NLP project!")
    main()
