---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-content-moderation-input-output
name: llm-content-moderation-input-output
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, guardrails, content-moderation, moderation-api, llama-guard, safety-classifiers, output-filtering]
level: practitioner
status: docs-checked
description: "Moderate LLM inputs and outputs: OpenAI moderation endpoint, Llama Guard, LLM-based policy classifiers, thresholds per category, streaming output checks and refusal handling."
sources:
  - https://platform.openai.com/docs/guides/moderation
  - https://docs.claude.com/en/docs/about-claude/use-case-guides/content-moderation
  - https://huggingface.co/meta-llama/Llama-Guard-3-8B
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input/output moderation and content classifiers

**Goal:** enforce your product's content policy (beyond the model's built-in safety) on what users send and what the model returns, with measurable precision/recall.

## Options
| Classifier | Notes |
|---|---|
| OpenAI moderation (`omni-moderation-latest`) | Accepts text and image (not audio); the endpoint is documented as free; returns `flagged`, `categories` and `category_scores` |
| Llama Guard 3 (self-hosted) | Open weights; aligned to the MLCommons hazards taxonomy plus a code interpreter abuse category |
| LLM-as-classifier (a small, cheap Claude model) | Your own policy in natural language, with categories you can customise; best for product-specific rules |

```python
from openai import OpenAI
r = OpenAI().moderations.create(model="omni-moderation-latest", input=user_text)
res = r.results[0]
if res.flagged or res.category_scores.self_harm > SELF_HARM_THRESHOLD:  # tune on your data
    route_to_safe_flow(res)
```
Custom policy classifier:
```python
verdict = client.messages.parse(
    model=SMALL_MODEL_ID, max_tokens=200,
    system=POLICY_TEXT,            # numbered rules with examples of allowed/disallowed
    messages=[{"role": "user", "content": f"<content>{text}</content>\nClassify against the policy."}],
    output_format=Verdict,          # Pydantic: allowed: bool, rule_ids: list[int], confidence: float
).parsed_output
```

## Where to check
- **Input:** before the main model call (block, redirect to resources, or answer with a policy message). Run in parallel with the main call to save latency, and discard the answer if the check fails.
- **Output:** before showing/sending. OpenAI inline moderation scores arrive only after the full output is available, not with partial deltas; with streaming, buffer by sentence or chunk and check incrementally, or stream and retract (only acceptable for low-severity categories). Treat scores as signals for your policy, not automatic blocking decisions.
- **Tool actions:** check content before posting it externally (emails, comments).

## Thresholds and evaluation
- Set thresholds per category from labelled samples of *your* traffic; self-harm and minors-related categories warrant low thresholds and human escalation paths, others higher to avoid over-blocking.
- Track false positive rate (blocked legitimate use) as closely as misses - over-blocking drives users away.
- Handle model refusals gracefully: check the response's stop reason and content before using it, and show a clear message.
- Log decisions (category, score, action) without storing more sensitive content than needed.

## Verify
- [ ] Labelled eval set per category with precision/recall at chosen thresholds.
- [ ] Self-harm flows route to crisis resources; tested end to end.
- [ ] Output check covers streamed responses.

## Checked
2026-11-01. Confirmed on the OpenAI moderation guide (`omni-moderation-latest`, text and image input, free endpoint, inline moderation, scores after full output, scores are signals), the Llama Guard 3 model card (MLCommons taxonomy, code interpreter abuse category) and the Claude content moderation guide (customisable unsafe categories, small model for cost). Removed: model ids, Llama Guard 4 and cloud-service rows, numeric threshold, `refusal` stop-reason claim.
Method: documentation only; no commands were run.
