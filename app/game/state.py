from pydantic import BaseModel
from typing import List

from .data import GameMessage, Player, Question


class GameState(BaseModel):
    location: str
    questioner: Player

    _messages: List[GameMessage] = []
    _question: Question | None = None

    def print(self):
        print("## Current game state:")
        print(self)

    def add_message(self, message: GameMessage):
        self._messages.append(message)

    def conversation_prompt(self):
        output = "Previous messages: "
        output += "\n".join([str(msg) for msg in self._messages])
        return output

    def __str__(self):
        messages_str = "\n".join(str(message) for message in self._messages)
        return f"GameState\nMessages:\n\n----\n{messages_str}\n----"
