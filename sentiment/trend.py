from textblob import TextBlob

class MoodTrend:
    def __init__(self):
        self.scores = []  # store polarity values for each user message

    def track_message(self, text):
        """
        Track sentiment polarity for a single message.
        """
        polarity = TextBlob(text).sentiment.polarity
        self.scores.append(polarity)
        return polarity

    def summarize_trend(self):
        """
        Summarize mood trend across the conversation.
        Returns a string describing the shift in sentiment.
        """
        if not self.scores:
            return "No sentiment data available."

        start = self.scores[0]
        end = self.scores[-1]

        def label(p):
            if p > 0.1:
                return "Positive"
            elif p < -0.1:
                return "Negative"
            else:
                return "Neutral"

        start_label = label(start)
        end_label = label(end)

        if start_label == end_label:
            return f"Mood remained {start_label} throughout."
        else:
            return f"Mood shifted from {start_label} to {end_label}."
