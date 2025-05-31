from enum import StrEnum, auto

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


class Location(StrEnum):
    University = auto()
    CarWash = auto()
    Pool = auto()
    Library = auto()
    Bank = auto()
    PoliceStation = auto()
    Hospital = auto()
    Supermarket = auto()
    Cinema = auto()
    Embassy = auto()

class Question(BaseModel):
    to_player: Player = Field(description="The name of the player you want to question. It is important it is different from you.")
    content: str
    justification: str

    def to_game_message(self, user_name: str) -> GameMessage:
        return GameMessage(
            user=user_name,
            message_text=f"[Question to {self.to_player}] {self.content}",
        )


class Answer(BaseModel):
    content: str
    justification: str

    def to_game_message(self, questioner_name: str, user_name: str) -> GameMessage:
        return GameMessage(
            user=user_name, message_text=f"[Answer to {questioner_name}] {self.content}"
        )


class SpyGuess(BaseModel):
    guessed_location: Location | None = Field(
        description="Name of the guessed Hidden Location. Must be null if you don't want to provide any guess at the moment."
    )
    justification: str


class PlayerGuess(BaseModel):
    alleged_spy: Player | None= Field(
        description="Name of the player that you think is the Spy. Must be null if you don't want to provide any guess at the moment."
    )
    justification: str


class GameResult(BaseModel):
    spy_won: bool
