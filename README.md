
# pr-reviewer-ai 🚀

<p align="center">
  <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExb25wdG83eDZ1dWh2a2hhZ3VkbWpueXY5ZXRpN2t3eGtwZDEzOHpudyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RpfIXomvjCh8I/giphy.gif" alt="Glowing Star" width="100">
  <br>
  <b>⭐ Please Star this Repo if You Enjoy It! ⭐</b>
</p>


[![Stars](https://img.shields.io/github/stars/Shaid-T/pr-reviewer-ai?style=social)](https://github.com/Shaid-T/pr-reviewer-ai/stargazers)
[![Build](https://img.shields.io/github/actions/workflow/status/Shaid-T/pr-reviewer-ai/ci.yml?branch=main)](https://github.com/Shaid-T/pr-reviewer-ai/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues Welcome](https://img.shields.io/badge/Issues-Good%20first%20issue-brightgreen.svg)](.github/ISSUE_TEMPLATE/good_first_issue.md)

> Fast, privacy-first automated PR reviews powered by LLMs — one-click GitHub Action + local CLI.
> Summarize diffs, surface security/style issues, suggest fixes, and post rich PR comments or check-run reports.

Why star this project?
- Saves maintainers time by producing actionable, review-quality suggestions for PRs.
- One-click GitHub Action and a local CLI so anyone can try it in minutes (dry-run mode included).
- Provider-agnostic: works with OpenAI or self-hosted LLM adapters (privacy-friendly).
- Lightweight, tested, and easy to extend with new checks or provider adapters.

Demo
![demo gif placeholder](./assets/demo.gif)

TL;DR — Try it in 60 seconds
1. Add the Action example workflow (see /examples/pr-review.yml).
2. (Optional) Add OPENAI_API_KEY secret to your repo for live LLM suggestions.
3. Open a PR — the Action will run and post a summary (or produce an artifact).

Quickstart — GitHub Action (recommended)
1. Create a workflow file at .github/workflows/pr-review.yml with this minimal example:
```yaml
name: PR Review (LLM)
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  llm-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run PR reviewer
        uses: ./  # use this repo as a local action or replace with user/repo@vX.Y
        with:
          model: "openai/gpt-4"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }} # optional
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}     # provided automatically in Actions
```
2. Open a PR — the Action runs in dry-run mode by default unless configured to post comments.

Local Quickstart — CLI
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Dry-run: no API key required
python -m pr_reviewer.cli review --path . --base main --head HEAD --dry-run --format markdown
# With OpenAI (live suggestions)
export OPENAI_API_KEY="sk-..."
python -m pr_reviewer.cli review --path . --base main --head HEAD --format markdown
```

Key Features
- Summaries: 1–3 line PR summary from the diff.
- Top issues: prioritized list (security, correctness, tests, style).
- Suggestions: concrete fixes, code snippets, commands.
- Checklist: actionable next steps for the PR author.
- Outputs: Markdown, JSON; post as PR comment or GitHub Check Run.
- Extensible: add new check plugins (security scanner, lint integrations).

Config (.pr-reviewer.yml)
```yaml
model: openai/gpt-4
prompt_mode: succinct   # succinct | verbose
max_tokens: 1200
comment_on_pr: false    # Action mode: set true to post comments
post_as_checkrun: true
checks:
  - type: security
  - type: style
  - type: tests
```

Security & Privacy
- Dry-run by default when no OPENAI_API_KEY is present.
- Supports local/self-hosted adapters so organizations can avoid sending code externally.
- Do not include secrets or large sensitive artifacts in diffs you submit to third-party LLMs.
- Use prompt redaction if your repo contains sensitive info.

Integration examples
- GitHub Action: post a comment summary or create a check-run with the reviewer output.
- CI artifact: upload the JSON report for dashboards or further processing.
- Bot mode: integrate with Slack/MS Teams to ping relevant engineers for high-risk changes.

Best practices for adoption
- Start with dry-run mode and review suggestions manually before enabling auto-comments.
- Combine with existing linters and security scanners; use the LLM reviewer to produce human-friendly explanations and prioritized context.
- Seed repository with a small set of "good first issue" tasks to attract contributors.

Contributing
We welcome contributions — here's how to help:
- Open issues for feature requests or bugs.
- Add an LLM provider by implementing an adapter class.
- Add new checks under src/pr_reviewer/checks/.
- Follow the code style: black and pylint; run tests with pytest.
See CONTRIBUTING.md for details and the contributor checklist.

Roadmap (short)
- Add additional provider adapters (Anthropic, local LLMs, cloud TTLs).
- Expand plugin checks (SCA, SAST integrations).
- Add an official hosted demo and deployable template for enterprise installs.

Troubleshooting
- No diff found? Ensure base and head refs are correct.
- Missing PR env vars? The Action sets these automatically — for local posting, set PR_REPO_OWNER, PR_REPO_NAME, PR_NUMBER.
- LLM errors: check model and API key limits; fall back to dry-run to test locally.

Support & Contact
- Open an issue or discussion in this repo.
- For partnership or demo requests, open an issue titled "demo / partnership".

Acknowledgements
- Inspired by community tools around automating reviews, and built to be open, auditable, and extensible.

License
MIT — see LICENSE.

Thanks for trying pr-reviewer-ai — if this saves you a few minutes on a PR, consider starring the repo to help others discover it!
