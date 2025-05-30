from app.agent_player import AgentPlayer
from app.game_message import GameState, GameMessage


def main():
    game_state = GameState()

    player = AgentPlayer("gemma3:1b", "Stefano")

    game_state.add_message(
        GameMessage(
            "Lorenzo", "Stefano, do you believe that the place we are is warm?"
        )
    )

    response = player.reply_to(game_state)
    print(response.message.content)



if __name__ == "__main__":
    main()
