import json
import os

from ai import generate


class AppState:

    def __init__(self):
        self.file = "chat_history.json"
        self.messages = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })
        self.save()

    def ask_ai(self):
        return generate(self.messages)
