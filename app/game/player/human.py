
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

    def make_question(self, state: GameState) -> Question:
        print("Make a question:")
        to_player = input(f"To which player? (Options: {', '.join(Player)}) ").strip()
        content = input("What is your question? ").strip()
        return Question(to_player=Player(to_player), content=content, justification=DEFAULT_JUSTIFICATION)

    def answer(self, state: GameState) -> Answer:
        print("Answer a question:")
        content = input("What is your answer? ").strip()
        return Answer(content=content, justification=DEFAULT_JUSTIFICATION)

    def guess_location(self, state: GameState) -> SpyGuess:
        print("Guess the location:")
        guessed_location = input(f"Which location do you guess? (Options: {', '.join(Location)}) ").strip()
        return SpyGuess(guessed_location=Location(guessed_location), justification=DEFAULT_JUSTIFICATION)

    def guess_spy(self, state: GameState) -> PlayerGuess:
        if self.is_spy():
            return PlayerGuess(accused_player=None, justification=DEFAULT_JUSTIFICATION)

        print("Guess the spy:")
        accused_player = input(f"Which player do you accuse? (Options: {', '.join(Player)}, or press Enter to skip) ").strip()
        if not accused_player:
            return PlayerGuess(accused_player=None, justification=DEFAULT_JUSTIFICATION)
        return PlayerGuess(accused_player=Player(accused_player), justification=DEFAULT_JUSTIFICATION)
