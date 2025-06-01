from typing import Protocol, runtime_checkable
from pydantic import BaseModel


@runtime_checkable
class GamePrinter(Protocol):
    def print_info(self, players, spy_name, location): ...

    def print_question(self, questioner, question): ...

    def print_answer(self, player, answer): ...

    def print_spy_guess(self, spy, guess): ...

    def print_player_guess(self, player_name, guess): ...

    def print_spy_guess_result(self, guess, actual_location, spy_won): ...

    def print_player_guess_result(self, guess, spy_name, spy_won): ...


class VerboseGamePrinter:
    def print_info(self, players, spy_name, location):
        print("## Game info")
        print(f"Players: {[str(player_name) for player_name in players.keys()]}")
        print(f"Spy: {spy_name}")
        print(f"Location: {str(location)}")

    def print_question(self, questioner, question):
        print("-------------")
        print(f"[Game] Question from {questioner.value} to {question.to_player.value}:")
        print(f"[Game] Content: {question.content}")
        print(f"[Game] Justification: {question.justification}")
        print("-------------")

    def print_answer(self, player, answer):
        print("-------------")
        print(f"[Game] Answer from player {player.value}:")
        print(f"[Game] Content: {answer.content}")
        print(f"[Game] Justification: {answer.justification}")
        print("-------------")

    def print_spy_guess(self, spy, guess):
        print("-------------")
        print(f"[Game] Player {spy.name} (Spy) guess:")
        print(f"[Game] Guessed location: {guess.guessed_location}")
        print(f"[Game] Justification: {guess.justification}")
        print("-------------")

    def print_player_guess(self, player_name, guess):
        print("-------------")
        print(f"[Game] Player {player_name} guess:")
        print(f"[Game] Accused player: {guess.accused_player}")
        print(f"[Game] Justification: {guess.justification}")
        print("-------------")

    def print_spy_guess_result(self, guess, actual_location, spy_won):
        if spy_won:
            print("[Game] The Spy guessed the location and won!")
        else:
            print(
                f"[Game] The Spy tried to guess the location, but said {guess.guessed_location} while the location was {actual_location}!"
            )

    def print_player_guess_result(self, guess, spy_name, spy_won):
        if not spy_won:
            print(f"[Game] {spy_name} was the Spy and has been uncovered!")
        else:
            print(
                f"[Game] The Spy was {spy_name}, but {guess.accused_player} was accused instead!"
            )


class HumanGamePrinter(BaseModel):
    is_player_spy: bool

    def print_info(self, players, spy_name, location):
        print("## Game info")
        print(f"Players: {[str(player_name) for player_name in players.keys()]}")
        if not self.is_player_spy:
            print(f"Location: {str(location)}")
        else:
            print("You are the Spy!")

    def print_question(self, questioner, question):
        print("-------------")
        print(f"[Game] Question from {questioner.value} to {question.to_player.value}:")
        print(f"[Game] Content: {question.content}")
        print("-------------")

    def print_answer(self, player, answer):
        print("-------------")
        print(f"[Game] Answer from player {player.value}:")
        print(f"[Game] Content: {answer.content}")
        print("-------------")

    def print_spy_guess(self, spy, guess):
        if guess.guessed_location is None:
            return

        print("-------------")
        print(f"[Game] Player {spy.name} (Spy) guess:")
        print(f"[Game] Guessed location: {guess.guessed_location}")
        print(f"[Game] Justification: {guess.justification}")
        print("-------------")

    def print_player_guess(self, player_name, guess):
        if guess.accused_player is None:
            return

        print("-------------")
        print(f"[Game] Player {player_name} guess:")
        print(f"[Game] Accused player: {guess.accused_player}")
        print(f"[Game] Justification: {guess.justification}")
        print("-------------")

    def print_spy_guess_result(self, guess, actual_location, spy_won):
        if spy_won:
            print("[Game] The Spy guessed the location and won!")
        else:
            print(
                f"[Game] The Spy tried to guess the location, but said {guess.guessed_location} while the location was {actual_location}!"
            )

    def print_player_guess_result(self, guess, spy_name, spy_won):
        if not spy_won:
            print(f"[Game] {spy_name} was the Spy and has been uncovered!")
        else:
            print(
                f"[Game] The Spy was {spy_name}, but {guess.accused_player} was accused instead!"
            )
