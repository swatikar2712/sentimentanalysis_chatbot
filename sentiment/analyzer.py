# sentiment/analyzer.py

from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        pass

    def analyze_message(self, text):
        """
        Analyze sentiment of a single message.
        Returns: 'Positive', 'Negative', or 'Neutral'
        """
        stripped = text.strip()
        word_count = len(stripped.split())

        # Override for ultra-short inputs (1 word or < 5 characters)
        if word_count == 1 or len(stripped) < 5:
            return "Neutral"

        polarity = TextBlob(stripped).sentiment.polarity

        # Stricter thresholds to avoid false positives
        if polarity > 0.2:
            return "Positive"
        elif polarity < -0.2:
            return "Negative"
        else:
            return "Neutral"

    def analyze_conversation(self, history):
        """
        Analyze sentiment across all user messages in the conversation.
        history: list of (user_input, bot_response) tuples
        Returns: overall sentiment label
        """
        if not history:
            return "Neutral"

        total_polarity = 0
        count = 0

        for user_input, _ in history:
            polarity = TextBlob(user_input.strip()).sentiment.polarity
            total_polarity += polarity
            count += 1

        avg_polarity = total_polarity / count

        if avg_polarity > 0.2:
            return "Overall Positive"
        elif avg_polarity < -0.2:
            return "Overall Negative"
        else:
            return "Overall Neutral"
