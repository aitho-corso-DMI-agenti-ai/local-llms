from typing import Protocol, runtime_checkable
from pydantic import BaseModel


@runtime_checkable
class GamePrinter(Protocol):
    def print_game_info(self, players, spy_name, location): ...

    def print_question(self, questioner, question): ...

    def print_answer(self, player, answer): ...

    def print_spy_guess(self, spy, guess): ...

    def print_player_guess(self, player_name, guess): ...


class VerboseGamePrinter(BaseModel):
    with_justifications: bool = False

    def print_game_info(self, players, spy_name, location):
        print("## Game info")
        print(f"Players: {[str(player_name) for player_name in players.keys()]}")
        print(f"Spy: {spy_name}")
        print(f"Location: {str(location)}")

    def print_question(self, questioner, question):
        print(
            f"[QUESTION] From {questioner.value} to {question.to_player.value}: {question.content}"
        )
        if self.with_justifications:
            print(f"Justification: {question.justification}")

    def print_answer(self, player, answer):
        print(f"[ANSWER] {player.value}: {answer.content}")
        if self.with_justifications:
            print(f"Justification: {answer.justification}")

    def print_spy_guess(self, spy, guess):
        print(f"[SPY GUESS] From {spy.name} (Spy): {guess.guessed_location}")
        if self.with_justifications:
            print(f"Justification: {guess.justification}")

    def print_player_guess(self, player_name, guess):
        print(f"[PLAYER GUESS] From player {player_name}: {guess.accused_player}")
        if self.with_justifications:
            print(f"Justification: {guess.justification}")


class HumanGamePrinter(BaseModel):
    is_player_spy: bool
    with_justifications: bool = False

    def print_game_info(self, players, spy_name, location):
        print("## Game info")
        print(f"Players: {[str(player_name) for player_name in players.keys()]}")
        if not self.is_player_spy:
            print(f"Location: {str(location)}")
        else:
            print("You are the Spy!")

    def print_question(self, questioner, question):
        print(f"[QUESTION] {questioner.value} asks {question.to_player.value}: {question.content}")
        if self.with_justifications:
            print(f"Justification: {question.justification}")

    def print_answer(self, player, answer):
        print(f"[ANSWER] {player.value} responds: {answer.content}")
        if self.with_justifications:
            print(f"Justification: {answer.justification}")

    def print_spy_guess(self, spy, guess):
        if guess.guessed_location is None:
            print(f"[SPY GUESS] {spy.name} hasn't got an hint for the Secret Location, yet...")
            return

        print(f"[SPY GUESS] {spy.name} (Spy) guesses: {guess.guessed_location}")
        if self.with_justifications:
            print(f"Justification: '{guess.justification}'")

    def print_player_guess(self, player_name, guess):
        if guess.accused_player is None:
            print(f"[PLAYER GUESS] {player_name} is not accusing the Spy, yet...")
            return

        print(f"[PLAYER GUESS] {player_name} guesses: {guess.accused_player}")
        if self.with_justifications:
            print(f"Justification: '{guess.justification}'")
