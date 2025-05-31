from ollama import chat, Message
from pydantic import BaseModel

from app.game import GameMessage, GameState, GameRole
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

    def __format_conversation_prompt(self, game_messages: list[GameMessage]) -> Message:
        output = "Previous messages: "
        output += "\n".join([str(msg) for msg in game_messages])
        return {"role": "user", "content": output}

    def reply_to(self, game_state: GameState) -> Message:
        return chat(
            model="gemma3:1b",
            messages=[
                self._system_message,
                self.__format_conversation_prompt(game_state.messages),
            ],
        )
