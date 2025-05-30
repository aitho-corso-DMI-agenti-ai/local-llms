from app.agent_player import AgentPlayer
from app.game_message import GameState, GameMessage


def main():
    game_state = GameState()

    players = [
        AgentPlayer("gemma3:1b", "Stefano", game_role="spy"),
        AgentPlayer("gemma3:1b", "Lorenzo", game_role="player"),
    ]

    game_state.add_message(
        GameMessage("Lorenzo", "Stefano, do you believe that the place we are is warm?")
    )

    while True:
        for player in players:
            response = player.reply_to(game_state)
            text = response.message.content
            game_state.add_message(GameMessage(player.name, text))

        print(f"Game state: {game_state}")


if __name__ == "__main__":
    main()
