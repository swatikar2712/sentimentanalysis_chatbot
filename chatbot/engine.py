# chatbot/engine.py

import torch
from sentiment.analyzer import SentimentAnalyzer
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

class ChatBot:
    def __init__(self):
        self.history = []  # Stores tuples of (user_input, bot_response)
        self.analyzer = SentimentAnalyzer()

        # Load BlenderBot model
        model_name = "facebook/blenderbot-400M-distill"
        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

        # Grounding instruction to keep replies focused
        self.system_instruction = (
            "You are a helpful, empathetic chatbot. "
            "Stay focused on the user's input. "
            "Do not invent unrelated topics like dogs, games, or places. "
            "Respond naturally and reflectively."
        )

    def respond(self, user_input):
        # Analyse sentiment (used later in summary)
        sentiment = self.analyzer.analyze_message(user_input)

        # First turn: skip system instruction
        if not self.history:
            grounded_input = user_input
        else:
            grounded_input = self.system_instruction + " " + user_input

        # Encode input
        inputs = self.tokenizer([grounded_input], return_tensors="pt")

        # Generate response
        reply_ids = self.model.generate(**inputs, max_length=200)
        reply = self.tokenizer.decode(reply_ids[0], skip_special_tokens=True)

        # Strip hallucinated phrases
        hallucinated_starts = [
            "Thank you for the advice",
            "I'm guessing",
            "I think he's talking about",
            "I believe the person in the image"
        ]
        for phrase in hallucinated_starts:
            if reply.startswith(phrase):
                reply = "Hmm, could you clarify that a bit more?"

        return reply  

    def store(self, user_input, bot_response):
        self.history.append((user_input, bot_response))

    def get_history(self):
        return self.history
