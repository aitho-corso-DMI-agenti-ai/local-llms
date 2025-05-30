from ollama import chat, Message

from app.game_message import GameMessage, GameState

class AgentPlayer:
    def __init__(self, model, name):
        self.model = model
        self.system_message = {
            "role": "system",
            "content": 
            f"Your name is {name}."
            "You are playing a Spyfall gameand you are the Spy."
            "Be brief in your answers."
            "Listen to the conversation and reply to questions acting like you know where you are.",
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
                self.__format_conversation_prompt(game_state.messages),
            ]
        ) 