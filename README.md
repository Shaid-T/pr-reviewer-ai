

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

Roadmap (short)
- Add additional provider adapters (Anthropic, local LLMs, cloud TTLs).
- Expand plugin checks (SCA, SAST integrations).
- Add an official hosted demo and deployable template for enterprise installs.



License
MIT — see LICENSE.

