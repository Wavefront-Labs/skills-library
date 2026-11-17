---
id: computing-software.ai-ml-engineering.llm-application-engineering.parallel-tool-calls-and-tool-choice
name: parallel-tool-calls-and-tool-choice
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-use, function-calling, parallel-tool-calls, tool-choice, disable-parallel-tool-use]
level: practitioner
status: docs-checked
description: "Control Claude tool calling: tool_choice (forced any/tool is a 400 on 5.5 models), parallel tool calls, one result message."
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel tool calls and tool_choice

## tool_choice (Claude)
| Value | Behaviour |
|---|---|
| `{"type": "auto"}` (default when tools are given) | Model decides whether and which tools to call |
| `{"type": "none"}` | No tool calls (default when no tools are given) |
| `{"type": "any"}` | Must use one of the provided tools |
| `{"type": "tool", "name": ...}` | Forces that tool |

`any` and `tool` return a 400 on `claude-opus-5-5`, `claude-sonnet-5-5`, Fable 5.1 and Mythos 5.1. Manual extended thinking (`thinking: {type: "enabled"}`) also rejects them. Forced calls prefill the assistant turn, so no natural-language text appears before the `tool_use` block, and thinking is skipped on models that accept forcing. Changing `tool_choice` invalidates cached message blocks (tool definitions and system prompt stay cached).

Replacing forced calls on current models:
- Needed JSON back: use structured outputs instead of a fake tool.
- Needed a specific tool: `auto` plus an explicit instruction ("Use the lookup_order tool in your response"), `strict: true` on the tool for schema-valid arguments, and a check in code that re-prompts if no call occurred.

## Parallel tool calls
By default Claude may call several tools in one response. How you run them is up to you: concurrently, sequentially, or mixed. Independent read-only calls are usually safe in parallel; tools with side effects, shared state or ordering needs may be better run sequentially. Return **all** results in a **single** user message:
```python
tool_uses = [b for b in resp.content if b.type == "tool_use"]
results = await asyncio.gather(*(run_tool(b.name, b.input) for b in tool_uses), return_exceptions=True)
messages += [{"role": "assistant", "content": resp.content},
             {"role": "user", "content": [
                 {"type": "tool_result", "tool_use_id": b.id,
                  "content": str(r) if not isinstance(r, Exception) else f"Error: {r}",
                  "is_error": isinstance(r, Exception)}
                 for b, r in zip(tool_uses, results)]}]
```
- The most common cause of lost parallelism is formatting: a separate user message per result "teaches" Claude to avoid parallel calls.
- Return one `tool_result` per `tool_use` block, matched by `tool_use_id`, including failures (`is_error: true`). If you skip a call (for example an earlier sequential call failed), still return a result for it with `is_error: true` and a short explanation such as "Not executed: the preceding write_file call failed."
- `tool_result` blocks go first in the user content; text after them is allowed.
- Disable parallelism with `disable_parallel_tool_use: true` inside the `tool_choice` object (not a top-level parameter). With `auto` it means at most one tool per response; with `any` or `tool` exactly one.
- To encourage parallelism, add a system prompt instruction for independent lookups (documented for Claude 4 and later); weak prompting is a listed cause of missing parallel calls.
- The SDK tool runner handles multiple tool calls and result formatting for you.
- Computer use and browser use batch actions are stricter: run them sequentially in order and stop at the first failure.

## Verify
- [ ] Integration test with two independent lookups shows one assistant turn with two tool_use blocks and one user turn with two results.
- [ ] No code path sends `tool_choice` any/tool to the models listed above.

## Checked
Method: docs-checked 2026-11-09 against the Claude define-tools (forcing tool use section), parallel-tool-use and handle-tool-calls pages (platform.claude.com, markdown versions). Dropped: the OpenAI equivalents paragraph and platform.openai.com source (unreadable) and the `output_config.format` field name (not confirmed).
