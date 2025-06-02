from pydantic import BaseModel
from typing import List

from .data import GameMessage

class ConversationState(BaseModel):
    _messages: List[GameMessage] = []

    def add_message(self, message: GameMessage):
        self._messages.append(message)

    def as_prompt(self):
        return "\n".join([f"- {str(msg)}" for msg in self._messages])

