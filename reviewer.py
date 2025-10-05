
from typing import Dict, Optional, Any
import os
import time
import json
import logging
import requests
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def safe_extract_json(text: str) -> Optional[Dict[str, Any]]:
    #try to extract a JSON object from LLM response.
    
    text = re.sub(r"```(?:json)?\n?", "", text)
    start = text.find("{")
    if start == -1:
        return None
  
    for end in range(len(text), start, -1):
        try:
            candidate = text[start:end]
            return json.loads(candidate)
        except Exception:
            continue

    try:
        candidate = text[start : text.rfind("}") + 1]
        return json.loads(candidate)
    except Exception:
        return None

#LLM Adapter 
class LLMAdapter:
    def __init__(self, api_key: Optional[str] = None, model: str = "openai/gpt-4", timeout: int = 30):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str, max_tokens: int = 800, retries: int = 2) -> str:
        #generate text If API key present call OpenAI otherwise return dry run response more providers can be added by subclassing
        if not self.api_key:
            logger.info("No API key: returning dry-run response.")
            return "DRY-RUN: no API key configured. Prompt head:\n\n" + prompt[:2000]

        for attempt in range(retries + 1):
            try:
                import openai

                openai.api_key = self.api_key
                resp = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    timeout=self.timeout,
                )
                return resp["choices"][0]["message"]["content"]
            except Exception as e:
                logger.warning("LLM call failed (attempt %s): %s", attempt + 1, e)
                if attempt == retries:
                    raise
                time.sleep(1 + attempt * 2)
        return ""

#Prompt Builder
def build_prompt(diff: str, mode: str = "succinct") -> str:

    header = (
        "You are an expert code reviewer. Given the git diff, produce a JSON object with these keys:\n"
        "  - summary: short summary (1-3 lines)\n"
        "  - issues: list of top issues (security, correctness, style, tests)\n"
        "  - suggestions: suggested code changes or commands\n"
        "  - checklist: actionable checklist for the author\n\n"
        "Return only valid JSON when possible. If you cannot, still include a JSON object in the response.\n\n"
    )
    if mode == "succinct":
        header += "Be concise (use short bullet lines). Prioritize security and correctness.\n\n"
    else:
        header += "Explain reasoning in a bit more detail for each issue and suggestion.\n\n"

  
    max_diff_chars = 15000 if mode == "succinct" else 25000
    snippet = diff[:max_diff_chars]
    prompt = header + "Git diff:\n" + snippet
    return prompt

#PR Reviewer
class PRReviewer:
    def __init__(self, adapter: Optional[LLMAdapter] = None, github_token: Optional[str] = None):
        self.adapter = adapter or LLMAdapter()
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

    def review(self, diff: str, prompt_mode: str = "succinct") -> Dict[str, Any]:
        prompt = build_prompt(diff, mode=prompt_mode)
        raw = self.adapter.generate(prompt)
        parsed = safe_extract_json(raw)
        if parsed:
            return {"ok": True, "report": parsed}
      
        return {"ok": True, "report_raw": raw}

    def post_comment(self, owner: str, repo: str, pr_number: int, body_markdown: str, as_check_run: bool = False) -> Dict[str, Any]:
       
        if not self.github_token:
            raise RuntimeError("No GITHUB_TOKEN configured for posting comments/checks.")

        headers = {"Authorization": f"Bearer {self.github_token}", "Accept": "application/vnd.github+json"}
        if as_check_run:
        
            logger.info("GitHub check-run requested but not fully implemented; falling back to PR comment.")
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
        payload = {"body": body_markdown}
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()
