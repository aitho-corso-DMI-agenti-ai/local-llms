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
from .state import GameState
from .print import GamePrinter

class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    printer: GamePrinter 

    players: dict[Player, PlayerActor]
    spy_name: Player | None = None

    _location: Location | None = None

    def ask_spy_to_guess(self, state: GameState) -> SpyGuess | None:
        spy = self.get_spy()
        guess: SpyGuess = spy.guess_location(state)
        self.printer.print_spy_guess(spy, guess)

        if guess.guessed_location is not None:
            return guess
        else:
            return None

    def ask_players_to_guess(self, state: GameState) -> PlayerGuess | None:
        for player_name in self.players:
            player = self.players[player_name]
            if player.is_spy():
                continue

            guess: PlayerGuess = player.guess_spy(state)
            self.printer.print_player_guess(player_name, guess)

            if guess.accused_player is not None:
                return guess

        return None

    def make_question(self, state: GameState):
        questioner = self.players[state.questioner]
        question: Question = questioner.make_question(state)
        self.printer.print_question(state.questioner, question)

        state._question = question

    def answer(self, state: GameState):
        questioner = self.players[state.questioner]
        player = self.players[state._question.to_player]

        answer: Answer = player.answer(state)
        self.printer.print_answer(state._question.to_player, answer)

        state.add_message(state._question.to_game_message(questioner.name))
        state.add_message(answer.to_game_message(questioner.name, player.name))

        state.questioner = state._question.to_player

    def get_spy(self):
        return self.players[self.spy_name]

    def check_spy_guess(self, guess: SpyGuess) -> GameResult:
        spy_won = guess.guessed_location == self._location
        self.printer.print_spy_guess_result(guess, self._location, spy_won)
        return GameResult(spy_won=spy_won)

    def check_player_guess(self, guess: PlayerGuess) -> GameResult:
        spy = self.get_spy()
        spy_won = guess.accused_player.value != spy.name
        self.printer.print_player_guess_result(guess, spy.name, spy_won)
        return GameResult(spy_won=spy_won)

    def __print_info(self):
        self.printer.print_info(self.players, self.spy_name, self._location)

    def play(self):
        first_questioner = random.choice(list(self.players.keys()))
        if self.spy_name is None:
            self.spy_name = random.choice(list(self.players.keys()))

        self.get_spy().make_spy()

        if self._location is None:
            self._location = random.choice(list(Location))

        state = GameState(location=self._location, questioner=first_questioner)

        self.__print_info()

        turns = 0
        while True:
            turns += 1

            self.make_question(state)
            self.answer(state)

            print("## Spy guess")
            spy_guess = self.ask_spy_to_guess(state)
            if spy_guess:
                return self.check_spy_guess(spy_guess), state
            print("------------")

            print("## Player guesses")
            player_guess = self.ask_players_to_guess(state)
            if player_guess:
                return self.check_player_guess(player_guess), state
            print("-----------------")

            if turns == 5:
                return GameResult(spy_won=True), state