import os
import gc
import tempfile
import shutil
from git import Repo
from dotenv import load_dotenv
from urllib.parse import quote
from pathlib import Path

load_dotenv()

def run(state):
    username = "naveenduttvyas"
    pat_token = os.getenv("GIT_TOKEN")  # Store your PAT in .env under GIT_TOKEN
    encoded_pat = quote(pat_token)
    repo_url = f"https://{username}:{encoded_pat}@github.com/{username}/sample-api.git"

    for story in state["ai_stories"]:
        story_type = story.get("type", "code")
        story_key = story["key"]

        with tempfile.TemporaryDirectory() as tmp:
            try:
                repo = Repo.clone_from(repo_url, tmp, env={"GIT_TERMINAL_PROMPT": "0"})
                repo.git.update_environment(GIT_ASKPASS="echo", GIT_TERMINAL_PROMPT="0")
                repo.git.config("credential.helper", "")

                if "origin" not in [remote.name for remote in repo.remotes]:
                    origin = repo.create_remote("origin", url=repo_url)
                else:
                    origin = repo.remote(name="origin")
                    origin.set_url(repo_url)

                if story_type == "document":
                    updated_file_path = story.get("updated_file_path")
                    if not updated_file_path:
                        print(f"[WARN] No updated_file_path found for {story_key}, skipping document commit.")
                        continue

                    abs_doc_path = Path(updated_file_path)
                    if not abs_doc_path.exists():
                        print(f"[WARN] Document {updated_file_path} does not exist.")
                        continue

                    print(f"[INFO] Preparing to commit document: {abs_doc_path}")

                    # Maintain structure: copy to same relative path inside repo
                    repo_root = Path(os.getenv("LOCAL_REPO_PATH", "sample-api")).resolve()
                    relative_to_repo = abs_doc_path.resolve().relative_to(repo_root.parent) if abs_doc_path.is_absolute() else abs_doc_path

                    target_path = Path(tmp) / relative_to_repo
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(abs_doc_path, target_path)


                elif story_type == "code":
                    updated_file_path = story.get("updated_file_path")
                    if not updated_file_path:
                        print(f"[WARN] No updated_file_path found for {story_key}, skipping code commit.")
                        continue

                    abs_updated_path = Path(updated_file_path)
                    if not abs_updated_path.exists():
                        print(f"[WARN] LLM said it wrote {updated_file_path}, but it does not exist.")
                        continue

                    repo_root = Path(os.getenv("LOCAL_REPO_PATH", "sample-api")).resolve()
                    relative_to_repo = abs_updated_path.resolve().relative_to(repo_root)
                    target_path = Path(tmp) / relative_to_repo
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(abs_updated_path, target_path)

                else:
                    print(f"Unknown type for story {story_key}, skipping...")
                    continue

                # Git operations
                repo.git.add(A=True)
                repo.index.commit(f"Auto commit for {story_key}")

                try:
                    origin.push()
                    print(f"Pushed successfully for {story_key}")
                except Exception as e:
                    print("Git push failed:", e)

                repo.close()
                del repo
                gc.collect()

            finally:
                try:
                    shutil.rmtree(tmp, ignore_errors=True)
                except Exception as e:
                    print("Manual cleanup failed:", e)

    return state