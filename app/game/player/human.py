
from pydantic import BaseModel

from app.game.state import GameState
from app.game.data import Question, Answer, SpyGuess, PlayerGuess, Player, Location, GameRole

DEFAULT_JUSTIFICATION = "I'm a human, I don't need to justify my choice"

class HumanPlayer(BaseModel):
    name: str

    _game_role: GameRole

    def model_post_init(self, context):
        self._game_role = GameRole.PLAYER

    def make_spy(self):
        self._game_role = GameRole.SPY

    def is_spy(self) -> bool:
        return self._game_role == GameRole.SPY

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
        return SpyGuess(
            guessed_location=Location(self._get_input(f"Which location do you guess? (Options: {', '.join(Location)}) ")),
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
