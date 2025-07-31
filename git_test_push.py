import os
import tempfile
import shutil
from git import Repo, GitCommandError
from urllib.parse import quote

username = "naveedvyas"
pat_token = "y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"
encoded_pat = quote(pat_token)
repo_url = f"https://{username}:{encoded_pat}@github.com/{username}/mysamplecode.git"

try:
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📁 Cloning into: {tmpdir}")
        
        repo = Repo.clone_from(repo_url, tmpdir)
        print(repo.git.config('--list'))
        
        # Force Git to use credentials for all actions
        repo.git.update_environment(GIT_ASKPASS=None)

        # Create a test file
        file_path = os.path.join(tmpdir, "push_token_test.py")
        with open(file_path, "w") as f:
            f.write("print('✅ Token-based Git push from Python works!')\n")

        repo.git.add(A=True)
        repo.index.commit("✅ Token push test via Python")
        
        print("🚀 Attempting push with PAT...")
        repo.remote().push()
        print("✅ Push successful.")

except GitCommandError as e:
    print("❌ Git operation failed:")
    print(e)

except Exception as e:
    print("❌ Other error occurred:", e)
