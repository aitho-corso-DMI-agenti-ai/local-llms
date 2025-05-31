from pydantic import BaseModel
from langgraph.graph import StateGraph, START

from .player import AgentPlayer
from .data import Player, Question, Answer, SpyGuess, PlayerGuess, GameRole
from .state import GameState


class Game(BaseModel):
    players: dict[Player, AgentPlayer]

    _graph: any

    def model_post_init(self, context):
        graph_builder = StateGraph(GameState)

        graph_builder.add_node("make_question", self.make_question)
        graph_builder.add_node("answer", self.answer)
        graph_builder.add_node("ask_spy_to_guess", self.ask_spy_to_guess)
        graph_builder.add_node("ask_players_to_guess", self.ask_players_to_guess)

        graph_builder.add_edge(START, "make_question")
        graph_builder.add_edge("make_question", "answer")
        graph_builder.add_edge("answer", "ask_spy_to_guess")
        graph_builder.add_edge("ask_spy_to_guess", "ask_players_to_guess")
        graph_builder.add_edge("ask_players_to_guess", "make_question")

        self._graph = graph_builder.compile()

    def ask_spy_to_guess(self, state: GameState) -> GameState:
        spy = self.get_spy()
        guess: SpyGuess = spy.guess_location(state)
        print(f"[Game] Spy guess: {guess}")
        return state

    def ask_players_to_guess(self, state: GameState) -> GameState:
        for player_name in self.players:
            player = self.players[player_name]
            if player.game_role == GameRole.SPY:
                continue

            guess: PlayerGuess = player.guess_spy(state)
            print(f"[Game] Player {player_name} guess: {guess}")

        return state

    def make_question(self, state: GameState) -> GameState:
        questioner = self.players[state.questioner]
        question: Question = questioner.make_question(state)
        print(f"[Game] Question from player {state.questioner}: {question}")

        state._question = question

        return state

    def answer(self, state: GameState) -> GameState:
        questioner = self.players[state.questioner]
        player = self.players[state._question.to_player]

        answer: Answer = player.answer(state)
        print(f"[Game] Answer from player {state._question.to_player}: {answer}")

        state.add_message(state._question.to_game_message(questioner.name))
        state.add_message(answer.to_game_message(questioner.name, player.name))

        state.questioner = state._question.to_player

        state.print()
        return state

    def get_spy(self):
        for player_name in self.players:
            player = self.players[player_name]
            if player.game_role == GameRole.SPY:
                return player

    def play(self, location: str, first_player: Player):
        self._graph.invoke(
            GameState(location=location, questioner=first_player)
        )
