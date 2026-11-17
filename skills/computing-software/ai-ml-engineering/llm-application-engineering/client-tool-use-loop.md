---
id: computing-software.ai-ml-engineering.llm-application-engineering.client-tool-use-loop
name: client-tool-use-loop
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-use-loop, tool-use, tool-result, agentic-loop, claude-api, function-calling]
level: practitioner
status: docs-checked
description: "Implement the client tool-use loop: tool_use/tool_result blocks, parallel results in one message, is_error, stop reasons, iteration caps."
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner
  - https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Client tool-use loop (tool_use / tool_result)

## The loop
```python
import anthropic, json
client = anthropic.Anthropic()
tools = [{"name": "get_order", "description": "Look up an order by id. Returns status and items.",
          "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                           "required": ["order_id"]},
          "strict": True}]
messages = [{"role": "user", "content": "Where is order A-1001?"}]

for _ in range(20):                                        # hard cap on iterations
    resp = client.messages.create(model="claude-opus-5-5", max_tokens=16000,
                                  tools=tools, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})   # append full content, not text
    if resp.stop_reason != "tool_use":
        break                                              # end_turn, max_tokens, refusal, pause_turn...
    results = []
    for block in resp.content:
        if block.type == "tool_use":
            try:
                out = run_tool(block.name, block.input)   # input is already parsed JSON
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(out)})
            except Exception as e:
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": f"Error: {e}", "is_error": True})
    messages.append({"role": "user", "content": results})  # ALL results in ONE user message
```

## Rules
- Each `tool_use` block has an `id`; the result must carry it as `tool_use_id`. Tool result blocks must immediately follow the assistant message that called them, with no messages between. A mismatch gives an error such as "tool_use ids were found without tool_result blocks immediately after".
- In the user message, `tool_result` blocks come first; any text goes after all of them (text before a result is a 400).
- Return all parallel results together in the next user message; splitting them across messages "teaches" Claude to avoid parallel calls. Independent read-only calls can run concurrently; the API does not prescribe an execution order.
- Report failures with `is_error: true` and an instructive message (what went wrong and what to try next); do not drop the result. If you choose not to run a call, still return a `tool_result` for it with `is_error: true` and a brief explanation.
- A `max_tokens` stop that cuts off a `tool_use` block leaves an incomplete call: retry with a higher `max_tokens` rather than executing it. Check `refusal` and `pause_turn` stop reasons before assuming a tool call.
- Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1 return a 400 for `tool_choice` `any` or `tool`; steer with descriptions and instructions, and use `strict: true` for schema-valid inputs.
- Tool results often carry untrusted content (web pages, email, uploads): keep it inside `tool_result` blocks, not system prompts.

## Let the SDK do it
`client.beta.messages.tool_runner(...)` with `@beta_tool`-decorated functions runs this loop for you: it handles the agentic loop and error wrapping, loops until Claude returns a message without a tool use or until `max_iterations` if you set it, and supports debug logging, tool-error interception and modifying tool results. For human-in-the-loop approval, custom logging or conditional execution the docs point to the manual loop.

## Verify
- [ ] Tests cover: no tool call, one call, parallel calls, tool exception, iteration cap reached.

## Checked
Method: docs-checked 2026-11-09 against the Claude define-tools, handle-tool-calls, parallel-tool-use, tool-runner and handling-stop-reasons pages (platform.claude.com, markdown versions; tool-runner read by keyword search, others read in the relevant sections). Dropped: the unverified `additionalProperties` schema line, the claim that the tool runner provides approval hooks, and the overview page source (not read).
