from ollama import chat
from pydantic import BaseModel

from app.prompting import load_prompt

from .data import GameRole, Question, Answer, SpyGuess, PlayerGuess
from .state import GameState


class AgentPlayer(BaseModel):
    model: str
    name: str

    _game_role: GameRole 

    def model_post_init(self, context):
        self._game_role = GameRole.PLAYER

    def make_spy(self):
        self._game_role = GameRole.SPY

    def is_spy(self) -> bool:
        return self._game_role == GameRole.SPY

    def __role_prompt(self, prompt_id, **kwargs):
        return load_prompt(f"{self._game_role}/{prompt_id}", **kwargs)

    def __build_system_prompt(self, state: GameState):
        game_role_prompt = self.__role_prompt("system", location=state.location)
        conversation_prompt = state.conversation_prompt()

        return {
            "role": "system",
            "content": load_prompt(
                "general_system",
                name=self.name,
                game_role_prompt=game_role_prompt,
                conversation_prompt=conversation_prompt,
            ),
        }

    def make_question(self, state: GameState) -> Question:
        messages = [
            self.__build_system_prompt(state),
            {"role": "user", "content": self.__role_prompt("make_question")},
        ]
        response = chat(
            model=self.model, messages=messages, format=Question.model_json_schema()
        )

        return Question.model_validate_json(response.message.content)

    def answer(self, state: GameState) -> Answer:
        messages = [
            self.__build_system_prompt(state),
            {
                "role": "user",
                "content": self.__role_prompt(
                    "answer",
                    questioner_name=state.questioner,
                    question=state._question.content,
                ),
            },
        ]
        response = chat(
            model=self.model, messages=messages, format=Question.model_json_schema()
        )

        return Answer.model_validate_json(response.message.content)

    def guess_location(self, state: GameState) -> SpyGuess:
        messages = [
            self.__build_system_prompt(state),
            {
                "role": "user",
                "content": self.__role_prompt("guess_location"),
            },
        ]
        response = chat(
            model=self.model, messages=messages, format=SpyGuess.model_json_schema()
        )
        return SpyGuess.model_validate_json(response.message.content)

    def guess_spy(self, state: GameState) -> PlayerGuess:
        messages = [
            self.__build_system_prompt(state),
            {
                "role": "user",
                "content": self.__role_prompt("guess_the_spy"),
            },
        ]
        response = chat(
            model=self.model, messages=messages, format=PlayerGuess.model_json_schema()
        )
        return PlayerGuess.model_validate_json(response.message.content)

