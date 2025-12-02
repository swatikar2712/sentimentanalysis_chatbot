# gui.py

import tkinter as tk
from chatbot.engine import ChatBot
from sentiment.analyzer import SentimentAnalyzer
from sentiment.trend import MoodTrend

class ChatBotGUI:
    def __init__(self, root):
        self.bot = ChatBot()
        self.analyzer = SentimentAnalyzer()
        self.trend = MoodTrend()

        root.title("Swati's Sentiment Chatbot")
        root.geometry("650x500")

        # Chat display
        self.chat_display = tk.Text(root, bg="black", fg="white", wrap="word")
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input
        self.entry = tk.Entry(root, bg="gray20", fg="white", font=("Arial", 12))
        self.entry.pack(padx=10, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        # Buttons
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_chat)
        self.exit_button.pack(pady=5)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        # Sentiment for this line
        sentiment = self.analyzer.analyze_message(user_input)

        # Display user message with sentiment
        self.chat_display.insert(tk.END, f"You ({sentiment}): {user_input}\n")

        # Track sentiment for trend
        self.trend.track_message(user_input)

        # Get bot response
        bot_response = self.bot.respond(user_input)
        self.bot.store(user_input, bot_response)

        # Display bot response
        self.chat_display.insert(tk.END, f"Bot: {bot_response}\n\n")

        # Clear entry
        self.entry.delete(0, tk.END)

    def exit_chat(self):
        # Overall sentiment + trend summary
        overall_sentiment = self.analyzer.analyze_conversation(self.bot.get_history())
        trend_summary = self.trend.summarize_trend()

        self.chat_display.insert(tk.END, "\n--- Conversation Summary ---\n")
        self.chat_display.insert(tk.END, f"Overall Sentiment: {overall_sentiment}\n")
        self.chat_display.insert(tk.END, f"Mood Trend: {trend_summary}\n\n")

        # Sentence-wise sentiment analysis
        self.chat_display.insert(tk.END, "--- Sentence-wise Sentiment ---\n")
        for idx, (user_input, bot_response) in enumerate(self.bot.get_history(), start=1):
            sentiment = self.analyzer.analyze_message(user_input)
            self.chat_display.insert(tk.END, f"{idx}. {user_input} → {sentiment}\n")

        # Disable input after exit
        self.entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatBotGUI(root)
    root.mainloop()
