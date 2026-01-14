import json
import os

# Load GitHub PR event payload
with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
    event = json.load(f)

pr_title = event["pull_request"]["title"].lower()
branch_name = event["pull_request"]["head"]["ref"].lower()

print(f"🧾 PR Title: {pr_title}")
print(f"🌿 Branch Name: {branch_name}")

# Default classification
pr_type = "FEATURE"

# Primary: PR title intent
if pr_title.startswith("bug:"):
    pr_type = "BUG"
elif pr_title.startswith("feat:"):
    pr_type = "FEATURE"

# Secondary fallback (optional safety)
elif branch_name.startswith("fix/") or branch_name.startswith("bug/"):
    pr_type = "BUG"
elif branch_name.startswith("feat/") or branch_name.startswith("feature/"):
    pr_type = "FEATURE"

print(f"📌 Final PR Classification: {pr_type}")

# Persist for next phases
with open("pr_type.txt", "w") as f:
    f.write(pr_type)
