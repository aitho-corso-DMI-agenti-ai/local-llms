from app.game.player import AgentPlayer
from app.game import Game
from app.game.data import Player


def init_players():
    # model = "mistral-nemo:12b"
    # model = "mistral:7b"
    # model = "phi:2.7b"
    # model = "deepseek-r1"
    model = "gemma3:1b"

    players = dict()
    for player_name in Player:
        players[player_name] = AgentPlayer(model=model, name=player_name.value)

    return players


def main():
    game_result = Game(players=init_players()).play()

    print(f"Final game result {game_result}")


if __name__ == "__main__":
    main()
