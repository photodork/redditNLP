import os

# GitHub provides this automatically
pr_title = os.getenv("GITHUB_HEAD_REF", "").lower()
branch_name = os.getenv("GITHUB_REF_NAME", "").lower()

print(f"PR Title/Branch context: {pr_title} | {branch_name}")

pr_type = "FEATURE"  # default

if pr_title.startswith("fix") or pr_title.startswith("bug"):
    pr_type = "BUG"
elif branch_name.startswith("fix/") or branch_name.startswith("bug/"):
    pr_type = "BUG"
elif branch_name.startswith("feat/") or branch_name.startswith("feature/"):
    pr_type = "FEATURE"

print(f"📌 Classified PR as: {pr_type}")

with open("pr_type.txt", "w") as f:
    f.write(pr_type)
