# Running local LLMs with Python and Ollama

This repository contains the code shown during the seminar "Local agents with Python and Ollama", held at the Department of Mathematics and Computer Science of University of Catania by Lorenzo Catania.

The source code is made of an engine for the social game [Spyfall](https://hobbyworldint.com/portfolio-item/spyfall/), including interfaces for agentic and human players to join the game.

## Requirements

### uv (Dependency Manager)

To get started with this project, you need to install `uv`: https://docs.astral.sh/uv/#installation

### ollama (Local LLM Server)

This project also requires `ollama`, a local LLM (Language Model) server. 
The easiest way to run an `ollama` server is through Docker:

```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Then pull the model needed to run the examples (Gemma3) with:
```sh
docker exec -it ollama ollama pull gemma3:1b
```

Alternatively, you can find alternative installation methods on the [ollama GitHub repository](https://github.com/ollama/ollama).

## Examples

### Watch Local LLMs Play Spyfall

To watch local LLMs play Spyfall, use the following command:

```sh
uv run -m main
```

This command will start the game and allow you to observe how the LLMs interact and play Spyfall.

### Try to Hide as a Spy from LLMs

If you want to participate and try to hide as a spy from the LLMs, you can use the following command:

```sh
uv run -m human_play [Your name]
```

Replace `[Your name]` with one of the ```Player``` names in ```app/data.py```. This command will start the game with you as a spy, so try to blend in and avoid detection by the AIs!
