---
id: computing-software.ai-ml-engineering.langchain.tool-error-handling-and-artifacts
name: tool-error-handling-and-artifacts
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, agents, tool-error-handling, toolexception, toolnode, handle-tool-errors, content-and-artifact, tool-retries]
level: practitioner
status: verified
description: "Make LangChain/LangGraph tools fail gracefully: ToolException and handle_tool_error, ToolNode error handling, validation errors, retries, and content_and_artifact outputs."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://langchain-ai.github.io/langgraph/reference/agents/#langgraph.prebuilt.tool_node.ToolNode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tool error handling and artifacts

**Goal:** tool failures become information the model can act on (retry with fixed arguments, ask the user) instead of crashing the agent run.

## Errors as observations
```python
from langchain_core.tools import tool, ToolException

@tool
def get_invoice(invoice_id: str) -> str:
    """Fetch an invoice by ID (format INV-000123)."""
    if not invoice_id.startswith("INV-"):
        raise ToolException("invoice_id must look like INV-000123")
    return fetch(invoice_id)

get_invoice.handle_tool_error = True     # ToolException text returned to the model instead of raising
```
`handle_tool_error` can also be a string or a function `(err) -> str` to customise the message.

In LangGraph, `ToolNode(..., handle_tool_errors=True)` catches every exception from a tool and returns a `ToolMessage` with `status="error"` whose text is `Error: ValueError('secret stack')  Please fix your mistakes.`, so the model sees it and can retry (run, langgraph-prebuilt 1.1.1). The DEFAULT (`_default_handle_tool_errors`) is narrower: it only handles tool-invocation/validation errors and unknown tool names, and re-raises exceptions raised inside the tool body (run: `ValueError` propagated out of the graph). Other accepted values: a `str` (fixed message), a callable `(e) -> str`, an exception type or tuple (only those are caught, others raise), `False` (raise). Use a callable or string to avoid leaking internal details to the model (and through it, to users).

## Validation errors
Arguments are validated against the tool's schema (from type hints or `args_schema`). Bad arguments raise a validation error before your function runs (run: `ValidationError` from `tool.invoke`); the default `ToolNode` returns it to the model as an error `ToolMessage`. Clear field descriptions and constrained types (`Literal`, enums, patterns) prevent most of these.

## Retries and timeouts
- Transient failures (HTTP 5xx, timeouts) should be retried inside the tool with backoff - don't spend model turns on them.
- Put a timeout on every network call in a tool; a hung tool hangs the agent.
- Cap repeated failing calls: the recursion limit ends the loop, but a custom counter in state lets you stop earlier with a useful message.

## Content and artifact
Return a short summary to the model and keep the full payload for the application:
```python
@tool(response_format="content_and_artifact")
def search_orders(query: str) -> tuple[str, list[dict]]:
    """Search orders matching a free-text query."""
    rows = run_search(query)
    return f"Found {len(rows)} orders; top: {rows[0]['id'] if rows else 'none'}", rows
```
Run: invoking with a tool-call dict returns a `ToolMessage` with `content="Found 2"` and the artifact list. `ToolMessage.content` goes to the model; `ToolMessage.artifact` holds `rows` for your UI or later steps, without consuming context tokens.

## Verify
- [ ] Forced tool failures produce an error ToolMessage and the agent recovers or explains.
- [ ] Error messages sent to the model contain no secrets or stack traces.
- [ ] Large tool outputs summarised for the model, full data kept as artifacts.
