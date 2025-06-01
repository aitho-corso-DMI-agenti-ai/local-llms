import sys

from app.game import Game, HumanGamePrinter


def main():
    human_player_name = sys.argv[1]

    game = Game(
        agent_model="gemma3:1b",
        human_name=human_player_name,
        printer=HumanGamePrinter(is_player_spy=True),
        spy_name=human_player_name,
    )

    game_result = game.play()

    print("################")
    print(f"Final game result: {game_result}")
    print(f"Final conversation:\n\n{game.get_conversation().as_prompt()}")


if __name__ == "__main__":
    main()
