
import argparse
import subprocess
import os
import sys
import json
from .reviewer import PRReviewer, LLMAdapter
from typing import Optional

def git_diff(base: str = "main", head: str = "HEAD", path: str = ".") -> str:
    cmd = ["git", "-C", path, "diff", f"{base}...{head}"]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        return out
    except subprocess.CalledProcessError:
        return ""

def format_report_to_markdown(report: dict) -> str:
    if "report" in report:
        r = report["report"]
        md = f"## Summary\n{r.get('summary','')}\n\n### Top Issues\n"
        for i, it in enumerate(r.get("issues", []), 1):
            md += f"{i}. {it}\n"
        md += "\n### Suggestions\n"
        for s in r.get("suggestions", []):
            md += f"- {s}\n"
        md += "\n### Checklist\n"
        for c in r.get("checklist", []):
            md += f"- [ ] {c}\n"
        return md
    return "```\n" + report.get("report_raw","") + "\n```"

def main(argv=None):
    p = argparse.ArgumentParser(prog="pr-reviewer-ai")
    p.add_argument("action", choices=["review"])
    p.add_argument("--path", default=".")
    p.add_argument("--base", default="main")
    p.add_argument("--head", default="HEAD")
    p.add_argument("--model", default=os.getenv("REVIEWER_MODEL","openai/gpt-4"))
    p.add_argument("--openai-api-key", default=os.getenv("OPENAI_API_KEY"))
    p.add_argument("--github-token", default=os.getenv("GITHUB_TOKEN"))
    p.add_argument("--prompt-mode", default="succinct", choices=["succinct","verbose"])
    p.add_argument("--format", default="markdown", choices=["markdown","json"])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--post-comment", action="store_true", help="Post summary as PR comment (requires GITHUB_TOKEN and owner/repo/pr env vars)")
    args = p.parse_args(argv)

    adapter = LLMAdapter(api_key=args.openai_api_key, model=args.model)
    reviewer = PRReviewer(adapter=adapter, github_token=args.github_token)

    if args.action == "review":
        diff = git_diff(args.base, args.head, args.path)
        if not diff:
            print("No diff found between refs. Exiting.")
            return 2
        result = reviewer.review(diff, prompt_mode=args.prompt_mode)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_report_to_markdown(result))

        if args.post_comment and not args.dry_run:
            # environment-based owner/repo/pr
            owner = os.getenv("PR_REPO_OWNER")
            repo = os.getenv("PR_REPO_NAME")
            pr_num = os.getenv("PR_NUMBER")
            if not (owner and repo and pr_num):
                print("Missing PR env vars (PR_REPO_OWNER, PR_REPO_NAME, PR_NUMBER); cannot post comment.")
                return 3
            md = format_report_to_markdown(result)
            reviewer.post_comment(owner, repo, int(pr_num), md)
            print("Posted PR comment.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
