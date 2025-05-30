from ollama import chat


def main():
    response = chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "system",
                "content": "You are playing a Spyfall game and you are the Spy. Be brief in your answers. Listen to the conversation and reply to questions acting like you know where you are.",
            },
            {
                "role": "user",
                "content": "Do you believe that the place we are is warm?",
            },
        ],
    )
    print(response.message.content)


if __name__ == "__main__":
    main()
