import random
from pydantic import BaseModel, ConfigDict

from .player import PlayerActor
from .data import (
    Player,
    Question,
    Answer,
    SpyGuess,
    PlayerGuess,
    GameResult,
    Location,
)
from .print import GamePrinter
from .state import ConversationState


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    printer: GamePrinter

    players: dict[Player, PlayerActor]
    spy_name: Player | None = None

    _conversation: ConversationState = ConversationState()
    _questioner_name: Player | None = None
    _location: Location | None = None

    def ask_spy_to_guess(self) -> SpyGuess | None:
        spy = self.get_spy()
        guess: SpyGuess = spy.guess_location(self._conversation)
        self.printer.print_spy_guess(spy, guess)

        if guess.guessed_location is not None:
            return guess
        else:
            return None

    def ask_players_to_guess(self) -> PlayerGuess | None:
        for player_name in self.players:
            player = self.get_player(player_name)
            if player.is_spy():
                continue

            guess: PlayerGuess = player.guess_spy(self._conversation)
            self.printer.print_player_guess(player_name, guess)

            if guess.accused_player is not None:
                return guess

        return None

    def make_question(self):
        question: Question = self.get_player(self._questioner_name).make_question(
            self._conversation
        )
        self.printer.print_question(self._questioner_name, question)
        return question

    def answer(self, question: Question):
        respondent_name = question.to_player

        answer: Answer = self.get_player(respondent_name).answer(
            self._conversation, self._questioner_name, question.content
        )
        self.printer.print_answer(respondent_name, answer)

        self._conversation.add_message(question.to_game_message(self._questioner_name))
        self._conversation.add_message(answer.to_game_message(self._questioner_name, respondent_name))

        self._questioner_name = respondent_name

    def get_spy(self):
        return self.players[self.spy_name]

    def check_spy_guess(self, guess: SpyGuess) -> GameResult:
        spy_won = guess.guessed_location == self._location
        if spy_won:
            print("The Spy guessed the location and won!")
        else:
            print(
                f"The Spy tried to guess the location, but said {guess.guessed_location} while the location was {self._location}!"
            )
        return GameResult(spy_won=spy_won)

    def check_player_guess(self, guess: PlayerGuess) -> GameResult:
        spy = self.get_spy()
        spy_won = guess.accused_player.value != spy.name
        if not spy_won:
            print(f"{spy.name} was the Spy and has been uncovered!")
        else:
            print(
                f"The Spy was {spy.name}, but {guess.accused_player} was accused instead!"
            )
        return GameResult(spy_won=spy_won)


    def get_player(self, name: Player):
        return self.players[name]

    def get_conversation(self) -> ConversationState:
        return self._conversation

    def play(self):
        if self._location is None:
            self._location = random.choice(list(Location))

        if self.spy_name is None:
            self.spy_name = random.choice(list(self.players.keys()))

        for player in self.players.values():
            if player.name != self.spy_name:
                player.communicate_location(self._location)

        self._questioner_name = random.choice(list(self.players.keys()))
        self._conversation = ConversationState()

        self.printer.print_game_info(self.players, self.spy_name, self._location)
        print(f"First questioner: {self._questioner_name}")

        while True:
            question = self.make_question()
            self.answer(question)

            spy_guess = self.ask_spy_to_guess()
            if spy_guess:
                return self.check_spy_guess(spy_guess) 

            player_guess = self.ask_players_to_guess()
            if player_guess:
                return self.check_player_guess(player_guess)
