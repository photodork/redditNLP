import os
import re
import json
import requests
from requests.auth import HTTPBasicAuth

# -------------------------
# Helper functions
# -------------------------

def extract_jira_id(text):
    match = re.search(r"[A-Z]+-\d+", text)
    return match.group(0) if match else None

def fetch_jira_issue(issue_id):
    url = f"{os.environ['JIRA_BASE_URL']}/rest/api/3/issue/{issue_id}"
    auth = HTTPBasicAuth(
        os.environ["JIRA_EMAIL"],
        os.environ["JIRA_API_TOKEN"]
    )
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()
    return response.json()

# -------------------------
# Load GitHub PR context (CORRECT WAY)
# -------------------------

event_path = os.getenv("GITHUB_EVENT_PATH")

if not event_path:
    raise RuntimeError("GITHUB_EVENT_PATH not found")

with open(event_path, "r") as f:
    event = json.load(f)

pr_title = event["pull_request"]["title"]
branch_name = event["pull_request"]["head"]["ref"]

combined_text = f"{pr_title} {branch_name}"

print(f"🧾 PR Title: {pr_title}")
print(f"🌿 Branch Name: {branch_name}")

# -------------------------
# Classification logic
# -------------------------

jira_id = extract_jira_id(combined_text)
pr_type = "FEATURE"  # default

# ---- JIRA-based classification (PRIMARY) ----

if jira_id:
    print(f"🔍 Extracted JIRA ID: {jira_id}")
    try:
        issue = fetch_jira_issue(jira_id)
        issue_type = issue["fields"]["issuetype"]["name"]
        print(f"📘 JIRA Issue Type: {issue_type}")

        if issue_type.lower() == "bug":
            pr_type = "BUG"
        else:
            pr_type = "FEATURE"

    except Exception as e:
        print(f"⚠️ JIRA lookup failed: {e}")
        print("➡️ Falling back to branch/title logic")

# ---- Fallback (Phase 3 logic) ----

if not jira_id:
    branch_lower = branch_name.lower()
    title_lower = pr_title.lower()

    if branch_lower.startswith("fix/") or branch_lower.startswith("bug/") or title_lower.startswith("fix"):
        pr_type = "BUG"
    elif branch_lower.startswith("feat/") or branch_lower.startswith("feature/") or title_lower.startswith("feat"):
        pr_type = "FEATURE"

print(f"📌 Final PR Classification: {pr_type}")

with open("pr_type.txt", "w") as f:
    f.write(pr_type)
