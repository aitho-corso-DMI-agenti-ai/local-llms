from enum import StrEnum

from pydantic import BaseModel
from typing import List

class GameRole(StrEnum):
    SPY = "spy"
    PLAYER = "player"

class GameMessage(BaseModel):
    user: str
    message_text: str

    def __str__(self):
        return f"{self.user}: {self.message_text}"

class GameState(BaseModel):
    messages: List[GameMessage] = []

    def add_message(self, message: GameMessage):
        self.messages.append(message)
        
    def __str__(self):
        messages_str = '\n'.join(str(message) for message in self.messages)
        return f"GameState(messages={messages_str})"
