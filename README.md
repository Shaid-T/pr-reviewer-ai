```markdown
# pr-reviewer-ai 🚀

[![Stars](https://img.shields.io/github/stars/Shaid-T/pr-reviewer-ai?style=social)](https://github.com/Shaid-T/pr-reviewer-ai/stargazers)
[![CI](https://img.shields.io/github/actions/workflow/status/Shaid-T/pr-reviewer-ai/ci.yml?branch=main)](https://github.com/Shaid-T/pr-reviewer-ai/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A privacy-first, production-ready GitHub Action + CLI that uses LLMs to automatically review pull requests: summarize diffs, surface security & style issues, propose changes, and post rich PR comments or check-run reports.

Why this project gets stars
- Solves a universal problem: faster, higher-quality PR reviews for maintainers and contributors.
- One-click Action & local CLI — easy to try and adopt.
- Configurable prompts and provider-agnostic adapters (OpenAI, local LLMs).
- Privacy-first defaults: dry-run mode when API keys aren't provided; optional PR commenting.
- Extensible: add new checks (security, tests, linter suggestions) with simple plugin hooks.

Demo (gif placeholder)
![demo gif](./assets/demo.gif)

Quickstart — GitHub Action (one minute)
1. Fork or add this repo as a template.
2. Create a workflow file (.github/workflows/pr-review.yml) using the `pr-reviewer-ai` Action (example in /examples).
3. Set repository secret: GITHUB_TOKEN (Actions provides one automatically). For cloud LLMs add OPENAI_API_KEY if you want live suggestions.
4. Open a PR — the Action will attach a review summary.

Local Quickstart (CLI)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# dry-run local review (no API keys required)
python -m pr_reviewer.cli review --path . --base main --head HEAD --dry-run --format markdown
```

Features
- Concise summary, top issues, suggested fixes, checklist for authors.
- Post summary as: PR comment, GitHub Check Run, or upload JSON artifact in CI.
- Support for multiple LLM providers via adapter pattern.
- Config file (.pr-reviewer.yml) for per-repo settings and templates.
- Lightweight Docker image for reproducible CI runs.

Config example (.pr-reviewer.yml)
```yaml
model: openai/gpt-4
comment_on_pr: true
post_as_checkrun: true
max_tokens: 1200
prompt_mode: succinct # succinct | verbose
checks:
  - type: security
  - type: style
  - type: tests
```

How you can help
- Star the repo if you find it useful — it helps others discover it.
- Try the CLI and one-click Action and open issues with feedback.
- Add adapters for other LLM providers or new check plugins.

Security & Privacy
- Default dry-run prevents accidental data leakage.
- Option to use self-hosted LLM adapters (no external calls).
- When using public cloud LLMs, avoid sending full secrets or sensitive data; configure prompts to redact.

Contributing
- See CONTRIBUTING.md for development, tests, and how to add adapters.
- Look for issues tagged "good first issue".

License
- MIT
```
