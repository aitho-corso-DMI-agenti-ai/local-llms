from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

from .player import AgentPlayer
from .data import Player, Question, Answer
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
        questioner = self.players[state.questioner]
        question: Question = questioner.make_question(state)
        print(f"[Game] Question from player {state.questioner}: {question}")

        state.question = question

        return state

    def answer(self, state: GameState) -> GameState:
        questioner = self.players[state.questioner]
        player = self.players[state.question.to_player]

        answer: Answer = player.answer(state)
        print(f"[Game] Answer from player {state.question.to_player}: {answer}")

        state.add_message(state.question.to_game_message(questioner.name))
        state.add_message(answer.to_game_message(questioner.name, player.name))

        state.questioner = state.question.to_player

        state.print()
        return state

    def play(self, location: str, first_player: Player):
        self._graph.invoke(GameState(location=location, questioner=first_player))
