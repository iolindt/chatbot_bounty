import json
import re
from datetime import datetime
from collections import defaultdict


class Memory:
    def __init__(self, file="memory.json"):
        self.file = file
        self.data = self.load()

    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except:
            return {"history": []}

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add(self, user, bot):
        self.data["history"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "bot": bot
        })
        self.save()


class IntentEngine:
    def __init__(self):
        self.patterns = {
            "greeting": r"\b(hi|hello|hey)\b",
            "bye": r"\b(bye|goodbye|see you)\b",
            "crypto": r"\b(crypto|bitcoin|web3|blockchain)\b",
            "help": r"\b(help|support|how)\b"
        }

    def detect(self, text):
        for intent, pattern in self.patterns.items():
            if re.search(pattern, text.lower()):
                return intent
        return "unknown"


class Chatbot:
    def __init__(self):
        self.memory = Memory()
        self.intent_engine = IntentEngine()
        self.responses = self._load_responses()

    def _load_responses(self):
        return {
            "greeting": [
                "Hey! How can I help you?",
                "Hello! What’s up?"
            ],
            "bye": [
                "Goodbye! 👋",
                "See you later!"
            ],
            "crypto": [
                "Crypto is evolving fast. Are you learning or building?",
                "Web3 is interesting. What part are you exploring?"
            ],
            "help": [
                "Sure, tell me what you need help with.",
                "I can help — just ask your question."
            ],
            "unknown": [
                "Hmm, I’m not sure I understand.",
                "Can you rephrase that?"
            ]
        }

    def generate_response(self, text):
        intent = self.intent_engine.detect(text)
        return self._pick_response(intent)

    def _pick_response(self, intent):
        import random
        return random.choice(self.responses[intent])

    def chat(self):
        print("=== Smart Chatbot === (type 'exit' to quit)")

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                print("Bot: Bye!")
                break

            response = self.generate_response(user_input)
            print("Bot:", response)

            self.memory.add(user_input, response)


if __name__ == "__main__":
    bot = Chatbot()
    bot.chat()
