from enum import StrEnum

from pydantic import BaseModel, Field


class GameRole(StrEnum):
    SPY = "spy"
    PLAYER = "player"

class GameMessage(BaseModel):
    user: str
    message_text: str

    def __str__(self):
        return f"{self.user}: {self.message_text}"

class Player(StrEnum):
    Lorenzo = "Lorenzo"
    Stefano = "Stefano"
    Davide = "Davide"
    Alessio = "Alessio"

class Question(BaseModel):
    to_player: Player = Field(description="Name of the player that must reply to the question")
    content: str = Field(description="Content of the question. IMPORTANT: Must be regarding the location of the game.")

    def to_game_message(self, user_name: str) -> GameMessage:
        return GameMessage(
            user = user_name,
            message_text = f"[Question to {self.to_player}] {self.content}"
        )