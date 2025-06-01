from ollama import chat
from pydantic import BaseModel

from app.prompting import load_prompt

from app.game.data import Question, Answer, SpyGuess, PlayerGuess, Player
from app.game.state import GameState


class AgentPlayer(BaseModel):
    model: str
    name: str
    _location: str = None

    def communicate_location(self, location: str):
        self._location = location

    def is_spy(self) -> bool:
        return self._location is None

    def __role_prompt(self, prompt_id, **kwargs):
        role = "spy" if self.is_spy() else "player"
        return load_prompt(f"{role}/{prompt_id}", **kwargs)

    def __build_system_prompt(self, state: GameState):
        game_role_prompt = self.__role_prompt("system", location=self._location)
        conversation_prompt = state.conversation_prompt()

        return {
            "role": "system",
            "content": load_prompt(
                "general_system",
                name=self.name,
                game_role_prompt=game_role_prompt,
                conversation_prompt=conversation_prompt,
                player_names=", ".join(list(Player))
            ),
        }

    def __remove_own_name_from_output_structure(self, structure):
        if "$defs" in structure and "Player" in structure["$defs"]:
            structure["$defs"]["Player"]["enum"].remove(self.name)
        return structure

    def _send_request(
        self,
        state: GameState,
        prompt: str,
        output_model: type[BaseModel],
    ) -> dict:
        messages = [
            self.__build_system_prompt(state),
            {"role": "user", "content": prompt},
        ]

        while True:
            try:
                response = chat(
                    model=self.model,
                    messages=messages,
                    format=self.__remove_own_name_from_output_structure(
                        output_model.model_json_schema()
                    ),
                    options={"temperature": 1.0},
                )

                return output_model.model_validate_json(response.message.content)
            except Exception as e:
                print(f"Exception while making a request: {e}, retrying...")

    def make_question(self, state: GameState) -> Question:
        return self._send_request(
            state,
            self.__role_prompt("make_question"),
            Question,
        )

    def answer(self, state: GameState) -> Answer:
        return self._send_request(
            state,
            self.__role_prompt(
                "answer",
                questioner_name=state.questioner,
                question=state._question.content,
            ),
            Answer,
        )

    def guess_location(self, state: GameState) -> SpyGuess:
        return self._send_request(
            state,
            self.__role_prompt("guess_location"),
            SpyGuess,
        )

    def guess_spy(self, state: GameState) -> PlayerGuess:
        return self._send_request(
            state,
            self.__role_prompt("guess_the_spy"),
            PlayerGuess,
        )
