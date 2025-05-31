from pydantic import BaseModel
from typing import List


from .data import GameMessage, Player

class GameState(BaseModel):
    messages: List[GameMessage] = []
    location: str
    current_player: Player

    @staticmethod
    def init(location: str, first_player: Player):
        return GameState(
            messages=list(), location=location, current_player=first_player
        )

    def print(self):
        print("Current game state:")
        print(self)

    def add_message(self, message: GameMessage):
        self.messages.append(message)

    def conversation_prompt(self):
        output = "Previous messages: "
        output += "\n".join([str(msg) for msg in self.messages])
        return output

    def __str__(self):
        messages_str = "\n".join(str(message) for message in self.messages)
        return f"GameState\nMessages:\n\n----{messages_str}----)"