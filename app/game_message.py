class GameMessage:
    def __init__(self, user, message_text):
        self.user = user
        self.message_text = message_text

    def __str__(self):
        return f"{self.user}: {self.message_text}"

class GameState:
    def __init__(self):
        self.messages = list()

    def add_message(self, message: GameMessage):
        self.messages.append(message)