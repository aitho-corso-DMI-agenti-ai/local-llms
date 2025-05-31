from enum import StrEnum, auto

from pydantic import BaseModel


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


class Location(StrEnum):
    University = auto()
    CarWash = auto()
    Pool = auto()

class Question(BaseModel):
    to_player: Player
    content: str
    justification: str

    def to_game_message(self, user_name: str) -> GameMessage:
        return GameMessage(
            user = user_name,
            message_text = f"[Question to {self.to_player}] {self.content}"
        )

class Answer(BaseModel):
    content: str
    justification: str

    def to_game_message(self, questioner_name: str, user_name: str) -> GameMessage:
        return GameMessage(
            user = user_name,
            message_text = f"[Answer to {questioner_name}] {self.content}"
        )

class SpyGuess(BaseModel):
    guessed_location: Location | None
    justification: str

class PlayerGuess(BaseModel):
    alleged_spy: Player | None
    justification: str


class GameResult(BaseModel):
    spy_won: bool
