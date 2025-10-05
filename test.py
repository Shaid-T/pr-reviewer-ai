
from pr_reviewer.reviewer import build_prompt, LLMAdapter, PRReviewer

def test_build_prompt_truncation():
    diff = "a" * 20000
    p = build_prompt(diff, mode="succinct")
    assert "Git diff:" in p
    assert len(p) < 16000 + 2000  # header + truncated diff

def test_adapter_dryrun():
    adapter = LLMAdapter(api_key=None)
    out = adapter.generate("hello")
    assert out.startswith("DRY-RUN")
