from typing import Protocol, runtime_checkable
from app.game.data import Question, Answer, SpyGuess, PlayerGuess
from app.game.state import ConversationState

@runtime_checkable
class PlayerActor(Protocol):
    def communicate_location(self, location: str):
        ...

    def is_spy(self) -> bool:
        ...

    def make_question(self, conversation_state: ConversationState) -> Question:
        ...

    def answer(self, conversation_state: ConversationState, questioner_name: str, question: str) -> Answer:
        ...

    def guess_location(self, conversation_state: ConversationState) -> SpyGuess:
        ...

    def guess_spy(self, conversation_state: ConversationState) -> PlayerGuess:
        ...