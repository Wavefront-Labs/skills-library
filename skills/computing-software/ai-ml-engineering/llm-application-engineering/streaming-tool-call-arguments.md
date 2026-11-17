---
id: computing-software.ai-ml-engineering.llm-application-engineering.streaming-tool-call-arguments
name: streaming-tool-call-arguments
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-streaming, tool-use, streaming, input-json-delta, eager-input-streaming]
level: practitioner
status: docs-checked
description: "Stream tool-call arguments as they are generated: Claude input_json_delta and eager_input_streaming, incremental UIs, and validating before execution."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/streaming
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming tool-call arguments

**Goal:** large tool inputs (file contents, documents, code) appear progressively instead of after a long silent pause, and nothing executes on incomplete or invalid input.

## Claude event sequence
`content_block_start` (block `type: "tool_use"`, with `id`, `name`, empty `input`) -> many `content_block_delta` with `delta.type == "input_json_delta"` and a `partial_json` string fragment -> `content_block_stop`. Concatenate fragments per block index; parse only at `content_block_stop` (or with a tolerant parser for previews).
```python
bufs = {}
with client.messages.stream(model="claude-opus-5-5", max_tokens=64000, tools=tools, messages=msgs) as s:
    for ev in s:
        if ev.type == "content_block_start" and ev.content_block.type == "tool_use":
            bufs[ev.index] = ""
        elif ev.type == "content_block_delta" and ev.delta.type == "input_json_delta":
            bufs[ev.index] += ev.delta.partial_json
            preview(ev.index, bufs[ev.index])
    msg = s.get_final_message()
```

## Eager input streaming
Without `eager_input_streaming`, the API buffers and validates each parameter value before streaming it, so nothing prints for a large parameter until Claude has finished generating it. Set `"eager_input_streaming": true` on each user-defined tool where you want fine-grained streaming, and enable streaming on the request. The docs say all models support it on the Claude API and the listed cloud platforms. With it the API does not buffer or validate input, so:
- the accumulated JSON may be invalid or truncated (`stop_reason: "max_tokens"`),
- you must validate against the tool schema before running the tool,
- on invalid input, you cannot run the tool: return a `tool_result` block with `is_error: true`. The docs suggest wrapping the raw string in a JSON object under a single key (built with a JSON library, not string concatenation) so Claude can tell it received invalid JSON and the original input is preserved.
- a response that stops at `max_tokens` can cut a parameter off midway: check the stop reason and retry with a higher `max_tokens` or repair the partial input.

## UI patterns
- Show which tool is being prepared as soon as `content_block_start` arrives ("Writing report.md...").
- Preview partial content (e.g. a file being written) with a tolerant JSON parser; mark it as draft.
- Execute only after the stream completes and the accumulated input parses and validates.

## Verify
- [ ] Time to first visible tool progress drops for large inputs.
- [ ] Truncated or invalid tool JSON never reaches the executor (test with a tiny `max_tokens`).

## Checked
2026-11-01. Confirmed on the Claude streaming page and the fine-grained tool streaming page: `input_json_delta` partial JSON accumulated and parsed at `content_block_stop`, `eager_input_streaming`, no server buffering or validation, partial or invalid JSON, `max_tokens` truncation, `is_error` tool results and the wrapper suggestion. Removed: OpenAI function-calling deltas and source, the `stop_reason == "tool_use"` and `refusal` checks, non-streaming and server-tool remarks.
Method: documentation only; no commands were run.
