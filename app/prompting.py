def load_prompt(prompt_id: str):
    return open(f"prompts/{prompt_id}.md", 'r').read()