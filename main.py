import json
import os

from chatbot.engine import ChatBot
from sentiment.analyzer import SentimentAnalyzer
from sentiment.trend import MoodTrend

def main():
    bot = ChatBot()
    analyzer = SentimentAnalyzer()
    trend = MoodTrend()

    print("ChatBot Sentiment Analyzer 🤖")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Bot generates a reply
        bot_response = bot.respond(user_input)
        print(f"Bot: {bot_response}")

        # Store conversation
        bot.store(user_input, bot_response)

        # Track sentiment trend (Tier 2)
        trend.track_message(user_input)


    overall_sentiment = analyzer.analyze_conversation(bot.get_history())
    print(f"\nOverall Conversation Sentiment: {overall_sentiment}")


    print("\nPer-Message Sentiment:")
    for msg, _ in bot.get_history():
        sentiment = analyzer.analyze_message(msg)
        print(f"{msg} → {sentiment}")

    print("\nMood Trend Summary:")
    print(trend.summarize_trend())


    log_data = {
        "conversation": bot.get_history(),
        "overall_sentiment": overall_sentiment,
        "trend_summary": trend.summarize_trend()
    }

    log_path = os.path.join("data", "conversation_log.json")


    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
        if isinstance(existing, list):
            existing.append(log_data)
        else:
            existing = [existing, log_data]
    else:
        existing = [log_data]

    with open(log_path, "w") as f:
        json.dump(existing, f, indent=4)

    print(f"\nConversation appended to {log_path}")


if __name__ == "__main__":
    main()
