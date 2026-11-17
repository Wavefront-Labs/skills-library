---
id: computing-software.ai-ml-engineering.llm-application-engineering.streaming-partial-structured-output
name: streaming-partial-structured-output
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, partial-json-streaming, structured-outputs, streaming, ui, pydantic]
level: practitioner
status: docs-checked
description: "Stream structured JSON output and render it progressively: incremental partial-JSON parsing, partial models, field-level UI updates, and final validation."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/streaming
  - https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming partial structured output

**Goal:** a UI shows a structured result (title, sections, list items) as it is generated, while the final object is still fully validated.

## The core problem
Mid-stream text is truncated JSON (`{"title": "Q3 rev`). `json.loads` fails until the end. You need a tolerant parser that closes open strings, arrays and objects.

## Python
```python
from pydantic_core import from_json
buf = ""
with client.messages.stream(model=MODEL_ID, max_tokens=4096, messages=msgs,
                            output_config={"format": {"type": "json_schema", "schema": REPORT_SCHEMA}}) as stream:
    for text in stream.text_stream:
        buf += text
        partial = from_json(buf, allow_partial=True)        # dict with whatever is complete so far
        render(partial)
    final = stream.get_final_message()
report = Report.model_validate_json(final.content[0].text)  # strict validation at the end
```
With `allow_partial=False` (the default) pydantic_core raises on truncated JSON; with `True` it deserialises the complete part. Pydantic's docs also show passing the partial dict to `Model.model_validate`, which only succeeds if the missing fields are optional.

## Other stacks
On the raw Claude stream, tool-call arguments arrive as `input_json_delta` events carrying `partial_json` fragments. Other SDKs and frameworks offer their own partial-object helpers: check their docs rather than assuming the Python approach.

## UI patterns
- Render fields in schema order; order the schema so the most useful fields come first (summary before details).
- Treat the last item of an array as unstable until the next item starts or the stream ends.
- Do not trigger side effects (saving, sending) on partial data - only on the validated final object.
- Debounce re-renders for long outputs.

## Failure handling
- Check the final message's stop reason: a truncated or refused response has no complete object; show it as partial and offer retry or a fallback.
- Network drop: discard partial state or resume by re-requesting; never persist half objects as final.

## Verify
- [ ] Partial renders never crash on any prefix of a sample output (test by feeding every prefix).
- [ ] Final object validates against the full schema before any persistence.

## Checked
2026-11-01. Confirmed on the Pydantic partial JSON page (`from_json`, `allow_partial` default and behaviour, validating the partial dict) and the Claude streaming page (`text_stream`, `get_final_message()`, `input_json_delta` with `partial_json`). Removed: `trailing-strings`, third-party partial-JSON libraries, OpenAI and Vercel AI SDK and Instructor helper names, render debounce figure, stop-reason specifics.
Method: documentation only; no commands were run.
