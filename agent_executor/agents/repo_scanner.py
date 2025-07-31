import os
from pathlib import Path

def find_matching_code_file(story_text: str, repo_root: str):
    story_text = story_text.lower()
    matches = []

    for py_file in Path(repo_root).rglob("*.py"):
        filename = py_file.name.lower()
        if filename.replace(".py", "") in story_text:
            matches.append(py_file)

    if matches:
        return str(matches[0])  # pick the first relevant match
    return None