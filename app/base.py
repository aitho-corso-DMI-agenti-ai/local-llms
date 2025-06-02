import random
from pydantic import BaseModel, ConfigDict

from .player import PlayerActor, HumanPlayer, AgentPlayer
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
    agent_model: str

    spy_name: Player | None = None
    human_name: Player | None = None

    _players: dict[Player, PlayerActor] = None
    _conversation: ConversationState = ConversationState()
    _questioner_name: Player | None = None
    _location: Location | None = None

    def model_post_init(self, context):
        self.spy_name = self.spy_name or random.choice(list(Player))
        self._location = random.choice(list(Location))

        self.__init_players()

        for player in self._players.values():
            if player.name != self.spy_name:
                player.communicate_location(self._location)

        self._questioner_name = random.choice(list(Player))
        self._conversation = ConversationState()

    def __init_players(self):
        self._players = dict()
        for player_name in Player:
            if player_name.value == self.human_name:
                self._players[player_name] = HumanPlayer(name=player_name.value)
            else:
                self._players[player_name] = AgentPlayer(
                    model=self.agent_model, name=player_name.value
                )

    def ask_spy_to_guess(self) -> SpyGuess | None:
        spy = self.get_spy()
        guess: SpyGuess = spy.guess_location(self._conversation)
        self.printer.print_spy_guess(spy, guess)

        if guess.guessed_location is not None:
            return guess
        else:
            return None

    def ask_players_to_guess(self) -> PlayerGuess | None:
        for player_name in self._players:
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
        self._conversation.add_message(
            answer.to_game_message(self._questioner_name, respondent_name)
        )

        self._questioner_name = respondent_name

    def check_spy_guess(self, guess: SpyGuess) -> GameResult:
        if guess.guessed_location == self._location:
            print("The Spy guessed the location and won!")
            return GameResult.SpyGuessedTheLocation
        else:
            print(
                f"The Spy tried to guess the location, but said {guess.guessed_location} while the location was {self._location}!"
            )
            return GameResult.SpyMissedTheLocation

    def check_player_guess(self, guess: PlayerGuess) -> GameResult:
        spy = self.get_spy()
        if guess.accused_player.value == spy.name:
            print(f"{spy.name} was the Spy and has been uncovered!")
            return GameResult.SpyWasUncovered
        else:
            print(
                f"The Spy was {spy.name}, but {guess.accused_player} was accused instead!"
            )
            return GameResult.WrongPlayerWasAccused

    def get_spy(self):
        return self._players[self.spy_name]

    def get_player(self, name: Player):
        return self._players[name]

    def get_conversation(self) -> ConversationState:
        return self._conversation

    def play(self):
        self.printer.print_game_info(self._players, self.spy_name, self._location)
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
