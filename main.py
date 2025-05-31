from app.agent_player import AgentPlayer
from app.game import GameState, GameRole


def main():
    game_state = GameState()

    location = "Department of Mathematics and Computer Science"
    model = "deepseek-r1"

    players = {
        "Lorenzo": AgentPlayer(model=model, name="Lorenzo", game_role=GameRole.SPY),
        "Stefano": AgentPlayer(model=model, name="Stefano", game_role=GameRole.PLAYER, location=location),
        "Alessio": AgentPlayer(model=model, name="Alessio", game_role=GameRole.PLAYER, location=location),
        "Davide": AgentPlayer(model=model, name="Davide", game_role=GameRole.PLAYER, location=location),
    }

    turns = 0
    current_player = players["Lorenzo"]
    while True:
        turns += 1

        player_question = current_player.reply_to(game_state)
        print(f"-- Player {current_player.name} question: {player_question}")
        game_state.add_message(player_question.to_game_message(current_player.name))

        print("###### ")
        print(f"Turn #{turns}")
        print(f"Game state: {game_state}")

        current_player = players[player_question.to_player]


if __name__ == "__main__":
    main()
