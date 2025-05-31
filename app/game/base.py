from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

from .player import AgentPlayer
from .data import Player, Question
from .state import GameState


class Game(BaseModel):
    players: dict[Player, AgentPlayer]

    _graph: any

    def model_post_init(self, context):
        graph_builder = StateGraph(GameState)

        graph_builder.add_node("make_question", self.make_question)
        graph_builder.add_node("answer", self.answer)

        graph_builder.add_edge(START, "make_question")
        graph_builder.add_edge("make_question", "answer")
        graph_builder.add_edge("answer", END)

        self._graph = graph_builder.compile()

    def make_question(self, state: GameState) -> GameState:
        player = self.players[state.current_player]

        question: Question = player.make_question(state)
        state.add_message(question.to_game_message(player.name))

        state.current_player = question.to_player
        state.print()
        return state

    def answer(self, state: GameState) -> GameState:
        pass

    def play(self, location: str, first_player: Player):
        self._graph.invoke(GameState.init(location, first_player))
