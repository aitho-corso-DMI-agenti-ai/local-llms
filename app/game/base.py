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


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    players: dict[Player, PlayerActor]

    _location: Location | None = None
    _spy: Player | None

    def ask_spy_to_guess(self, state: GameState) -> SpyGuess | None:
        spy = self.get_spy()
        guess: SpyGuess = spy.guess_location(state)
        print("-------------")
        print(f"[Game] Player {spy.name} (Spy) guess:")
        print(f"[Game] Guessed location: {guess.guessed_location}")
        print(f"[Game] Justification: {guess.justification}")
        print("-------------")

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
            print("-------------")
            print(f"[Game] Player {player_name} guess:")
            print(f"[Game] Accused player: {guess.accused_player}")
            print(f"[Game] Justification: {guess.justification}")
            print("-------------")

            if guess.accused_player is not None:
                return guess

        return None

    def make_question(self, state: GameState):
        questioner = self.players[state.questioner]
        question: Question = questioner.make_question(state)
        print("-------------")
        print(f"[Game] Question from {state.questioner.value} to {question.to_player.value}:")
        print(f"[Game] Content: {question.content}")
        print(f"[Game] Justification: {question.justification}")
        print("-------------")

        state._question = question

    def answer(self, state: GameState):
        questioner = self.players[state.questioner]
        player = self.players[state._question.to_player]

        answer: Answer = player.answer(state)
        print("-------------")
        print(f"[Game] Answer from player {state._question.to_player.value}:")
        print(f"[Game] Content: {answer.content}")
        print(f"[Game] Justification: {answer.justification}")
        print("-------------")

        state.add_message(state._question.to_game_message(questioner.name))
        state.add_message(answer.to_game_message(questioner.name, player.name))

        state.questioner = state._question.to_player

    def get_spy(self):
        return self.players[self._spy_name]

    def check_spy_guess(self, guess: SpyGuess) -> GameResult:
        if guess.guessed_location == self._location:
            print("[Game] The Spy guessed the location and won!")
            return GameResult(spy_won=True)
        else:
            print(
                f"[Game] The Spy tried to guess the location, but said {guess.guessed_location} while the location was {self._location}!"
            )
            return GameResult(spy_won=False)

    def check_player_guess(self, guess: PlayerGuess) -> GameResult:
        spy = self.get_spy()
        if guess.accused_player.value == spy.name:
            print(f"[Game] {spy.name} was the Spy and has been uncovered!")
            return GameResult(spy_won=False)
        else:
            print(
                f"[Game] The Spy was {spy.name}, but {guess.accused_player} was accused instead!"
            )
            return GameResult(spy_won=True)

    def __print_info(self):
        print("## Game info")
        print(f"Players: {[str(player_name) for player_name in self.players.keys()]}")
        print(f"Spy: {self._spy_name}")
        print(f"Location: {str(self._location)}")

    def play(self):
        first_questioner = random.choice(list(self.players.keys()))
        self._spy_name = random.choice(list(self.players.keys()))
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
