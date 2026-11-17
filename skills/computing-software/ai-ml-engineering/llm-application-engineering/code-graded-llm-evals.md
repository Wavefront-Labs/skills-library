---
id: computing-software.ai-ml-engineering.llm-application-engineering.code-graded-llm-evals
name: code-graded-llm-evals
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, code-graded-evals, llm-evaluation, exact-match, unit-tests, pass-at-k]
level: practitioner
status: docs-checked
description: "Grade LLM outputs with code where possible: exact and normalised match, regex, schema and numeric checks, tool-call assertions, sandboxed unit tests and unbiased pass@k."
sources:
  - https://docs.claude.com/en/docs/test-and-evaluate/develop-tests
  - https://arxiv.org/abs/2107.03374
  - https://platform.openai.com/docs/guides/evals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Code-graded evals

**Goal:** fast, cheap, deterministic grading for every output property that can be checked by code, leaving LLM judges only for what truly needs judgment.

## Grader types
| Grader | Use for | Example |
|---|---|---|
| Exact match | labels, ids, short answers | `pred == gold` |
| Normalised match | case, whitespace, punctuation variations | `norm(pred) == norm(gold)` |
| Set / multi-label | extracted entities | precision, recall, F1 over sets |
| Regex / contains | required phrases, forbidden content | `re.search(r"\bINV-\d{6}\b", out)` |
| Schema validation | structured output | `Model.model_validate_json(out)` |
| Numeric tolerance | calculations | `abs(pred - gold) <= 0.01 * abs(gold)` |
| Tool-call assertions | agents | right tool, required args, no forbidden tools |
| Execution | code generation, SQL | run tests or compare query results |

## Example harness
```python
import json, re
def norm(s): return re.sub(r"\s+", " ", s.strip().lower().rstrip("."))
def grade(case, out):
    checks = {
        "label": norm(out["label"]) == norm(case["gold_label"]),
        "invoice_ids": set(out["invoice_ids"]) == set(case["gold_invoice_ids"]),
        "no_pii": not re.search(r"\b\d{16}\b", json.dumps(out)),
    }
    return {"pass": all(checks.values()), **checks}
```
Report each check separately; a single pass/fail hides which property regressed.

## Code generation: tests and pass@k
Run generated code in a sandbox (container with no network, CPU/memory/time limits). Generate n samples per problem, count c passing; the unbiased estimator is `pass@k = 1 - C(n-c, k) / C(n, k)`:
```python
from math import comb
def pass_at_k(n, c, k): return 1.0 if n - c < k else 1 - comb(n - c, k) / comb(n, k)
```
For SQL, compare result sets (order-insensitive unless ORDER BY is required), not query text.

## Designing gradeable tasks
- Ask for structured output so fields can be checked individually.
- Prefer closed answers (enums, ids) in eval design when the product allows.
- Keep gold data versioned; when the grader and the gold disagree with a human, fix the gold or the grader, not the threshold.

## Combine with judges
Use code graders as gates (format, safety regexes, tool rules) and LLM judges or humans for tone, helpfulness and faithfulness. Code checks run on every commit; judges on release candidates.

## Verify
- [ ] Each grader has unit tests with known pass and fail outputs.
- [ ] Code execution graders run sandboxed with resource limits.
- [ ] Results reported per check and per slice.

## Checked
2026-11-01. Confirmed against the Codex paper (arXiv 2107.03374): generate n samples per task, count the c that pass unit tests, and use the unbiased estimator 1 - C(n-c, k)/C(n, k) averaged over problems; generated code was run in a sandbox. Anthropic's develop-tests page and OpenAI's evals guide support code-based grading alongside model grading. Code snippets are illustrative.
Method: documentation only; no commands were run.
