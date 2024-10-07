from textblob import TextBlob
import re


def is_bot_like(text):
    # Simple heuristic checks for chatbot-like patterns

    # Check for overly polite or repetitive phrases
    polite_phrases = [
        "I'm sorry", "As a language model", "I can help",
        "I cannot", "Thank you", "I don't have feelings", "As an AI"
    ]

    for phrase in polite_phrases:
        if phrase.lower() in text.lower():
            return True

    # Check for overuse of formal language
    formal_language_patterns = [
        r"\b(?:therefore|however|consequently|furthermore)\b",
        r"\b(?:kind regards|best regards)\b"
    ]

    for pattern in formal_language_patterns:
        if re.search(pattern, text.lower()):
            return True

    # Check for overly structured sentences
    blob = TextBlob(text)
    avg_sentence_length = sum(len(sentence.words) for sentence in blob.sentences) / len(blob.sentences)

    if avg_sentence_length > 20:  # If average sentence is very long, it might be a chatbot
        return True

    # If none of the conditions matched, it's unlikely to be a chatbot
    return False


def main():
    response_text = input("Enter the response to analyze: ")

    if is_bot_like(response_text):
        print("This response has characteristics of a chatbot.")
    else:
        print("This response seems more human-like.")


if __name__ == "__main__":
    main()