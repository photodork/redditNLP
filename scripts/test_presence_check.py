print("Step 2: Checking if tests already exist (stub)")
import subprocess

def get_changed_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True
    )
    return result.stdout.splitlines()

def has_tests(files):
    for file in files:
        if file.startswith("tests/"):
            return True
        if file.endswith("_test.py") or file.startswith("test_"):
            return True
    return False

changed_files = get_changed_files()

if has_tests(changed_files):
    print("Tests detected in PR")
    with open("tests_present.txt", "w") as f:
        f.write("true")
else:
    print("No tests detected in PR")
    with open("tests_present.txt", "w") as f:
        f.write("false")
