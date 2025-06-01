from app.game.player import AgentPlayer, HumanPlayer
from app.game import Game, HumanGamePrinter
from app.game.data import Player
import argparse

def init_players(human_player_name: str):
    model = "gemma3:1b"

    players = dict()
    for player_name in Player:
        if player_name.value == human_player_name:
            players[player_name] = HumanPlayer(name=player_name.value)
        else:
            players[player_name] = AgentPlayer(model=model, name=player_name.value)

    return players

def main():
    parser = argparse.ArgumentParser(description="Run the game with a specified human player.")
    parser.add_argument("human_player_name", type=str, help="The name of the human player.")
    args = parser.parse_args()

    human_player_name = args.human_player_name
    game_result, game_state = Game(players=init_players(human_player_name),
    printer=HumanGamePrinter(is_player_spy=True)).play()

    print("################")
    print(f"Final game result: {game_result}")
    print(f"Final game state: {game_state}")

if __name__ == "__main__":
    main()