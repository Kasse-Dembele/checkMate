import os
import requests

# GitHub API details
GITHUB_API_URL = "https://api.github.com"
REPO = os.getenv("GITHUB_REPOSITORY")  # e.g., "owner/repo"
# Extract PR number from ref, assuming format "refs/pull/<PR_NUMBER>/merge"
try:
    PR_NUMBER = os.getenv("GITHUB_REF").split("/")[2]
except Exception as e:
    print(f"[ERROR] Failed to extract PR number: {e}")
    PR_NUMBER = None


GITHUB_TOKEN = os.getenv("INPUT_GITHUB_TOKEN")


# Checklist template
CHECKLIST = """
### **PR Review Checklist**

- [ ] Code compiles and passes all tests.
- [ ] Solution produces the expected results.
- [ ] Code is clean, readable, and adheres to standards.
- [ ] Documentation is updated.
- [ ] Commit messages and changelogs are clear.
- [ ] Examples and tests are updated.
- [ ] Versioning is evaluated and justified.
- [ ] Review feedback is addressed.
- [ ] Integration and deployment readiness is confirmed.

---

*This checklist was automatically generated by the PR Checklist Bot.*
"""

def get_pr_details():
    """Fetch PR details to get the list of reviewers."""
    if not PR_NUMBER:
        print("[ERROR] PR_NUMBER is not defined.")
        return None

    url = f"{GITHUB_API_URL}/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[ERROR] Failed to fetch PR details: {response.status_code} {response.text}")
        return None

def post_comment(reviewer):
    """Post the checklist comment and tag the reviewer."""
    if not PR_NUMBER:
        print("[ERROR] PR_NUMBER is not defined.")
        return

    url = f"{GITHUB_API_URL}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    body = f"@{reviewer}, please review this PR. Here's a checklist to guide you:\n\n{CHECKLIST}"
    data = {"body": body}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"[SUCCESS] Checklist posted for reviewer: {reviewer}")
    else:
        print(f"[ERROR] Failed to post comment: {response.status_code} {response.text}")

def main():
    pr_details = get_pr_details()
    if pr_details:
        #reviewers = pr_details.get("requested_reviewers", [])
        #if not reviewers:
            #print("[INFO] No reviewers found.")
        #for reviewer in reviewers:
        post_comment("Reviewer")

if __name__ == "__main__":
    main()
