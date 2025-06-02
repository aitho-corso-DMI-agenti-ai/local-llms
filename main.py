from app.base import Game
from app.print import VerboseGamePrinter

def main():
    game = Game(
        agent_model="gemma3:1b",
        printer=VerboseGamePrinter(with_justifications=True),
    )

    game_result = game.play()

    print("################")
    print(f"Final game result: {game_result}")
    print(f"Final conversation:\n\n{game.get_conversation().as_prompt()}")


if __name__ == "__main__":
    main()
