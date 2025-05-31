from ollama import chat, Message
from pydantic import BaseModel

from app.game import GameMessage, GameState, GameRole, Question
from app.prompting import load_prompt


class AgentPlayer(BaseModel):
    model: str
    name: str
    game_role: GameRole
    location: str | None = None

    _system_message: dict[str, any]

    def model_post_init(self, context):
        self._system_message = {
            "role": "system",
            "content": load_prompt(
                "general_system",
                name=self.name,
                game_role_prompt=load_prompt(
                    f"{self.game_role}_system", location=self.location
                ),
            ),
        }

    def __format_conversation_prompt(
        self, game_messages: list[GameMessage]
    ) -> Question:
        output = "Previous messages: "
        output += "\n".join([str(msg) for msg in game_messages])
        return {"role": "user", "content": output}

    def reply_to(self, game_state: GameState) -> Message:
        messages = [
            self._system_message,
            self.__format_conversation_prompt(game_state.messages),
        ]

        # print("---")
        # for msg in messages:
        #     print(msg)
        #     print("---")
        

        response = chat(
            model=self.model, messages=messages, format=Question.model_json_schema()
        )

        return Question.model_validate_json(response.message.content)
