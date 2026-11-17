---
id: computing-software.ai-ml-engineering.llm-application-engineering.tool-result-errors-timeouts-and-size-limits
name: tool-result-errors-timeouts-and-size-limits
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-use, tool-result-errors, is-error, tool-timeouts, result-truncation, agent-reliability]
level: practitioner
status: docs-checked
description: "Handle tool failures in LLM agents: is_error results with actionable messages, timeouts and retries, truncating and paginating large outputs, and stopping runaway tool loops."
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
  - https://www.anthropic.com/engineering/writing-tools-for-agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tool errors, timeouts and result size limits

## Return errors to the model, do not crash the loop
```python
async def execute(block):
    try:
        out = await asyncio.wait_for(TOOLS[block.name](**block.input), timeout=TIMEOUTS.get(block.name, 30))
        return {"type": "tool_result", "tool_use_id": block.id, "content": fit(out)}
    except asyncio.TimeoutError:
        msg = f"{block.name} timed out after {TIMEOUTS.get(block.name, 30)}s. Try a narrower query or a smaller date range."
    except ValidationError as e:
        msg = f"Invalid arguments: {e.errors()[0]['loc']} {e.errors()[0]['msg']}. Check the tool schema."
    except NotFound as e:
        msg = f"No record found for {e.key}. Use search_customers to find the correct id."
    except Exception as e:                       # unexpected: log full detail, give the model a short reason
        log.exception("tool failure", extra={"tool": block.name})
        msg = f"{block.name} failed with an internal error; do not retry more than once."
    return {"type": "tool_result", "tool_use_id": block.id, "content": msg, "is_error": True}
```
- Error text is a prompt: say what went wrong and what to do next. Anthropic advises actionable error messages rather than opaque error codes or tracebacks; the API docs give "Rate limit exceeded. Retry after 60 seconds." as an instructive example versus a bare "failed".
- `is_error: true` marks the result as a failed call; Claude incorporates the error into its response, and for invalid calls (for example a missing required parameter) the docs say it retries two to three times with corrections before apologising.
- Every `tool_use` still needs a `tool_result`, including for an unknown tool or malformed input.
- Server tools (web search and similar) are different: Claude handles their errors itself and you do not return `is_error` results for them.
- `strict: true` on tool definitions guarantees inputs match the schema, which removes missing-parameter and type errors.

## Retries
Retry transient failures (network, 429, 5xx) **inside** the tool with backoff before reporting an error; let the model handle semantic errors (bad id, no results). Never auto-retry non-idempotent actions (payments, emails) without an idempotency key. (Engineering practice, not from the cited pages.)

## Result size limits
Large outputs (logs, query results, web pages) consume context. Anthropic suggests some combination of pagination, range selection, filtering and truncation, with sensible default parameter values, for any tool response that could use a lot of context; Claude Code restricts tool responses to 25,000 tokens by default.
```python
def fit(out, max_chars=40_000):
    text = out if isinstance(out, str) else json.dumps(out, default=str)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n[truncated {len(text) - max_chars} chars; call again with offset={max_chars} or add filters]"
```
When truncating, say so in the result and tell the model how to narrow the next call. Design tools with limit, offset and filter parameters and sensible defaults, return semantic identifiers for drill-down, and consider a concise/detailed response format option. Watch tool metrics: many redundant calls suggest rightsizing pagination or token limits; many invalid-parameter errors suggest clearer descriptions or examples.

## Loop guards
- Cap tool calls per task and wall-clock time; on hitting them, ask the model for a final answer with what it has.
- Detect repeats (same tool and arguments several times) and inject a note or stop.
- Check `stop_reason` each turn before executing anything.

## Verify
- [ ] Fault-injection tests: timeout, 500, bad args, huge output - agent recovers or ends gracefully each time.
- [ ] Metrics: tool error rate and truncation rate per tool.

## Checked
Method: docs-checked 2026-11-09 against the Claude handle-tool-calls page (platform.claude.com, error-handling and result-format sections) and the Anthropic engineering post Writing tools for agents (token limits, pagination and error-message passages). Dropped: the OpenAI function-calling source, and the context editing and compaction claim (not confirmed in pages read). Retry and loop-guard advice is practitioner guidance, not source-backed.
