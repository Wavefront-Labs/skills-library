---
id: computing-software.ai-ml-engineering.ollama.capability-structured-outputs
name: capability-structured-outputs
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [structured-outputs, json-schema, format, pydantic]
level: practitioner
status: docs-checked
description: "Constrain replies to JSON or a JSON schema using the format field, with Pydantic or Zod schemas and temperature 0."
sources:
  - https://docs.ollama.com/capabilities/structured-outputs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get machine-parseable output.

Two forms of the `format` field on chat and generate:

- `"format": "json"` returns JSON.
- `"format": { ...JSON schema... }` constrains the reply to the schema.

```
curl -X POST http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
  "model": "gpt-oss",
  "messages": [{"role": "user", "content": "Tell me about Canada."}],
  "stream": false,
  "format": {
    "type": "object",
    "properties": {"name": {"type": "string"}, "capital": {"type": "string"}},
    "required": ["name", "capital"]
  }
}'
```

Tips from the page:

- Define schemas with Pydantic (Python) and pass `Model.model_json_schema()` to `format`, then validate the response; in JavaScript serialise a Zod schema with `z.toJSONSchema()`.
- Also include the schema as a string in the prompt to ground the model.
- Lower the temperature, for example `0`, for more deterministic completions.
- Vision models accept the same `format`, which gives deterministic image descriptions.
- Through the OpenAI-compatible API use `response_format`.

Limitation: Ollama's cloud currently does not support structured outputs; use a local model.

The JSON arrives in `message.content` (examples read `response.message.content`).

## Checked

Method: 2026-11-08 read the full structured outputs page. Claims unchanged and matched; the generate `response` field was dropped from the claim because the page only shows chat.
