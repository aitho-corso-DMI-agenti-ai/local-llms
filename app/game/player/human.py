
from pydantic import BaseModel

from app.game.state import GameState
from app.game.data import Question, Answer, SpyGuess, PlayerGuess, Player, Location

DEFAULT_JUSTIFICATION = "I'm a human, I don't need to justify my choice"

class HumanPlayer(BaseModel):
    name: str

    def communicate_location(self, location: str):
        print(f"The location is: {location}!")

    def is_spy(self) -> bool:
        return True

    def _get_input(self, prompt: str) -> str:
        return input(prompt).strip()

    def make_question(self, state: GameState) -> Question:
        print("Make a question:")
        return Question(
            to_player=Player(self._get_input(f"To which player? (Options: {', '.join(Player)}) ")),
            content=self._get_input("What is your question? "),
            justification=DEFAULT_JUSTIFICATION
        )

    def answer(self, state: GameState) -> Answer:
        print("Answer a question:")
        return Answer(
            content=self._get_input("What is your answer? "),
            justification=DEFAULT_JUSTIFICATION
        )

    def guess_location(self, state: GameState) -> SpyGuess:
        print("Guess the location:")
        location_input = self._get_input(f"Which location do you guess? (Options: {', '.join(Location)}, or press Enter to skip) ")
        if not location_input:
            return SpyGuess(guessed_location=None, justification=DEFAULT_JUSTIFICATION)
        return SpyGuess(
            guessed_location=Location(location_input),
            justification=DEFAULT_JUSTIFICATION
        )

    def guess_spy(self, state: GameState) -> PlayerGuess:
        if self.is_spy():
            return PlayerGuess(accused_player=None, justification=DEFAULT_JUSTIFICATION)

        print("Guess the spy:")
        accused_player = self._get_input(f"Which player do you accuse? (Options: {', '.join(Player)}, or press Enter to skip) ")
        if not accused_player:
            return PlayerGuess(accused_player=None, justification=DEFAULT_JUSTIFICATION)
        return PlayerGuess(
            accused_player=Player(accused_player),
            justification=DEFAULT_JUSTIFICATION
        )
