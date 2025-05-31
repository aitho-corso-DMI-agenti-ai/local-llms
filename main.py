from app.agent_player import AgentPlayer
from app.game import GameState, GameMessage, GameRole


def main():
    game_state = GameState()

    location = "Department of Mathematics and Computer Science"

    players = [
        AgentPlayer(model="gemma3:1b", name="Lorenzo", game_role=GameRole.SPY),
        AgentPlayer(model="gemma3:1b", name="Stefano", game_role=GameRole.PLAYER, location=location),
        AgentPlayer(model="gemma3:1b", name="Alessio", game_role=GameRole.PLAYER, location=location),
        AgentPlayer(model="gemma3:1b", name="Davide", game_role=GameRole.PLAYER, location=location),
    ]

    game_state.add_message(
        GameMessage(
            user="Lorenzo",
            message_text="Stefano, do you believe that the place we are is warm?",
        )
    )

    turns = 0
    while True:
        turns += 1
        for player in players:
            response = player.reply_to(game_state)
            text = response.message.content
            game_state.add_message(GameMessage(user=player.name, message_text=text))

        print(" ###### ")
        print(f"Turn #{turns}")
        print(f"Game state: {game_state}")


if __name__ == "__main__":
    main()
