from ollama import chat
from pydantic import BaseModel

from app.prompting import load_prompt

from .data import GameRole, Question
from .state import GameState


class AgentPlayer(BaseModel):
    model: str
    name: str
    game_role: GameRole

    def make_question(self, state: GameState) -> Question:
        system_message = {
            "role": "system",
            "content": load_prompt(
                "general_system",
                name=self.name,
                game_role_prompt=load_prompt(
                    f"{self.game_role}_system", location=state.location
                ),
                conversation_prompt=state.conversation_prompt(),
            ),
        }

        query_message = {"role": "user", "content": load_prompt("make_question")}

        messages = [system_message, query_message]

        response = chat(
            model=self.model, messages=messages, format=Question.model_json_schema()
        )

        return Question.model_validate_json(response.message.content)
