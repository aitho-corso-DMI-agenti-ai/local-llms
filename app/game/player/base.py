from typing import Protocol, runtime_checkable
from app.game.state import GameState
from app.game.data import Question, Answer, SpyGuess, PlayerGuess

@runtime_checkable
class PlayerActor(Protocol):
    def make_spy(self):
        ...

    def is_spy(self) -> bool:
        ...

    def make_question(self, state: GameState) -> Question:
        ...

    def answer(self, state: GameState) -> Answer:
        ...

    def guess_location(self, state: GameState) -> SpyGuess:
        ...

    def guess_spy(self, state: GameState) -> PlayerGuess:
        ...