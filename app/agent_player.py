from ollama import chat, Message

from app.game_message import GameMessage, GameState
from app.prompting import load_prompt

class AgentPlayer:
    def __init__(self, model, name, game_role="player"):
        self.model = model
        self.name = name

        self.system_message = {
            "role": "system",
            "content": load_prompt("general_system"),
        }

        self.game_role_message = {
            "role": "system",
            "content": load_prompt(f"{game_role}_system"),
        }

    def __format_conversation_prompt(self, game_messages: list[GameMessage]) -> Message:
        output = "Previous messages: "
        output += "\n".join([str(msg) for msg in game_messages])
        return {
            "role": "user",
            "content": output
        }

    def reply_to(self, game_state: GameState) -> Message:
        return chat(
            model="gemma3:1b",
            messages=[
                self.system_message,
                self.game_role_message,
                self.__format_conversation_prompt(game_state.messages),
            ]
        ) 