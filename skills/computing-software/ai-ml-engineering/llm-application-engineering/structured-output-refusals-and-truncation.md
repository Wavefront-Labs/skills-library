---
id: computing-software.ai-ml-engineering.llm-application-engineering.structured-output-refusals-and-truncation
name: structured-output-refusals-and-truncation
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, structured-output-refusals, structured-output, stop-reason, max-tokens, refusal-handling]
level: practitioner
status: docs-checked
description: "Handle the cases where structured output is not valid JSON: refusal stop reasons, max_tokens truncation, schema-valid but wrong content, retries and safe fallbacks."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/structured-outputs
  - https://docs.claude.com/en/api/handling-stop-reasons
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Refusals and truncation in structured output

Anthropic notes structured outputs guarantee schema compliance in most cases, with exceptions for refusals and token-limit cut-offs. Check why it stopped before parsing.

## Claude API
```python
import anthropic, json
client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-5-5", max_tokens=4096,
    output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    messages=[{"role": "user", "content": doc}])

if resp.stop_reason == "refusal":
    log.warning("refused", category=resp.stop_details and resp.stop_details.category)
    result = fallback_result()                  # do not parse: content may be partial or empty
elif resp.stop_reason == "max_tokens":
    raise RetryWithMoreTokens()                 # JSON is cut off mid-object
else:
    result = json.loads(next(b.text for b in resp.content if b.type == "text"))
```
- A refusal still returns HTTP 200 and is billed for generated tokens; the refusal message takes precedence over the schema, so output may not match it.
- `stop_details` identifies the policy category on a refusal and is null for all other stop reasons; always guard.
- A schema property asking for the model's thinking or step-by-step reasoning can trigger a `reasoning_extraction` refusal; ask for a short explanation instead.
- On `max_tokens` the output may be incomplete; retry with a higher `max_tokens`.
- `client.messages.parse()` returns a parsed model; still branch on `stop_reason`.

## Truncation
- Size `max_tokens` for the largest legitimate output (long lists).
- Array constraints beyond `minItems` of 0 or 1 are not supported by the API, so bound size by asking for top-N and paginate large extractions.

## Valid but wrong
Schema validity does not mean correct values. Add semantic checks (IDs exist, dates in range, totals add up) and send failures back for one retry with the error message, then fall back to human review.

## Verify
- [ ] Tests simulate each stop reason (mock responses) and assert the fallback path; dashboards count refusals and truncations per route.

## Checked
2026-11-01. Confirmed against Anthropic's Structured outputs page (Invalid outputs: refusal 200 status and billing, schema precedence, reasoning_extraction, max_tokens retry; output_config.format json_schema; minItems limit; messages.parse) and Handling stop reasons (stop_details null except on refusal). Removed: OpenAI section and source (not fetched), the cyber/bio categories, the fallbacks option for named models, and the maxItems and streaming advice.
Method: documentation only; no commands were run.
