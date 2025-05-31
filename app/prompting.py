def load_prompt(prompt_id: str, **kwargs):
    return open(f"prompts/{prompt_id}.md", "r").read().format(**kwargs)
