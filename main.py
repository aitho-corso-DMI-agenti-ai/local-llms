from app.game.player import AgentPlayer
from app.game import Game
from app.game.data import GameRole, Player, Location


def main():
    location = Location.University

    # model = "mistral-nemo:12b"
    model = "gemma3:1b"

    game_result = Game(
        players={
            Player.Lorenzo: AgentPlayer(
                model=model, name="Lorenzo", game_role=GameRole.SPY
            ),
            Player.Stefano: AgentPlayer(
                model=model,
                name="Stefano",
                game_role=GameRole.PLAYER,
                location=location,
            ),
            Player.Alessio: AgentPlayer(
                model=model,
                name="Alessio",
                game_role=GameRole.PLAYER,
                location=location,
            ),
            Player.Davide: AgentPlayer(
                model=model, name="Davide", game_role=GameRole.PLAYER, location=location
            ),
        },
        location=Location.University,
    ).play()

    print(f"Final game result {game_result}")

if __name__ == "__main__":
    main()
