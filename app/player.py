from ollama import chat

from app.data import Question, Answer, SpyGuess, PlayerGuess
from app.state import ConversationState

from pydantic import BaseModel
from app.data import Player, Location
from typing import Protocol, runtime_checkable


@runtime_checkable
class PlayerActor(Protocol):
    def communicate_location(self, location: str): ...

    def is_spy(self) -> bool: ...

    def make_question(self, conversation_state: ConversationState) -> Question: ...

    def answer(
        self, conversation_state: ConversationState, questioner_name: str, question: str
    ) -> Answer: ...

    def guess_location(self, conversation_state: ConversationState) -> SpyGuess: ...

    def guess_spy(self, conversation_state: ConversationState) -> PlayerGuess: ...


def load_prompt(prompt_id: str, **kwargs):
    return open(f"prompts/{prompt_id}.md", "r").read().format(**kwargs)


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

    def __build_system_prompt(self, conversation_state: ConversationState):
        game_role_prompt = self.__role_prompt("system", location=self._location)
        return {
            "role": "system",
            "content": load_prompt(
                "general_system",
                name=self.name,
                game_role_prompt=game_role_prompt,
                conversation_prompt=conversation_state.as_prompt(),
                player_names=", ".join(list(Player)),
                possible_locations=", ".join(list(Location)),
            ),
        }

    def __remove_own_name_from_output_structure(self, structure):
        if "$defs" in structure and "Player" in structure["$defs"]:
            structure["$defs"]["Player"]["enum"].remove(self.name)
        return structure

    def _send_request(
        self,
        conversation_state: ConversationState,
        prompt: str,
        output_model: type[BaseModel],
    ) -> dict:
        messages = [
            self.__build_system_prompt(conversation_state),
            {"role": "user", "content": prompt},
        ]

        # print("------------------------------")
        # for message in messages:
        #     print(message["content"])
        # print("------------------------------")

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

    def make_question(self, conversation_state: ConversationState) -> Question:
        return self._send_request(
            conversation_state,
            self.__role_prompt("make_question"),
            Question,
        )

    def answer(
        self, conversation_state: ConversationState, questioner_name: str, question: str
    ) -> Answer:
        return self._send_request(
            conversation_state,
            self.__role_prompt(
                "answer",
                questioner_name=questioner_name,
                question=question,
            ),
            Answer,
        )

    def guess_location(self, conversation_state: ConversationState) -> SpyGuess:
        return self._send_request(
            conversation_state,
            self.__role_prompt("guess_location"),
            SpyGuess,
        )

    def guess_spy(self, conversation_state: ConversationState) -> PlayerGuess:
        return self._send_request(
            conversation_state,
            self.__role_prompt("guess_the_spy"),
            PlayerGuess,
        )


DEFAULT_JUSTIFICATION = "I'm a human, I don't need to justify my choice"


class HumanPlayer(BaseModel):
    name: str

    def communicate_location(self, location: str):
        print(f"The location is: {location}!")

    def is_spy(self) -> bool:
        return True

    def _get_input(self, prompt: str) -> str:
        return input(prompt).strip()

    def make_question(self, conversation_prompt: str) -> Question:
        print(conversation_prompt)
        return Question(
            to_player=Player(
                self._get_input(
                    f"To which player would you like to make a question? (Options: {', '.join(Player)}) "
                )
            ),
            content=self._get_input("What is your question? "),
            justification=DEFAULT_JUSTIFICATION,
        )

    def answer(
        self, conversation_prompt: str, questioner_name: str, question: str
    ) -> Answer:
        print(conversation_prompt)
        print(f"Question from {questioner_name}: {question}")
        return Answer(
            content=self._get_input("What is your answer? "),
            justification=DEFAULT_JUSTIFICATION,
        )

    def guess_location(self, conversation_prompt: str) -> SpyGuess:
        print(conversation_prompt)
        location_input = self._get_input(
            f"Which location do you guess? (Options: {', '.join(Location)}, or press Enter to skip) "
        )
        if not location_input:
            return SpyGuess(guessed_location=None, justification=DEFAULT_JUSTIFICATION)
        return SpyGuess(
            guessed_location=Location(location_input),
            justification=DEFAULT_JUSTIFICATION,
        )

    def guess_spy(self, conversation_prompt: str) -> PlayerGuess:
        if self.is_spy():
            return PlayerGuess(accused_player=None, justification=DEFAULT_JUSTIFICATION)

        print(conversation_prompt)
        accused_player = self._get_input(
            f"Which player do you accuse? (Options: {', '.join(Player)}, or press Enter to skip) "
        )
        if not accused_player:
            return PlayerGuess(accused_player=None, justification=DEFAULT_JUSTIFICATION)
        return PlayerGuess(
            accused_player=Player(accused_player), justification=DEFAULT_JUSTIFICATION
        )

