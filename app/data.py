from enum import StrEnum

from pydantic import BaseModel, Field


class GameMessage(BaseModel):
    user: str
    message_text: str

    def __str__(self):
        return f"{self.user}: {self.message_text}"


class GameResult(StrEnum):
    SpyGuessedTheLocation = "Spy guessed the location"
    WrongPlayerWasAccused = "Wrong player was accused"

    SpyMissedTheLocation = "Spy missed the location"
    SpyWasUncovered = "Spy was uncovered"



class Player(StrEnum):
    Patrick = "Patrick"
    Teresa = "Teresa"
    Grace = "Grace"
    Kimball = "Kimball"
    Wayne = "Wayne"


class Location(StrEnum):
    University = "University"
    CarWash = "Car Wash"
    Pool = "Pool"
    Library = "Library"
    Bank = "Bank"
    PoliceStation = "Police Station"
    Hospital = "Hospital"
    Supermarket = "Supermarket"
    Cinema = "Cinema"
    Embassy = "Embassy"


class Question(BaseModel):
    to_player: Player = Field(
        description="Name of the player you want to make the question to."
    )
    content: str = Field(description="The content of the question.")
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
    guessed_location: Location | None = Field(default=None)
    justification: str


class PlayerGuess(BaseModel):
    accused_player: Player | None = Field(default=None)
    justification: str

