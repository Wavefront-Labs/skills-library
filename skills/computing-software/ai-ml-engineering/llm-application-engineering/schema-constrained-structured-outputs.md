---
id: computing-software.ai-ml-engineering.llm-application-engineering.schema-constrained-structured-outputs
name: schema-constrained-structured-outputs
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, structured-output, strict-json-schema, constrained-decoding, output-config, strict-tool-use, json-schema]
level: practitioner
status: docs-checked
description: "Get schema-valid JSON from LLMs with provider structured outputs (Claude output_config format, OpenAI strict json_schema), strict tools, and open-model constrained decoding."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/structured-outputs
  - https://platform.openai.com/docs/guides/structured-outputs
  - https://docs.vllm.ai/en/latest/features/structured_outputs.html
  - https://github.com/dottxt-ai/outlines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema-constrained structured outputs

**Goal:** responses that always parse and validate against your schema, instead of free-form JSON plus retry loops.

## How constraint works
Constrained decoding restricts sampling at each token to tokens that keep the output valid under a grammar compiled from the JSON schema. Output is guaranteed to match the schema's structure; the *content* can still be wrong, so validate semantics.

## Claude
- Response format: `output_config={"format": {"type": "json_schema", "schema": {...}}}` on `messages.create`, or the SDK helper `client.messages.parse(...)` with a Pydantic/Zod model that validates the result. (An older `output_format` parameter is deprecated.)
- Tool arguments: set `strict: true` on a tool definition (with `additionalProperties: false` and `required`) to guarantee `tool_use.input` validates.
- The first request with a new schema has extra latency while the grammar compiles; compiled grammars are cached (24 hours from last use). Changing the schema structure invalidates that cache. The enum value can come back with different capitalisation, so compare enums case-insensitively.
- Claude limits strict schemas per request (strict tools, optional parameters, union-typed parameters): read the limits table on the structured outputs page before designing large schemas.

## OpenAI
```python
resp = client.responses.create(model=..., input=..., text={"format": {
    "type": "json_schema", "name": "invoice", "strict": True, "schema": schema}})
```
Strict mode requires `additionalProperties: false` and every property listed in `required` (express optional fields as `"type": ["string", "null"]`). Check the `refusal` field: a refusal returns text, not your schema.

## Open models
vLLM structured outputs (`guided_json`/`structured_outputs` request params, xgrammar/outlines backends), llama.cpp GBNF grammars, and the Outlines library.

## Schema design rules
- Keep schemas flat and small; deep nesting, huge enums and complex `anyOf` increase grammar compile time and can hit provider limits (check each provider's supported JSON Schema subset).
- Put a free-text `reasoning` field *before* answer fields if you want the model to think before committing; field order is generation order.
- Use enums for categorical outputs; `null` for "not found" instead of empty strings or invented values.

## Still validate
Business rules (dates in range, totals add up, IDs exist) need a validation step after parsing; on failure, re-ask with the error or route to review.

## Verify
- [ ] 100% parse rate across an eval set.
- [ ] Semantic validation errors measured and handled.
- [ ] Schema lives in code (Pydantic/Zod) and is versioned with the prompt.

## Checked
2026-11-01. Confirmed on the Claude structured outputs page: `output_config.format` with `type: "json_schema"`, `client.messages.parse()` with a Pydantic model, `strict: true` tools, `additionalProperties: false`, deprecated `output_format`, first-request grammar compile latency and 24-hour grammar cache. OpenAI strict mode and vLLM/Outlines claims matched their cited pages. Removed: prefill/tool_choice and citations claims, Outlines call syntax.
Method: documentation only; no commands were run.
