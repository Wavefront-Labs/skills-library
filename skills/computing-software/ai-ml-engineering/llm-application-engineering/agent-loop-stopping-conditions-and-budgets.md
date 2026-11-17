---
id: computing-software.ai-ml-engineering.llm-application-engineering.agent-loop-stopping-conditions-and-budgets
name: agent-loop-stopping-conditions-and-budgets
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agent-loop-budget, agents, task-budget, max-turns, stop-reason]
level: practitioner
status: docs-checked
description: "Bound agent loops: stop_reason handling, max turns, token, cost and wall-clock budgets, task budgets, loop detection and graceful wrap-up."
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
  - https://platform.claude.com/docs/en/build-with-claude/task-budgets
  - https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
  - https://openai.github.io/openai-agents-python/running_agents/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agent loop stopping conditions and budgets

**Goal:** agents finish their task or stop cleanly with a useful partial result - never loop forever, burn unbounded tokens, or cut off mid-action.

## Stop reasons to handle (Claude)
| `stop_reason` | Action |
|---|---|
| `end_turn` | done - return the answer |
| `tool_use` | run tools, append results, continue |
| `max_tokens` | output truncated - continue or raise `max_tokens`; never execute a truncated tool call |
| `pause_turn` | server tool loop paused - resend to continue |
| `refusal` | stop; show fallback or route to a fallback model if configured |

## Hard limits in your loop
```python
MAX_TURNS, MAX_COST_USD, DEADLINE = 25, 2.00, time.monotonic() + 300
turns, cost = 0, 0.0
while True:
    resp = client.messages.create(model="claude-opus-5-5", max_tokens=16000, tools=tools, messages=msgs)
    turns += 1; cost += price(resp.usage)
    msgs.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason != "tool_use":
        break
    if turns >= MAX_TURNS or cost >= MAX_COST_USD or time.monotonic() > DEADLINE:
        msgs.append({"role": "user", "content": tool_results_for(resp) + [
            {"type": "text", "text": "Budget reached. Stop calling tools and give your best final answer with what you have, listing anything unfinished."}]})
        final = client.messages.create(model="claude-opus-5-5", max_tokens=8000, tools=tools,
                                       tool_choice={"type": "none"}, messages=msgs)
        break
    msgs.append({"role": "user", "content": run_tools(resp)})
```
Always return tool results for every `tool_use` block before asking for a wrap-up, or the next request is invalid.

## Let the model pace itself
Task budgets (beta, header `task-budgets-2026-03-13`) take `output_config.task_budget` = `{"type": "tokens", "total": N, "remaining": optional}`. The budget spans the full agentic loop (thinking, tool calls, tool results, output) and the model sees a running countdown so it prioritises and finishes gracefully. The countdown is visible only to the model, not in API responses. It is a soft hint, not a hard cap: `max_tokens` is the enforced per-request ceiling, the two are independent, and the docs recommend combining them. Use task budget for pacing and your loop limits as the backstop.

## Framework equivalents
- OpenAI Agents SDK: `max_turns` on the runner; exceeding it raises `MaxTurnsExceeded` (set `max_turns=None` to disable), and an `error_handlers={"max_turns": ...}` handler can return a controlled final output instead.
- Claude SDK tool runner: `max_iterations` ends the loop after that many iterations if set.

## Loop detection
Practitioner heuristic (not from the cited pages): track (tool name, normalised args) per turn; the same call repeated several times with the same result means stuck - inject a message telling the model the approach is not working, or stop. Also cap per-tool call counts.

## Verify
- [ ] Every exit path returns a result object with status (completed, budget_exhausted, error).
- [ ] Turn, token and cost distributions monitored; alerts on tasks hitting limits frequently.
- [ ] A forced-loop test (tool always failing) stops within limits.

## Checked
Method: docs-checked 2026-11-09 against the Claude task-budgets page (read in part and by keyword), handle-tool-calls, tool-runner and handling-stop-reasons pages (platform.claude.com, by keyword search of the stop-reason table and max_tokens section), and the OpenAI Agents SDK running-agents page (max_turns and error handler passages). Dropped: LangGraph recursion_limit paragraph (page unreadable) and the Claude Agent SDK max_turns line (not read).
